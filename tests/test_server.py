import base64
import importlib
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from google.protobuf import descriptor_pb2
from google.protobuf import json_format as jf
from api import common as cm
from server import create_app, request_type
from storage import read_document, write_document

FIXTURES = Path(__file__).parent / 'fixtures'
UPSTREAM = json.loads((FIXTURES / 'upstream-routes.json').read_text())
UNSUPPORTED = {
    '/achievement/receive', '/achievement/receive_all', '/friend/delete', '/friend/invite',
    '/friend/ng_invite', '/friend/ok_invite', '/item/sell', '/present/receive',
    '/present/receive_all', '/recipe/create', '/unit/evolve', '/unit/level_up',
    '/user/set_transfer_password', '/weapon/sell',
}
PARAMS = {
    '/archive/read': {'quest_id': 99999991}, '/archive/release': {'quest_id': 99999991},
    '/board/release': {'unit_id': 311001001, 'sheet_no': 1, 'square_id': 1},
    '/deck/change_name': {'deck_no': 1, 'name': 'New deck'},
    '/deck/save': {'t_user_deck': {'deck_no': 1, 'name': 'Saved', 'unit_id_1': 311001001}},
    '/eventmap/get': {'event_id': 1}, '/exchange/item_list': {'exchange_id': 1},
    '/friend/search': {'view_user_id': 1},
    '/gacha/draw': {'gacha_id': 3010001, 'detail_id': 30100012},
    '/gacha/rate_list': {'gacha_id': 3010001}, '/information/read': {'information_id': 1},
    '/load/split': {'section': 1}, '/quest/start': {'quest_id': 99999991, 'deck_no': 1},
    '/quest/start_adv': {'quest_id': 99999991}, '/shop/item_list': {'shop_id': 1},
    '/spy/start': {'user_spy_id': 1, 'unit_id': 311001001, 'sub_unit_id': 311002001},
    '/spy/clear': {'user_spy_id': 1}, '/spy/stop': {'user_spy_id': 1},
    '/tips/save': {'tips_id_list': [110001]}, '/tutorial/register_name': {'user_name': 'New name'},
    '/tutorial/update_progress': {'status': 99}, '/tutorialhowtoplay/save': {'tutorial_type': 9999},
    '/user/change_name': {'name': '이름'}, '/user/change_comment': {'comment': 'Hello'},
    '/user/change_emblem': {'emblem_id': 10100000}, '/user/change_friend_unit': {'unit_id': 311001001},
    '/user/change_home_bg': {'background_id': 110100002},
    '/user/change_home_unit_main': {'unit_id': 311001001},
    '/user/change_home_unit_sub': {'unit_id': 311002001},
    '/weapon/equip': {'unit_id': 311001001, 'user_weapon_id': 1},
    '/weapon/lock': {'weapon_list': [{'user_weapon_id': 1}], 'flag': 1},
}


def response_type(path):
    module, action = path.strip('/').split('/')
    cls = 'Response' + ''.join(part.title() for part in action.split('_'))
    return getattr(importlib.import_module('proto.' + module + '_pb2'), cls)


def post(client, path, params=None, **kwargs):
    query = jf.ParseDict(params or {}, request_type(path)())
    return client.post(path, data=query.SerializeToString(), **kwargs)


def decoded(client, path, params=None):
    result = post(client, path, params)
    assert result.status_code == 200, (path, result.status_code, result.headers)
    return response_type(path).FromString(result.data)


def begin(client, kind='battle', quest_id=99999991):
    path = '/quest/start_adv' if kind == 'adventure' else '/quest/start'
    return decoded(client, path, dict(quest_id=quest_id, **({'deck_no': 1} if kind == 'battle' else {}))).token


def snapshot(app):
    with app.extensions['store'].transaction() as db:
        return dict(db.execute('SELECT name,value FROM documents').fetchall())


@pytest.mark.parametrize('path', UPSTREAM + ['/spy/stop'])
def test_upstream_routes_have_valid_protobuf_responses(client, path):
    params = PARAMS.get(path, {})
    if path in ('/quest/clear', '/quest/clear_adv', '/quest/fail', '/quest/continue', '/quest/retire'):
        token = begin(client, 'adventure' if path == '/quest/clear_adv' else 'battle')
        params = {'quest_id': 99999991}
        if path != '/quest/retire': params['token'] = token
    if path in ('/spy/clear', '/spy/stop'):
        decoded(client, '/spy/start', PARAMS['/spy/start'])
    result = post(client, path, params)
    assert result.status_code == (501 if path in UNSUPPORTED else 200), (path, result.headers)
    assert result.mimetype == 'application/x-protobuf'
    assert result.headers['X_RES_STATUS'] == ('1' if path in UNSUPPORTED else '0')
    assert result.headers['X_SQLITE_VER'] == '99'
    assert int(result.headers['X_TIMESTAMP']) > 0
    if path not in UNSUPPORTED: response_type(path).FromString(result.data)


@pytest.mark.parametrize('path', UPSTREAM + ['/spy/stop'])
def test_malformed_packets_are_rejected_without_changes(app, client, path):
    before = snapshot(app)
    result = client.post(path, data=b'\x80')
    assert result.status_code == 400, (path, result.status_code)
    assert result.headers['X_RES_STATUS'] == '1'
    assert not result.data
    assert snapshot(app) == before


def wire_signature(file):
    def message(m):
        return {'fields': [(f.name, f.number, f.type, f.label, f.type_name, f.oneof_index if f.HasField('oneof_index') else None)
                           for f in m.field],
                'nested': {n.name: message(n) for n in m.nested_type},
                'enums': {e.name: [(v.name, v.number) for v in e.value] for e in m.enum_type}}
    return (file.package, file.syntax, {m.name: message(m) for m in file.message_type},
            {e.name: [(v.name, v.number) for v in e.value] for e in file.enum_type})


def test_all_regenerated_schemas_keep_upstream_wire_contract():
    for encoded in (FIXTURES / 'upstream-descriptors.pb64').read_text().splitlines():
        original = descriptor_pb2.FileDescriptorProto.FromString(base64.b64decode(encoded))
        module = importlib.import_module('proto.' + original.name.replace('.proto', '_pb2'))
        current = descriptor_pb2.FileDescriptorProto.FromString(module.DESCRIPTOR.serialized_pb)
        assert wire_signature(current) == wire_signature(original), original.name


def test_all_load_sections_parse(client):
    index = decoded(client, '/load/split', {'section': 0})
    assert index.max_section == 22
    for section in range(1, index.max_section + 1):
        data = decoded(client, '/load/split', {'section': section})
        assert data.current_section == section
        assert data.max_section == index.max_section
    assert post(client, '/load/split', {'section': 23}).status_code == 400


def test_profiles_decks_weapons_and_progress_survive_restart(app, client):
    for path in ('/user/change_name', '/user/change_home_bg', '/deck/save', '/weapon/equip', '/weapon/lock',
                 '/tips/save', '/tutorialhowtoplay/save', '/tutorial/register_name'):
        decoded(client, path, PARAMS[path])
    before = snapshot(app)
    restarted = create_app(dict(app.config))
    assert snapshot(restarted) == before
    user = json.loads(before['t_user'])['t_user']
    assert user['name'] == 'New name'
    assert user['home_background_id'] == 110100002
    assert json.loads(before['t_user_deck_list'])['t_user_deck_list'][0]['name'] == 'Saved'
    assert json.loads(before['t_user_weapon_list'])['t_user_weapon_list'][0]['lock_flag'] == 1
    decoded(restarted.test_client(), '/weapon/equip', {'unit_id': 311002001, 'user_weapon_id': 1})
    rows = json.loads(snapshot(restarted)['t_user_unit_weapon_list'])['t_user_unit_weapon_list']
    assert rows == [{'user_id': 1, 'unit_id': 311002001, 'user_weapon_id': 1}]
    decoded(restarted.test_client(), '/weapon/equip', {'unit_id': 311002001, 'user_weapon_id': 0})
    assert json.loads(snapshot(restarted)['t_user_unit_weapon_list'])['t_user_unit_weapon_list'] == []


def test_invalid_deck_rolls_back_name_change(app, client):
    before = snapshot(app)
    result = post(client, '/deck/save', {'t_user_deck': {'deck_no': 1, 'name': 'Must rollback', 'unit_id_1': 999}})
    assert result.status_code == 400
    assert snapshot(app) == before
    assert post(client, '/deck/change_name', {'deck_no': 0, 'name': 'bad'}).status_code == 400


def test_quest_settlement_is_atomic_replay_safe_and_monotonic(app, client):
    token = begin(client)
    query = dict(quest_id=99999991, token=token, is_clear_mission_1=True,
                 is_clear_mission_2=True, is_clear_mission_3=True)
    first = post(client, '/quest/clear', query)
    assert first.status_code == 200
    one = snapshot(app)
    assert post(client, '/quest/clear', query).data == first.data
    assert snapshot(app) == one
    restarted = create_app(dict(app.config))
    assert post(restarted.test_client(), '/quest/clear', query).data == first.data
    token2 = begin(client)
    second = decoded(client, '/quest/clear', {'quest_id': 99999991, 'token': token2})
    assert second.t_user_quest.clear_count == 2
    assert second.t_user_quest.quest_mission_id_1 == 1
    assert len(second.mission_complete_reward_list) == 0
    first_reply = response_type('/quest/clear').FromString(first.data)
    reward_id = first_reply.drop_list[0].resource_id
    items = json.loads(snapshot(app)['t_user_item_list'])['t_user_item_list']
    assert next(i['amount'] for i in items if i['item_id'] == reward_id) >= 10
    assert json.loads(snapshot(app)['t_user'])['t_user']['exp'] == 360
    assert post(client, '/quest/clear', dict(query, token='invalid')).status_code == 409


def test_failed_quest_rolls_back_every_resource(app, client, monkeypatch):
    token = begin(client)
    before = snapshot(app)
    def fail(amount): raise RuntimeError('injected failure after multiple writes')
    monkeypatch.setattr(cm, 'add_user_gold', fail)
    result = post(client, '/quest/clear', {'quest_id': 99999991, 'token': token})
    assert result.status_code == 500
    assert result.headers['X_RES_STATUS'] == '1'
    assert snapshot(app) == before


def test_cancelled_and_mismatched_quests_cannot_settle(client):
    token = begin(client)
    assert post(client, '/quest/clear', {'quest_id': 999, 'token': token}).status_code == 409
    decoded(client, '/quest/fail', {'quest_id': 99999991, 'token': token})
    assert post(client, '/quest/clear', {'quest_id': 99999991, 'token': token}).status_code == 409


def test_concurrent_retries_pay_quest_reward_once(app, client):
    token = begin(client)
    query = {'quest_id': 99999991, 'token': token}
    def clear(_):
        with app.test_client() as own_client: return post(own_client, '/quest/clear', query)
    with ThreadPoolExecutor(max_workers=8) as pool: replies = list(pool.map(clear, range(24)))
    assert all(r.status_code == 200 for r in replies)
    assert len({r.data for r in replies}) == 1
    assert json.loads(snapshot(app)['t_user'])['t_user']['exp'] == 180


def test_gacha_counters_and_new_inventory_are_persistent(app, client, monkeypatch):
    gacha = importlib.import_module('api.gacha')
    # Pick a known draw result missing from the seed to exercise acquisition.
    with app.extensions['store'].transaction() as db:
        units = read_document(db, 't_user_unit_list')
        units['t_user_unit_list'] = [u for u in units['t_user_unit_list'] if u['unit_id'] != 311001001]
        write_document(db, 't_user_unit_list', units)
    monkeypatch.setattr(gacha, 'draw', lambda: [311001001, 3])
    result = decoded(client, '/gacha/draw', PARAMS['/gacha/draw'])
    assert len(result.draw_result_list) == 10
    assert result.t_user_gacha_normal_detail.gacha_detail_id == 30100012
    assert result.t_user_gacha_normal.execution_count == 1
    assert len(result.update_resource_result.replaced_unit_id_list) == 9
    restarted = create_app(dict(app.config))
    listing = decoded(restarted.test_client(), '/gacha/list')
    assert listing.t_user_gacha_normal_list[0].execution_count == 1
    assert post(client, '/gacha/draw', {'detail_id': 9}).status_code == 400


def test_daily_login_state_survives_restart(app, client):
    first = decoded(client, '/mypage/index')
    second = decoded(create_app(dict(app.config)).test_client(), '/mypage/index')
    assert any(b.login_bonus_id == 10000001 for b in first.t_user_login_bonus_list)
    assert len(second.t_user_login_bonus_list) == 0


def test_expeditions_enforce_lifecycle(app, client):
    app.config['SPY_DURATION_SECONDS'] = 3600
    decoded(client, '/spy/start', PARAMS['/spy/start'])
    assert post(client, '/spy/start', PARAMS['/spy/start']).status_code == 409
    assert post(client, '/spy/clear', {'user_spy_id': 1}).status_code == 409
    restarted = create_app(dict(app.config))
    listing = decoded(restarted.test_client(), '/spy/get_list')
    assert listing.t_user_spy_list[0].state == 1
    app.config['SPY_DURATION_SECONDS'] = 0
    result = decoded(client, '/spy/clear', {'user_spy_id': 1})
    assert result.t_user_spy_list[0].state == 2
    assert post(client, '/spy/clear', {'user_spy_id': 1}).status_code == 409


def test_backup_is_consistent_and_never_overwrites(app, client, tmp_path):
    decoded(client, '/user/change_name', {'name': 'Backup name'})
    target = tmp_path / 'backup.sqlite3'
    runner = app.test_cli_runner()
    assert runner.invoke(args=['backup', str(target)]).exit_code == 0
    assert runner.invoke(args=['backup', str(target)]).exit_code != 0
    with sqlite3.connect(target) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        row = db.execute("SELECT value FROM documents WHERE name='t_user'").fetchone()
        assert json.loads(row[0])['t_user']['name'] == 'Backup name'


def test_token_limits_errors_and_static_file_boundaries(app, client, tmp_path):
    app.config['API_TOKEN'] = 'test-secret'
    assert post(client, '/regist/check').status_code == 401
    assert post(client, '/regist/check', headers={'Authorization': 'Bearer test-secret'}).status_code == 200
    assert client.get('/healthz').json['status'] == 'ok'
    assert client.get('/user/change_name').status_code == 405
    assert client.get('/user/change_name').headers['X_RES_STATUS'] == '1'
    assert client.post('/user/unknown').status_code == 404
    assert client.post('/user/unknown').headers['X_RES_STATUS'] == '1'
    assert client.post('/regist/check', data=b'a' * (1024*1024 + 1),
                       headers={'Authorization': 'Bearer test-secret'}).status_code == 413
    directory = Path(app.config['ASSET_DIR']) / 'images'
    directory.mkdir(parents=True)
    (directory / 'sample.txt').write_text('sample')
    assert client.get('/images/sample.txt').data == b'sample'
    assert client.get('/images/../../data/t_user.json').status_code == 404


def test_multiple_worker_processes_do_not_lose_updates(app):
    import subprocess
    import sys
    store = app.extensions['store']
    with store.transaction() as db: write_document(db, 'process_counter', {'value': 0})
    program = '''
import sys
from storage import Store, read_document, write_document
store = Store(sys.argv[1], sys.argv[2])
for _ in range(20):
    with store.transaction() as db:
        data = read_document(db, 'process_counter')
        data['value'] += 1
        write_document(db, 'process_counter', data)
'''
    children = [subprocess.Popen([sys.executable, '-c', program, store.database, app.config['SEED_DIR']],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(4)]
    for child in children:
        output, error = child.communicate(timeout=20)
        assert child.returncode == 0, error.decode()
    with store.transaction() as db: assert read_document(db, 'process_counter')['value'] == 80


def test_new_app_preserves_save_and_rejects_future_schema(app, client):
    decoded(client, '/user/change_name', {'name': 'Keep me'})
    assert decoded(create_app(dict(app.config)).test_client(), '/load/split', {'section': 1}).t_user.name == 'Keep me'
    with sqlite3.connect(app.config['DATABASE']) as db: db.execute('PRAGMA user_version=999')
    with pytest.raises(RuntimeError, match='Unsupported save schema'):
        create_app(dict(app.config))


def test_gacha_effect_keeps_highest_rarity(client, monkeypatch):
    gacha = importlib.import_module('api.gacha')
    draws = iter([[gacha.ssr_chara[0], 3]] + [[gacha.sr_chara[0], 2]] * 9)
    monkeypatch.setattr(gacha, 'draw', lambda: next(draws))
    monkeypatch.setattr(gacha.random, 'randint', lambda low, high: high)
    result = decoded(client, '/gacha/draw', PARAMS['/gacha/draw'])
    assert result.effect_1 == result.effect_2 == 3


def test_vendored_source_bytes_match_pinned_upstream():
    import hashlib
    root = Path(__file__).resolve().parents[1] / 'protocol'
    manifest = json.loads((root / 'UPSTREAM.json').read_text())
    for name, expected in manifest['files'].items():
        data = (root / name).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == expected


def test_app_does_not_depend_on_current_working_directory(app, client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    restarted = create_app(dict(app.config))
    assert decoded(restarted.test_client(), '/load/split', {'section': 1}).t_user.user_id == 1

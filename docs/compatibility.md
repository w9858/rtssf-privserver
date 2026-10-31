# API compatibility and implementation scope

## Wire contract

The 71 routes present in the original server are retained. `/spy/stop` is added.
All game requests/responses use binary Protobuf. Static asset URLs are unchanged.
A request is bounded to 1 MiB. Known game routes validate request decoding even
when the operation is unsupported.

Success: HTTP 200, `Content-Type: application/x-protobuf`, `X_RES_STATUS: 0`.
Errors: HTTP 400/401/404/405/409/413/500/501/503 as appropriate, empty body,
`X_RES_STATUS: 1`, and an ASCII `X_ERROR_MSG`. Game responses also carry
`X_SQLITE_VER: 99`, Unix `X_TIMESTAMP`, and `Cache-Control: no-store`.
There is no common upstream Protobuf error message; HTML error bodies are suppressed.

## Deliberate behavior changes

- Quest clears require the token returned by `/quest/start` or `/quest/start_adv`.
  Completion replies are retained for the most recent 32 runs and can be replayed
  after restart without paying rewards again. Older tokens fail with HTTP 409.
- Every new clear increases the stored clear count. Mission completion never
  regresses. The original sandbox drops now actually update inventory. The mission
  completion reward is granted once when all three missions first become complete.
- Adventure completion increments quest progress. Reading/releasing an archive
  only marks it read and does not fabricate extra quest clears.
- Deck numbers refer to `deck_no`, never Python negative list indices. Invalid
  decks, unknown owned resources and duplicated unit slots fail without changes.
- `home_background_id` is saved under the field the client actually loads.
- Tips and tutorial-how-to-play save repeated messages, not Python integer lists.
- Gacha details are validated; counts and newly acquired units persist. Duplicate
  unit IDs are reported through `replaced_unit_id_list`; no original-game duplicate
  compensation is claimed. Draws remain free with the original 70/20/10 weights.
- Weapon equips are exclusive: moving one weapon removes its earlier assignment.
  Lock state persists. Selling remains unsupported because prices are unavailable.
- Board release retains the original full-sheet-unlock sandbox behavior; it is
  now persisted. This does not implement square costs or original progression.
- Login bonus *display* is persisted per game day. This does not grant undocumented
  original-game rewards. Friend profiles remain synthetic and now have stable IDs.
- Expeditions use persistent state and a one-hour sandbox duration, enforce unit
  exclusivity, and can be stopped. No original reward table is present, so clearing
  changes state without inventing a reward. No multiplayer matchmaking is supplied.
- The original 204 no-op command handlers now return explicit HTTP 501 rather than
  claiming a successful purchase, sale, grant, evolution or account transfer.
  Empty collections are valid typed Protobuf responses.

## Protocol sources

`protocol/*.proto` preserves the exact files pinned in `protocol/UPSTREAM.json`.
The generator overlays `protocol/compat/recipe.proto`: `ResponseCreate`'s
`update_resource_result` field is **1** in the original server's generated code,
but **4** in the separate schema repository. We preserve the server's field 1.
The original compiled descriptors in `tests/fixtures/upstream-descriptors.pb64`
anchor wire compatibility for every message, field number, type and enum.
The schemas describe additional operations beyond the original 71 routes; including
a schema does not mean that its entire service is implemented.

## Endpoint inventory

Every endpoint below is exercised with a valid request and malformed Protobuf.
Status and wire parsing checks are supplemented by stateful tests for profiles,
decks, weapons, quests, gacha, expeditions, login, rollback, concurrency and backup.
“샌드박스 표시 데이터” means a local fixture or simulated catalog, not an online service.

| API | 구현 범위 |
|---|---|
| `/achievement/get_list` | 읽기 전용 / 빈 컬렉션 |
| `/achievement/receive` | 미지원 · HTTP 501 |
| `/achievement/receive_all` | 미지원 · HTTP 501 |
| `/archive/read` | 저장 또는 저장 상태 조회 |
| `/archive/release` | 저장 또는 저장 상태 조회 |
| `/billing/top` | 샌드박스 표시 데이터 |
| `/board/release` | 저장 또는 저장 상태 조회 |
| `/deck/change_name` | 저장 또는 저장 상태 조회 |
| `/deck/save` | 저장 또는 저장 상태 조회 |
| `/eventmap/get` | 샌드박스 표시 데이터 |
| `/exchange/item_list` | 샌드박스 표시 데이터 |
| `/exchange/list` | 샌드박스 표시 데이터 |
| `/friend/delete` | 미지원 · HTTP 501 |
| `/friend/get_list` | 샌드박스 표시 데이터 |
| `/friend/invite` | 미지원 · HTTP 501 |
| `/friend/ng_invite` | 미지원 · HTTP 501 |
| `/friend/ok_invite` | 미지원 · HTTP 501 |
| `/friend/search` | 샌드박스 표시 데이터 |
| `/friend/top` | 샌드박스 표시 데이터 |
| `/gacha/draw` | 저장 또는 저장 상태 조회 |
| `/gacha/list` | 저장 또는 저장 상태 조회 |
| `/gacha/rate_list` | 저장 또는 저장 상태 조회 |
| `/gamecenter/get_list` | 읽기 전용 / 빈 컬렉션 |
| `/help/list` | 샌드박스 표시 데이터 |
| `/information/index` | 저장 또는 저장 상태 조회 |
| `/information/read` | 저장 또는 저장 상태 조회 |
| `/item/sell` | 미지원 · HTTP 501 |
| `/item/stamina_recover` | 읽기 전용 / 빈 컬렉션 |
| `/load/split` | 읽기 전용 / 빈 컬렉션 |
| `/load/sqlite_versions` | 읽기 전용 / 빈 컬렉션 |
| `/mypage/index` | 저장 또는 저장 상태 조회 |
| `/present/get_list` | 읽기 전용 / 빈 컬렉션 |
| `/present/get_received_list` | 읽기 전용 / 빈 컬렉션 |
| `/present/receive` | 미지원 · HTTP 501 |
| `/present/receive_all` | 미지원 · HTTP 501 |
| `/quest/clear` | 저장 또는 저장 상태 조회 |
| `/quest/clear_adv` | 저장 또는 저장 상태 조회 |
| `/quest/continue` | 저장 또는 저장 상태 조회 |
| `/quest/fail` | 저장 또는 저장 상태 조회 |
| `/quest/get_continue_crystal` | 저장 또는 저장 상태 조회 |
| `/quest/retire` | 저장 또는 저장 상태 조회 |
| `/quest/start` | 저장 또는 저장 상태 조회 |
| `/quest/start_adv` | 저장 또는 저장 상태 조회 |
| `/recipe/create` | 미지원 · HTTP 501 |
| `/regist/check` | 읽기 전용 / 빈 컬렉션 |
| `/shop/item_list` | 샌드박스 표시 데이터 |
| `/shop/list` | 샌드박스 표시 데이터 |
| `/spy/clear` | 저장 또는 저장 상태 조회 |
| `/spy/get_list` | 저장 또는 저장 상태 조회 |
| `/spy/start` | 저장 또는 저장 상태 조회 |
| `/spy/stop` | 저장 또는 저장 상태 조회 |
| `/tips/save` | 저장 또는 저장 상태 조회 |
| `/tutorial/adv_clear` | 저장 또는 저장 상태 조회 |
| `/tutorial/adv_start` | 저장 또는 저장 상태 조회 |
| `/tutorial/register_name` | 저장 또는 저장 상태 조회 |
| `/tutorial/update_progress` | 저장 또는 저장 상태 조회 |
| `/tutorialhowtoplay/save` | 저장 또는 저장 상태 조회 |
| `/unit/evolve` | 미지원 · HTTP 501 |
| `/unit/level_up` | 미지원 · HTTP 501 |
| `/user/change_comment` | 저장 또는 저장 상태 조회 |
| `/user/change_emblem` | 저장 또는 저장 상태 조회 |
| `/user/change_friend_unit` | 저장 또는 저장 상태 조회 |
| `/user/change_home_bg` | 저장 또는 저장 상태 조회 |
| `/user/change_home_unit_main` | 저장 또는 저장 상태 조회 |
| `/user/change_home_unit_sub` | 저장 또는 저장 상태 조회 |
| `/user/change_name` | 저장 또는 저장 상태 조회 |
| `/user/get_stamina_recover` | 저장 또는 저장 상태 조회 |
| `/user/set_transfer_password` | 미지원 · HTTP 501 |
| `/user/stamina_recover` | 저장 또는 저장 상태 조회 |
| `/weapon/equip` | 저장 또는 저장 상태 조회 |
| `/weapon/lock` | 저장 또는 저장 상태 조회 |
| `/weapon/sell` | 미지원 · HTTP 501 |

## Validation boundary

Automated tests and a local two-worker Gunicorn HTTP smoke test exercise this
server. No Android APK, device or game asset bundle was supplied; actual client
startup, battle UI, asset version matching, original AES transport and iOS remain
unverified. This is a single-player local server improvement, not a claim of a
complete original service reconstruction.

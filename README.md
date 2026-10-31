# RELEASE THE SPYCE secret fragrance — local server rebuild

기존 `rtssf-privserver`의 Flask/Protobuf API를 유지하면서 저장 안정성, 오류 처리,
프로토콜 검증을 보강한 **로컬 단일 플레이어 서버**입니다.
`rtssf-proto`의 원본 28개 스키마를 `protocol/`에 함께 포함했습니다.

## 실행

Python 3.12 또는 3.13을 사용합니다. 수정된 Android APK와 본인이 보유한 게임
에셋이 별도로 필요합니다. APK·에셋·게임 마스터 DB는 이 저장소에 포함되지 않습니다.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

기본 주소는 `http://127.0.0.1:19212`입니다. 실행 위치와 무관하게 저장소의
`data/`를 초기 데이터로 읽고, `instance/save.sqlite3`에 진행 상황을 저장합니다.
`data/*.json`은 플레이 도중 수정하지 않습니다.

에셋은 다음 디렉터리에 배치합니다.

```text
img/assets/    → /assets/...
img/sqlites/   → /sqlites/...
img/images/    → /images/...
```

다른 에셋 경로는 `RTSSF_ASSET_DIR`로 지정할 수 있습니다.

여러 워커로 실행하려면:

```sh
gunicorn --workers 2 --threads 4 --bind 127.0.0.1:19212 'server:create_app()'
```

모든 워커는 같은 SQLite 파일을 사용합니다. 변경 요청 전체를 하나의 트랜잭션으로
처리하고, 오류 응답 시 변경을 롤백합니다. SQLite는 로컬 디스크에 두세요.

## 구현 범위

| 영역 | 동작 |
|---|---|
| 등록·로드·마이페이지 | 기존 Protobuf 응답과 22개 분할 로드, 재시작 후에도 유지되는 일일 로그인 표시 |
| 프로필·덱·장비 | 입력 검증, 저장, 장비 이동·해제·잠금, 오류 시 전체 변경 취소 |
| 퀘스트 | 실행 토큰, 완료·실패·포기, 누적 클리어·미션 보존, 실제 아이템 반영, 완료 재전송 중복 보상 방지 |
| 가챠 | 기존 무료 1회·10회와 70/20/10 확률 유지, 실행 횟수·유닛 보유 저장 |
| 팁·튜토리얼·아카이브 | 올바른 Protobuf 반복 필드 처리 및 저장 |
| 보드 | 기존 전체 해제 방식 유지 및 선택한 유닛·시트의 상태 저장 |
| 탐색 | 샌드박스 시작·중단·완료 상태 저장, 중복 출전 방지, 기본 대기 1시간, 보상 테이블 없음 |
| 친구·상점·교환·이벤트 | 기존 샌드박스 표시 데이터. 실제 온라인 친구·경제 시스템이 아님 |
| 제작·판매·성장·보상 수령·계정 이전 | 기존 빈 성공 응답을 HTTP 501 미지원 오류로 변경 |

퀘스트 보상, 무료 가챠, 무제한 스태미나 등은 **기존 서버의 샌드박스 규칙**입니다.
원작의 정확한 경제·드롭·성장 규칙을 복원했다는 의미가 아닙니다.
실제 APK와의 연결 검증은 별도로 필요합니다. iOS와 원본 APK의 AES 암호화는 지원하지 않습니다.

자세한 API별 상태와 변경 사항은 [호환성 문서](docs/compatibility.md)를 확인하세요.

## 설정

| 환경 변수 | 기본값 | 설명 |
|---|---|---|
| `RTSSF_DATABASE` | 저장소의 `instance/save.sqlite3` | SQLite 저장 경로 |
| `RTSSF_ASSET_DIR` | 저장소의 `img` | 에셋 루트 |
| `RTSSF_HOST` | `127.0.0.1` | `python app.py`의 바인딩 주소 |
| `RTSSF_PORT` | `19212` | `python app.py`의 포트 |
| `RTSSF_API_TOKEN` | 비어 있음 | 설정하면 게임 API에 `Authorization: Bearer ...` 필요 |
| `RTSSF_GAME_TIMEZONE` | `Asia/Tokyo` | 생일·일일 로그인 기준 시간대 |

토큰 기능은 프록시나 수정 클라이언트가 해당 헤더를 전송할 수 있을 때 사용하세요.
저장 파일 하나가 플레이어 하나이며, 토큰은 여러 사용자 저장 공간을 분리하지 않습니다.
기본 localhost 구성을 기준으로 만들었습니다. 상태 확인은 `GET /healthz`입니다.

## 저장·백업·복원

```sh
flask --app 'server:create_app()' backup ./backups/save-001.sqlite3
```

실행 중에도 SQLite backup API로 일관된 사본을 만듭니다. 기존 파일을 덮어쓰지 않습니다.
복원은 서버를 중지한 뒤, 백업 파일을 새 경로에 복사하고 `RTSSF_DATABASE`를 그 경로로
지정해 재시작합니다. 실행 중인 DB 파일을 직접 교체하지 마세요.
기존 JSON 저장 데이터는 첫 실행 전에 `data/`에 배치하면 최초 1회만 가져옵니다.
이미 생성된 SQLite 데이터는 이후 서버 재시작이나 seed 변경으로 덮어쓰지 않습니다.

Termux 설치 스크립트는 별도 디렉터리를 만들고 기존 체크아웃·저장·압축 파일을 삭제하지 않습니다.
업데이트 전에는 백업하고, 변경 내역을 검토한 뒤 작업 브랜치의 새 커밋을 가져오세요.

## 개발·검증

```sh
python -m pip install -r requirements-dev.txt
python scripts/generate_proto.py
python -m pytest -q
```

원본 71개 API와 추가 탐색 중단 API의 응답·잘못된 패킷 처리, 전체 스키마의
필드 번호·자료형, 저장 재시작, 동시 요청·다중 프로세스, 퀘스트 재전송·롤백,
에셋 경로 경계와 백업을 검사합니다. GitHub Actions에도 같은 검증을 등록했습니다.

## 원본과 프로토콜 출처

- 서버 기준 커밋: `w9858/rtssf-privserver@205a9242ae225fd63363d6a9f813271327b88106`
- 스키마 기준 커밋: `w9858/rtssf-proto@ad71526c110b5a2cb503fff2befc31836fe84ef6`
- `protocol/*.proto`: 위 스키마 저장소 원문
- `protocol/compat/recipe.proto`: 기존 서버 바인딩과의 필드 번호 차이를 보정한 파일
- `proto/*_pb2.py`: 위 입력으로 재생성한 바인딩

`ResponseCreate.update_resource_result`는 스키마 원문에서 필드 4, 기존 서버에서는
필드 1입니다. 이 브랜치는 기존 서버와의 호환성을 위해 필드 1을 사용합니다.
원본 바인딩에서 추출한 descriptor를 테스트에 보존해 무심코 wire 형식을 변경하지 않도록 합니다.

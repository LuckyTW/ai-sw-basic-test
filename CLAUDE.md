# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

PBL(Problem-Based Learning) 교육 후 학습자의 학습 성취도를 자동 채점하는 **pytest 기반 자동 채점 시스템**.
리눅스 시스템 관리, Python 코딩, 자료구조, 알고리즘, 데이터베이스 미션을 지원하며, 새로운 도메인으로 자유롭게 확장 가능.

- **외부 의존성**: pytest 1개만 사용, 나머지는 Python 표준 라이브러리
- **합격 기준**: 70점 이상 Pass
- **미션 자료 일체형**: 문제지, 정답, 템플릿, 테스트를 한 폴더에 관리

---

## 실행 명령어

```bash
# 의존성 설치
pip3 install -r requirements.txt

# 전체 미션 정답 검증 (133개 테스트)
python3 -m pytest missions/ entry/ -v

# 응시자 제출물 채점 (--submission-dir 옵션)
python3 -m pytest missions/python/level1/mission01/tests/ --submission-dir /path/to/submission -v

# 정답 코드로 검증 (기본값 = sample_submission)
python3 -m pytest missions/python/level1/mission01/tests/ -v

# ─── 입학 연수 채점 명령어 ───

# 터미널 기초 - 디렉토리 탐색 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission01/tests/ -v

# Docker 기본 명령어 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission02/tests/ -v

# 터미널 파일 관리 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission03/tests/ -v

# Git 기본 명령어 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission04/tests/ -v

# ─── 입학 연수 Python 코딩 ───

# 미니 펫 시뮬레이터 (난이도 1, 10개 테스트)
python3 -m pytest entry/python/mission01/tests/ -v

# Git 워크플로우 시뮬레이터 (난이도 1, 10개 테스트)
python3 -m pytest entry/python/mission02/tests/ -v

# ─── 미션별 채점 명령어 ───

# Python 도서 관리 시스템 (난이도 1, 17개 테스트)
python3 -m pytest missions/python/level1/mission01/tests/ -v

# Python 서버 로그 분석기 (난이도 1, 7개 테스트)
python3 -m pytest missions/python/level1/mission02/tests/ -v

# Python 프롬프트 관리 프로그램 (난이도 1, 16개 테스트)
python3 -m pytest missions/python/level1/mission03/tests/ -v

# 리눅스 보안 감사 도구 (난이도 2, 7개 테스트)
python3 -m pytest missions/linux/level2/mission01/tests/ -v

# Mini LRU 캐시 (난이도 1, 15개 테스트)
python3 -m pytest missions/ds/level1/mission01/tests/ -v

# Mini Git 커밋 그래프 시뮬레이터 (난이도 2, 16개 테스트)
python3 -m pytest missions/algo/level2/mission01/tests/ -v

# 커밋 이력 DB 분석기 (난이도 3, 19개 테스트)
python3 -m pytest missions/db/level3/mission01/tests/ -v
```

---

## 디렉토리 구조

```
ai-sw-fundamentals/
├── CLAUDE.md                               # 프로젝트 지침서
├── README.md
├── requirements.txt                        # pytest>=7.0
├── conftest.py                             # 루트: --submission-dir 옵션 등록
├── pyproject.toml                          # pytest 설정 (testpaths 등)
│
├── entry/                                  # 입학 연수 시험
│   ├── dev-environment/                    #   [개발 환경] AI/SW 개발 워크스테이션 구축
│       ├── mission01/                      #     터미널 기초 - 디렉토리 탐색
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       answers.py (빈 답안)
│       │   ├── sample_submission/          #       answers.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_terminal_commands.py #     4개 테스트
│       ├── mission02/                      #     Docker 기본 명령어
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       answers.py (빈 답안)
│       │   ├── sample_submission/          #       answers.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_docker_commands.py #       4개 테스트
│       ├── mission03/                      #     터미널 파일 관리
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       answers.py (빈 답안)
│       │   ├── sample_submission/          #       answers.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_file_commands.py   #       4개 테스트
│       └── mission04/                      #     Git 기본 명령어
│           ├── problem.md, solution.md
│           ├── template/                   #       answers.py (빈 답안)
│           ├── sample_submission/          #       answers.py (정답)
│           └── tests/
│               ├── conftest.py
│               └── test_git_commands.py    #       4개 테스트
│   └── python/                             #   [Python 기초] Git과 함께하는 Python 첫 발자국
│       ├── mission01/                      #     미니 펫 시뮬레이터
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       pet_simulator.py (스켈레톤)
│       │   ├── sample_submission/          #       pet_simulator.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_pet_simulator.py   #       10개 테스트
│       └── mission02/                      #     Git 워크플로우 시뮬레이터
│           ├── problem.md, solution.md
│           ├── template/                   #       git_simulator.py (스켈레톤)
│           ├── sample_submission/          #       git_simulator.py (정답)
│           └── tests/
│               ├── conftest.py
│               └── test_git_simulator.py   #       10개 테스트
│
└── missions/
    ├── python/level1/
    │   ├── mission01/                      # Python 도서 관리 시스템
    │   │   ├── problem.md                  #   문제지
    │   │   ├── solution.md                 #   정답지
    │   │   ├── template/                   #   models.py, filters.py, storage.py, cli.py
    │   │   ├── sample_submission/          #   정답 예시 (4파일)
    │   │   └── tests/
    │   │       ├── conftest.py             #   submission_dir fixture
    │   │       └── test_book_manager.py    #   17개 테스트
    │   ├── mission02/                      # 서버 접근 로그 분석기
    │   │   ├── problem.md, solution.md
    │   │   ├── template/                   #   access_log_sample.csv
    │   │   ├── sample_submission/          #   log_analyzer.py
    │   │   └── tests/
    │   │       ├── conftest.py
    │   │       └── test_log_analyzer.py    #   7개 테스트
    │   └── mission03/                      # 프롬프트 관리 프로그램
    │       ├── problem.md, solution.md
    │       ├── template/                   #   prompt_manager.py
    │       ├── sample_submission/
    │       └── tests/
    │           ├── conftest.py
    │           └── test_prompt_manager.py  #   16개 테스트
    ├── linux/level2/mission01/             # 리눅스 서버 보안 감사 도구
    │   ├── problem.md, solution.md
    │   ├── sample_submission/              #   auditor.py
    │   └── tests/
    │       ├── conftest.py
    │       └── test_auditor.py             #   7개 테스트
    ├── ds/level1/mission01/                # Mini LRU 캐시
    │   ├── problem.md, solution.md
    │   ├── template/                       #   lru_cache.py, cli.py
    │   ├── sample_submission/
    │   └── tests/
    │       ├── conftest.py
    │       └── test_mini_redis.py          #   15개 테스트
    ├── algo/level2/mission01/              # Mini Git 커밋 그래프 시뮬레이터
    │   ├── problem.md, solution.md
    │   ├── template/                       #   mini_git.py, cli.py
    │   ├── sample_submission/
    │   └── tests/
    │       ├── conftest.py
    │       └── test_mini_git.py            #   16개 테스트
    └── db/level3/mission01/                # 커밋 이력 DB 분석기
        ├── problem.md, solution.md
        ├── template/                       #   commit_analyzer.py
        ├── sample_submission/
        └── tests/
            ├── conftest.py
            └── test_commit_analyzer.py     #   19개 테스트
```

---

## 아키텍처

### 채점 흐름

```
python3 -m pytest missions/{category}/level{N}/mission{NN}/tests/ --submission-dir /path/to/submission -v
 │
 ├→ conftest.py (루트)         → --submission-dir CLI 옵션 등록
 ├→ tests/conftest.py (미션별) → submission_dir fixture 제공 (기본값: sample_submission/)
 └→ tests/test_*.py            → submission_dir fixture로 제출물 경로 참조
     ├→ AST 분석: 소스코드 구조 검증
     ├→ subprocess.run(): 학생 코드 실행 후 출력 검증
     ├→ subprocess.Popen(): 시간 의존 테스트 (TTL 등)
     └→ sqlite3: DB 쿼리 검증
```

### pytest 제출물 참조 메커니즘

**루트 conftest.py** - `--submission-dir` CLI 옵션 등록:
```python
def pytest_addoption(parser):
    parser.addoption("--submission-dir", action="store", default=None)
```

**미션별 conftest.py** - `submission_dir` session-scoped fixture:
```python
@pytest.fixture(scope="session")
def submission_dir(request):
    cli_value = request.config.getoption("--submission-dir")
    resolved = os.path.abspath(cli_value) if cli_value else _DEFAULT_SUBMISSION
    assert os.path.isdir(resolved)
    return resolved
```

**테스트 파일** - fixture 기반 제출물 참조:
```python
@pytest.fixture(scope="module")
def report_content(tmp_path_factory, submission_dir):
    script_path = os.path.join(submission_dir, "my_script.py")
    # subprocess.run으로 학생 코드 실행 후 검증
```

### 테스트 패턴

| 패턴 | 설명 | 사용 미션 |
|------|------|---------|
| **AST 분석형** | `ast` 모듈로 소스코드 구문 분석 | Python M1, DS, Algo |
| **subprocess 실행형** | `subprocess.run()`으로 학생 코드 실행 후 출력 검증 | 전체 |
| **파일 I/O형** | `tempfile`로 임시 환경 구성 | Python M1/M2, Linux, DB |
| **Popen형** | `subprocess.Popen()` + `time.sleep()`으로 시간 의존 테스트 | DS (TTL 만료) |
| **DB 쿼리형** | `sqlite3` 직접 연결하여 메타데이터 쿼리 | DB |

### 다중 파일 미션 처리

다중 파일 제출 미션(python_mission01, ds_mission01, algo_mission01)은 모듈 수준 글로벌 변수 패턴을 사용.

```python
_SUBMISSION_DIR = ""  # autouse fixture가 설정

@pytest.fixture(autouse=True, scope="module")
def _set_submission_dir(submission_dir):
    global _SUBMISSION_DIR
    _SUBMISSION_DIR = submission_dir
```

- **python_mission01** (4파일): `_import_module("models")`, `_import_module("filters")`, `_import_module("storage")` 개별 import + `cli.py` subprocess 실행
- **ds_mission01** (2파일): `lru_cache.py` AST 분석 + `cli.py` subprocess REPL
- **algo_mission01** (2파일): `mini_git.py` AST 분석 + `cli.py` subprocess REPL

---

## 미션 목록

### 입학 연수

#### entry_mission01 - 터미널 기초: 디렉토리 탐색

- **난이도**: 1 | **권장 시간**: 5분 | **합격**: 100점 (4개 전체)
- **제출물**: answers.py (1파일)
- **정답 예시**: `entry/dev-environment/mission01/sample_submission/`
- **검증 방식**: `importlib`로 answers dict 로드 → 정규화 후 허용 목록 매칭

| 테스트 (총 4개) | AI 트랩 |
|-----------------|--------|
| q1_pwd, q2_mkdir, q3_cd, q4_ls | 없음 |

---

#### entry_mission02 - Docker 기본 명령어

- **난이도**: 1 | **권장 시간**: 5분 | **합격**: 100점 (4개 전체)
- **제출물**: answers.py (1파일)
- **정답 예시**: `entry/dev-environment/mission02/sample_submission/`
- **검증 방식**: `importlib`로 answers dict 로드 → 정규화 후 허용 목록 매칭

| 테스트 (총 4개) | AI 트랩 |
|-----------------|--------|
| q1_version, q2_pull, q3_images, q4_ps | 없음 |

---

#### entry_mission03 - 터미널 파일 관리

- **난이도**: 1 | **권장 시간**: 5분 | **합격**: 100점 (4개 전체)
- **제출물**: answers.py (1파일)
- **정답 예시**: `entry/dev-environment/mission03/sample_submission/`
- **검증 방식**: `importlib`로 answers dict 로드 → 정규화 후 허용 목록 매칭

| 테스트 (총 4개) | AI 트랩 |
|-----------------|--------|
| q1_touch, q2_cat, q3_cp, q4_rm | 없음 |

---

#### entry_mission04 - Git 기본 명령어

- **난이도**: 1 | **권장 시간**: 5분 | **합격**: 100점 (4개 전체)
- **제출물**: answers.py (1파일)
- **정답 예시**: `entry/dev-environment/mission04/sample_submission/`
- **검증 방식**: `importlib`로 answers dict 로드 → 정규화 후 허용 목록 매칭

| 테스트 (총 4개) | AI 트랩 |
|-----------------|--------|
| q1_init, q2_add, q3_status, q4_log | 없음 |

---

#### entry_python_mission01 - 미니 펫 시뮬레이터

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 100점 (10개 전체)
- **제출물**: pet_simulator.py (1파일)
- **정답 예시**: `entry/python/mission01/sample_submission/`
- **검증 방식**: AST 구조 분석 + `importlib`로 모듈 import 후 기능 검증

| 테스트 클래스 | 테스트 (총 10개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestStructure` | classes_exist, no_external_lib | |
| `TestPet` | pet_init, feed, play, status | |
| `TestPetShop` | shop_add_find, hungry_pets, to_dict_list | |
| `TestFunction` | summarize | |

---

#### entry_python_mission02 - Git 워크플로우 시뮬레이터

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 100점 (10개 전체)
- **제출물**: git_simulator.py (1파일)
- **정답 예시**: `entry/python/mission02/sample_submission/`
- **검증 방식**: AST 구조 분석 + `importlib`로 모듈 import 후 기능 검증
- **출제 형식**: 빈칸 채우기 - `__init__`, `log`, `create_branch`, `switch`, `summarize`는 제공, 학생은 **`add`, `commit`, `status`** 3개 메서드만 구현

| 테스트 클래스 | 테스트 (총 10개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestStructure` | class_exists, no_external_lib | |
| `TestGitBasic` | init, add, commit, log | |
| `TestBranch` | create_branch, switch, status | |
| `TestFunction` | summarize | |

---

### python_level1_mission01 - Python 도서 관리 시스템 코딩 시험

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + tmpdir 기반)
- **제출물**: models.py, filters.py, storage.py, cli.py (4파일)
- **정답 예시**: `missions/python/level1/mission01/sample_submission/`

| 테스트 클래스 | 테스트 (총 17개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestModelValidator` | model_dataclass, model_fields, model_type_hints, model_post_init | |
| `TestPatternValidator` | pattern_yield, pattern_decorator, pattern_type_hints, pattern_no_any | yield, no_any |
| `TestCLIValidator` | cli_runnable, cli_help, cli_add, cli_list, cli_no_crash | cli_help |
| `TestPersistenceValidator` | persist_roundtrip, persist_format, persist_no_pickle, persist_integrity | no_pickle |

**AI 트랩 포인트** (4개):
- `pattern_yield`: yield 없이 리스트 반환하는 실수
- `pattern_no_any`: `Any` 타입 30% 이상 남용
- `cli_help`: `--help` 옵션 미구현
- `persist_no_pickle`: pickle 사용 (보안 취약)

---

### python_level1_mission02 - 서버 접근 로그 분석기

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + tmpdir 기반)
- **제출물**: log_analyzer.py (1파일)
- **정답 예시**: `missions/python/level1/mission02/sample_submission/`
- **샘플 데이터**: `missions/python/level1/mission02/template/access_log_sample.csv`

| 테스트 (총 7개) | AI 트랩 |
|-----------------|--------|
| csv_parse, top_ips, ip_order, status_ratio, slow_order, report_sections, slow_values | ip_order, status_ratio, slow_values |

**AI 트랩 포인트** (3개):
- `ip_order`: 동점 IP를 오름차순 정렬 → 정답은 내림차순
- `status_ratio`: 1xx 상태코드를 무시하여 리포트에 1xx 비율이 누락
- `slow_values`: response_time 소수점(33.7)을 정수 처리하여 평균 오차 발생

---

### python_level1_mission03 - 프롬프트 관리 프로그램

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + stdin 기반)
- **제출물**: prompt_manager.py (1파일)
- **정답 예시**: `missions/python/level1/mission03/sample_submission/`

| 테스트 (총 16개) | AI 트랩 |
|-----------------|--------|
| func_separation, data_structure, initial_data, no_external_lib, menu_display, add_prompt, list_prompts, category_filter, search_title, search_content, add_validation, detail_view, favorite_toggle, favorite_list, invalid_input, exit_message | search_content, add_validation, favorite_toggle |

**AI 트랩 포인트** (3개):
- `search_content`: 제목만 검색, 내용(content) 미포함
- `add_validation`: 빈 제목 입력 시 검증 없이 추가
- `favorite_toggle`: 즐겨찾기 추가만 가능, 해제(토글) 미구현

---

### linux_level2_mission01 - 리눅스 서버 보안 감사 도구

- **난이도**: 2 | **권장 시간**: 25분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + tmpdir 기반)
- **제출물**: auditor.py (1파일)
- **정답 예시**: `missions/linux/level2/mission01/sample_submission/`

| 테스트 (총 7개) | AI 트랩 |
|-----------------|--------|
| config_parse, ssh_audit, firewall_audit, account_audit, permission_audit, log_stats, report_sections | ssh_audit, firewall_audit, account_audit, permission_audit |

**AI 트랩 포인트** (4개):
- `ssh_audit`: PermitRootLogin `prohibit-password`를 "안전"으로 오판 → 정답은 `no`만 안전
- `firewall_audit`: 23/tcp(Telnet) 위험 포트 미탐지
- `account_audit`: agent-test의 agent-core 그룹 포함 RBAC 위반 미탐지
- `permission_audit`: api_keys 디렉토리 775+agent-common 권한 위반 미탐지

**검증 방식**: 라인 기반 매칭 (해당 토픽 라인에서만 취약 키워드 확인, 타 섹션 간 오염 방지)

---

### ds_level1_mission01 - Mini LRU 캐시 구현 시험

- **난이도**: 1 | **권장 시간**: 15분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + Popen 기반)
- **제출물**: lru_cache.py, cli.py (2파일)
- **정답 예시**: `missions/ds/level1/mission01/sample_submission/`

| 테스트 클래스 | 테스트 (총 15개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestStructure` | node_class, no_builtin_cache, linked_list_ops | no_builtin_cache |
| `TestBasicCommand` | cli_runnable, set_get, del_command, exists_dbsize, output_format | output_format |
| `TestLRU` | config_maxmemory, lru_eviction, lru_get_refresh, info_memory | lru_get_refresh |
| `TestTTL` | expire_ttl_basic, ttl_expired_get, ttl_nonexistent | ttl_expired_get |

**AI 트랩 포인트** (4개):
- `no_builtin_cache`: OrderedDict/deque/functools.lru_cache 사용 → Node 직접 구현 필요
- `output_format`: Python `True`/`None` 출력 → Redis 형식 `OK`/`(nil)`/`"value"` 필요
- `lru_get_refresh`: SET만 LRU 갱신, GET은 조회만 → GET도 move_to_front 필수
- `ttl_expired_get`: 별도 타이머/스레드 TTL → GET 시 lazy deletion 필요

---

### algo_level2_mission01 - Mini Git 커밋 그래프 시뮬레이터

- **난이도**: 2 | **권장 시간**: 25분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess.run 기반)
- **제출물**: mini_git.py, cli.py (2파일)
- **정답 예시**: `missions/algo/level2/mission01/sample_submission/`

| 테스트 클래스 | 테스트 (총 16개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestStructure` | commit_class, no_builtin_sort, graph_structure | no_builtin_sort |
| `TestBasicCommand` | cli_runnable, init_command, commit_basic, branch_switch | |
| `TestGraphAlgorithm` | commit_parent_after_switch, log_all_branches, path_same_branch, path_cross_branch, ancestors_complete | commit_parent, log_all_branches, path_cross_branch |
| `TestSearchSort` | search_keyword, search_no_result, search_author, sort_by_date | |

**AI 트랩 포인트** (4개):
- `no_builtin_sort`: sorted()/list.sort()/heapq 사용 → merge sort 직접 구현 필요
- `commit_parent_after_switch`: SWITCH 후 전역 "마지막 커밋"을 부모로 설정 → HEAD 브랜치의 최신 커밋이 부모
- `log_all_branches`: 현재 브랜치만 출력 → 저장소의 모든 커밋을 시간순 출력
- `path_cross_branch`: 부모 방향으로만 BFS → DAG를 무방향 그래프로 취급하여 BFS

**설계 특이사항**:
- 테스트 독립성: `path_same_branch`는 독립 세션(선형 체인)으로 테스트하여 `commit_parent` 트랩에 의한 연쇄 실패 방지
- 결정적 해시: `generate_hash(message, seq)` 함수를 템플릿에 제공하여 테스트가 해시값 사전 계산 가능

---

### db_level3_mission01 - 커밋 이력 DB 분석기

- **난이도**: 3 | **권장 시간**: 40분 | **합격**: 70점
- **실행 환경**: macOS/Linux (subprocess + tmpdir 기반)
- **제출물**: commit_analyzer.py (1파일)
- **정답 예시**: `missions/db/level3/mission01/sample_submission/`

| 테스트 클래스 | 테스트 (총 19개) | AI 트랩 |
|-------------|-----------------|--------|
| `TestSchema` | db_created, foreign_keys, root_commit_null, data_loaded, index_exists | root_commit_null |
| `TestAnalysis` | author_commit_count, author_left_join, branch_commit_count, branch_no_commits, distinct_file_count, most_changed_files, self_join_parent, history_count | author_left_join, branch_no_commits, distinct_file_count, self_join_parent |
| `TestReport` | report_created, report_sections, top_author, commit_total, summary_stats, file_ranking_order | |

**AI 트랩 포인트** (5개):
- `root_commit_null`: parent_hash를 NOT NULL로 정의 → root commit INSERT 실패
- `author_left_join`: INNER JOIN으로 커밋 없는 작성자(황서진) 제외
- `branch_no_commits`: INNER JOIN으로 커밋 없는 브랜치(hotfix/urgent) 제외
- `distinct_file_count`: COUNT(*)로 중복 파일을 별도 카운트 → COUNT(DISTINCT file_path) 필요
- `self_join_parent`: INNER JOIN self-reference → parent=NULL인 root commit 제외

**미션 융합 매핑**:
- **DB 미션** (핵심): 4테이블 스키마, PK/FK, JOIN, GROUP BY, 서브쿼리, 인덱스
- **Algo M1** (Mini Git): 커밋 그래프 DAG, 브랜치, self-referencing FK
- **Python M2** (로그 분석): CSV 파싱, 집계, Top-N, 텍스트 리포트

---

## 시험 문제 출제 가이드 (코디세이 시험 가이드 v1.1 기반)

> 새 미션 문제를 제작할 때 반드시 아래 원칙과 템플릿을 따라야 한다.

### 핵심 설계 원칙

1. **AI 활용 전제**: 시험은 인터넷 연결 환경에서 진행되며, ChatGPT/Claude 등 상용 AI 서비스 자유 이용 가능
2. **AI만으로는 불합격**: LLM에 문제를 넣었을 때 한 번에 정답이 나오지 않아야 함
3. **검토, 고도화 능력 평가**: AI가 만든 결과물을 학습자가 검토하고 수정, 고도화하여 체크리스트를 전부 통과하는 것이 핵심
4. **유출 전제 설계**: 문항은 학습자 사이에 공유될 것을 전제로, 단순 암기가 아닌 원리 이해 기반의 응용력을 평가
5. **미션 융합 출제**: 하나의 문항에 여러 미션의 개념이 융합, 교차 (문항 ↔ 특정 미션 1:1 매핑 금지)

### 난이도 체계 (5문항 / 총 120분)

| 문항 | 난이도 | 권장 시간 | 성격 |
|------|--------|----------|------|
| 1번 | 1 | 15분 | 기본기 확인 + 워밍업. AI가 거의 바로 풀어주지만, 학습자가 의도, 결과 검증에 충실해야 함 |
| 2번 | 1 | 15분 | 기본기 확인. 학습 자체를 안 했으면 못 푸는 수준 |
| 3번 | 2 | 25분 | 응용. 여러 개념 조합, 미션 내용의 변형/확장. AI가 50~70% 수준의 답을 주므로 학습자가 심도있게 검토, 수정 필요. **엣지 케이스, 제약 조건을 꼼꼼히 넣어서 AI 출력물을 그대로 제출하면 Fail** |
| 4번 | 2 | 25분 | 응용 (3번과 동급). 엣지 케이스, 제약 조건 포함 |
| 5번 | 3 | 40분 | 심화 통합. 여러 미션을 아우르는 복합 문제. AI가 부분적으로만 도움 → 학습자가 직접 설계, 통합. AI 결과물을 조합, 고도화해야 Pass |

### 시험 운영 규칙

| 항목 | 내용 |
|------|------|
| 장소 | 오프라인 시험장 |
| 시간 | 최대 2시간 (120분) |
| 문항 수 | 시험당 최대 5문항 |
| 제출 | 문제당 1회만 제출 가능 |
| 합격 조건 | 5문항 All Pass |
| 탈락 시 | 문제 Fail → 즉시 시험 Fail, 다음 문제 진행 불가, 1주일간 재응시 불가 |
| 결과 표시 | Pass/Fail만 표시, 체크 항목 통과/실패 여부 비공개 |
| 채점 방식 | pytest 기반 자동 채점 (`pytest --submission-dir /path/to/submission -v`) |
| 라이브러리 | 각자 알아서 설치 (문제별 제약에 따름) |

### 적용 과정

**AI 올인원** (총 5회 시험):

| 시점 | 시험 범위 | 대상 미션 수 | 문항 수 |
|------|----------|-------------|---------|
| 입학 연수 1 | 미션 1 | 1 | - |
| 입학 연수 2 | 미션 2 | 1 | - |
| 입학 연수 3 | 미션 3 | 1 | - |
| AI/SW 기초 | 미션 4~16 (필수 10개) | 10 | 5 |
| AI/SW 심화 | 미션 17~26 중 도메인별 2개 | 8 | 5 |

**AI 네이티브** (총 2회 시험):

| 시점 | 시험 범위 | 문항 수 |
|------|----------|---------|
| AI 도구 학습 | 미션 1~3 | - |
| AI 활용 학습 | 미션 4~6 | 5 |

### 문항 3종 세트 템플릿

모든 문항은 **문제지 + 정답지 + 검증지** 3종 세트로 구성해야 한다.

#### 1. 문제지 (학습자 배포용) → `problem.md`

```markdown
## 문항 [번호]: [문항 제목]

### 시험 정보
- 과정: [AI 올인원 / AI 네이티브]
- 단계: [입학연수 / AI/SW 기초 / AI/SW 심화 / AI 도구 학습 / AI 활용 학습]
- 난이도: [1 / 2 / 3]
- 권장 시간: [분]
- Pass 기준: 정답 체크리스트 [N]개 중 [M]개 이상 충족

### 문제
[문제 상황 및 요구사항을 구체적으로 서술]

### 제약 사항
- [제약 1]
- [제약 2]

### 입력 형식
[입력 데이터의 형식, 파일명, 구조 등]

### 출력 형식
[기대 출력의 형식, 파일명, 구조 등]

### 제출 방식
[제출할 파일 또는 결과물 명시]
```

#### 2. 정답지 (출제자 보관용, 비공개) → `solution.md`

```markdown
## 문항 [번호] 정답지

### 정답 코드
[모범 정답 코드 전문]

### 정답 체크리스트
| 번호 | 체크 항목 | 배점 | 검증 방법 |
|------|----------|------|----------|
| 1 | [체크 항목 1] | [점수] | [자동 / 수동] |
| 2 | [체크 항목 2] | [점수] | [자동 / 수동] |

- Pass 기준: 총 [N]점 중 [M]점 이상
```

#### 3. 검증지 (채점 시스템용) → `tests/conftest.py` + `tests/test_*.py`

```markdown
## 문항 [번호] 검증지

### 검증 환경
- 실행 환경: Python 3.10+
- 필요 패키지: pytest>=7.0

### 검증 코드
tests/conftest.py - submission_dir fixture 제공
tests/test_*.py - pytest 테스트 (AST 분석 + subprocess 실행)

### 실행 방법
python3 -m pytest missions/{category}/level{N}/mission{NN}/tests/ --submission-dir /path/to/submission -v

### 예상 출력 (정답 기준)
python3 -m pytest missions/{category}/level{N}/mission{NN}/tests/ -v → 전체 PASS
```

### AI 트랩 설계 가이드

AI 트랩은 **AI가 흔히 범하는 실수를 의도적으로 유도하는 채점 항목**으로, 학습자의 검토, 수정 능력을 평가하는 핵심 장치다.

**효과적인 AI 트랩 유형**:
- **엣지 케이스 함정**: 빈 값, 경계값, 소수점 등 AI가 간과하는 데이터 (예: 빈 IP, 소수점 응답시간)
- **정렬/순서 함정**: AI가 기본 정렬을 사용하지만 문제는 역순을 요구 (예: 동점 IP 내림차순)
- **보안/관례 함정**: AI가 '일반적'인 답을 주지만 문제는 엄격한 답을 요구 (예: `prohibit-password` vs `no`)
- **패턴 강제 함정**: 특정 구현 패턴을 요구하지만 AI가 다른 패턴 사용 (예: yield 대신 리스트, pickle 사용)
- **JOIN/집계 함정**: SQL JOIN 유형이나 집계 함수 오용 (예: INNER→LEFT JOIN, COUNT(*)→DISTINCT)

**AI 트랩 배치 원칙**:
- 난이도 2~3 문항에 집중 배치
- 문항당 2~4개의 AI 트랩 포함 권장
- 테스트 함수명에 트랩 의도 반영 (예: `test_ip_order`, `test_no_builtin_sort`)

### 문항 개발 운영 사항

- 대표 문항 개발 후, 동일 구조, 다른 데이터/시나리오의 **변형 문항**을 다수 확보 (유출 대비)
- 객관식은 정확히 떨어지는 정답이 없는 경우에만 허용 (재단 검토 필수, AI 네이티브 한정)
- "Exam"이라는 용어 사용 금지 → "시험", "시험 평가", "Test"만 사용

---

## 새 미션 추가 방법

### 1. 미션 디렉토리 생성

```bash
mkdir -p missions/{category}/level{N}/mission{NN}/{template,sample_submission,tests}
```

### 2. 미션 파일 작성

| 파일 | 용도 |
|------|------|
| `problem.md` | 학생용 문제지 |
| `solution.md` | 모범 답안 |
| `template/` | (선택) 학생 배포용 스켈레톤 코드 |
| `sample_submission/` | 정답 예시 코드 |

### 3. 테스트 작성

`tests/conftest.py` - submission_dir fixture:

```python
import os, pytest

_MISSION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_SUBMISSION = os.path.join(_MISSION_DIR, "sample_submission")

@pytest.fixture(scope="session")
def submission_dir(request):
    cli_value = request.config.getoption("--submission-dir")
    resolved = os.path.abspath(cli_value) if cli_value else _DEFAULT_SUBMISSION
    assert os.path.isdir(resolved), f"제출물 디렉토리 없음: {resolved}"
    return resolved
```

`tests/test_*.py` - 테스트 파일에서 submission_dir 사용.

```python
@pytest.fixture(scope="module")
def report_content(tmp_path_factory, submission_dir):
    script_path = os.path.join(submission_dir, "my_script.py")
    # subprocess.run으로 학생 코드 실행 후 검증
    ...
```

### 4. 정답으로 검증

```bash
python3 -m pytest missions/{category}/level{N}/mission{NN}/tests/ -v
# → 전체 PASS 확인
```

---

## 코딩 컨벤션

- **언어**: 코드 변수/함수명은 영어(snake_case), 문서/주석/커밋은 한국어
- **의존성**: pytest 외에는 Python 표준 라이브러리만 사용 (`ast`, `subprocess`, `importlib`, `os`, `json`, `csv`, `pathlib`, `dataclasses`, `abc`, `inspect`, `tempfile`, `sqlite3`, `re`, `hashlib`)
- **subprocess 호출**: 5~10초 타임아웃 적용
- **크로스 플랫폼**: 모든 미션이 macOS/Linux에서 동작 (subprocess + tmpdir 기반)

---

## 현재 프로젝트 현황

| 구분 | 수치 |
|------|------|
| 총 미션 수 | 13개 (입학연수 6, Linux 1, Python 3, DS 1, Algo 1, DB 1) |
| 총 테스트 수 | 133개 |
| 총 AI 트랩 항목 | 27개 |

| 미션 ID | 카테고리 | 난이도 | 시간 | 테스트 수 | AI 트랩 | 제출물 |
|---------|---------|--------|------|----------|---------|--------|
| `entry_mission01` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission02` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission03` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission04` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_python_mission01` | 입학연수 | 1 | 15분 | 10 | 0 | pet_simulator.py |
| `entry_python_mission02` | 입학연수 | 1 | 15분 | 10 | 0 | git_simulator.py |
| `python_level1_mission01` | Python | 1 | 15분 | 17 | 4 | models.py, filters.py, storage.py, cli.py |
| `python_level1_mission02` | Python | 1 | 15분 | 7 | 3 | log_analyzer.py |
| `python_level1_mission03` | Python | 1 | 15분 | 16 | 3 | prompt_manager.py |
| `linux_level2_mission01` | Linux | 2 | 25분 | 7 | 4 | auditor.py |
| `ds_level1_mission01` | 자료구조 | 1 | 15분 | 15 | 4 | lru_cache.py, cli.py |
| `algo_level2_mission01` | 알고리즘 | 2 | 25분 | 16 | 4 | mini_git.py, cli.py |
| `db_level3_mission01` | 데이터베이스 | 3 | 40분 | 19 | 5 | commit_analyzer.py |

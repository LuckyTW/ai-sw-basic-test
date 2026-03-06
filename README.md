# 코디세이 시험 자동 채점 시스템

PBL 교육 후 학습 성취도를 측정하는 **pytest 기반 자동 채점 시스템**

---

## 개요

이 시스템은 **코디세이** PBL 교육 과정을 완료한 학습자의 실습 성취도를 자동으로 채점합니다.
리눅스 시스템 관리, Python 코딩, 자료구조, 알고리즘, 데이터베이스 등 다양한 미션 카테고리를 지원하며,
새로운 도메인으로 자유롭게 확장할 수 있습니다.

### 주요 특징

- **pytest 기반** - 표준 pytest로 채점, 별도 프레임워크 없이 `pytest` 명령 하나로 실행
- **미션 자료 일체형** - 문제지, 정답, 템플릿, 테스트를 한 폴더에 관리
- **AI 트랩 요소** - 학습자가 AI 도구에 의존하지 않고 핵심 개념을 이해했는지 검증
- **크로스 플랫폼** - 모든 미션이 macOS/Linux에서 동작 (subprocess + tmpdir 기반)
- **최소 의존성** - pytest 1개만 사용

### 프로젝트 현황

| 구분 | 수치 |
|------|------|
| 총 미션 수 | 14개 (입학연수 8, Linux 1, Python 2, DS 1, Algo 1, DB 1) |
| 총 테스트 수 | 137개 |
| 총 AI 트랩 항목 | 27개 |

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
│       ├── mission01/                      #     Git 브랜치 워크플로우
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       answers.py (빈 답안)
│       │   ├── sample_submission/          #       answers.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_git_branch.py      #       4개 테스트
│       ├── mission02/                      #     미니 펫 시뮬레이터
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       pet_simulator.py (스켈레톤)
│       │   ├── sample_submission/          #       pet_simulator.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_pet_simulator.py   #       10개 테스트
│       ├── mission03/                      #     Git 워크플로우 시뮬레이터
│       │   ├── problem.md, solution.md
│       │   ├── template/                   #       git_simulator.py (스켈레톤)
│       │   ├── sample_submission/          #       git_simulator.py (정답)
│       │   └── tests/
│       │       ├── conftest.py
│       │       └── test_git_simulator.py   #       10개 테스트
│       └── mission04/                      #     프롬프트 관리 프로그램
│           ├── problem.md, solution.md
│           ├── template/                   #       prompt_manager.py (스켈레톤)
│           ├── sample_submission/          #       prompt_manager.py (정답)
│           └── tests/
│               ├── conftest.py
│               └── test_prompt_manager.py  #       16개 테스트
│
└── missions/
    ├── python/level1/
    │   ├── mission01/                      # Python 도서 관리 시스템
    │   │   ├── problem.md                  #   문제지
    │   │   ├── solution.md                 #   정답지
    │   │   ├── template/                   #   book_manager.py
    │   │   ├── sample_submission/          #   정답 예시 (1파일)
    │   │   └── tests/
    │   │       ├── conftest.py             #   submission_dir fixture
    │   │       └── test_book_manager.py    #   17개 테스트
    │   └── mission02/                      # 서버 접근 로그 분석기
    │       ├── problem.md, solution.md
    │       ├── template/                   #   access_log_sample.csv
    │       ├── sample_submission/          #   log_analyzer.py
    │       └── tests/
    │           ├── conftest.py
    │           └── test_log_analyzer.py    #   7개 테스트
    ├── linux/level2/mission01/             # 리눅스 서버 보안 감사 도구
    │   ├── problem.md, solution.md
    │   ├── sample_submission/              #   auditor.py
    │   └── tests/
    │       ├── conftest.py
    │       └── test_auditor.py             #   7개 테스트
    ├── ds/level1/mission01/                # Mini LRU 캐시
    │   ├── problem.md, solution.md
    │   ├── template/                       #   lru_cache.py
    │   ├── sample_submission/
    │   └── tests/
    │       ├── conftest.py
    │       └── test_mini_redis.py          #   15개 테스트
    ├── algo/level2/mission01/              # Mini Git 커밋 그래프 시뮬레이터
    │   ├── problem.md, solution.md
    │   ├── template/                       #   mini_git.py
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

## 빠른 시작

### 1. 의존성 설치

```bash
pip3 install -r requirements.txt
```

### 2. 채점 실행

```bash
# 응시자 제출물 채점
python3 -m pytest missions/python/level1/mission01/tests/ --submission-dir /path/to/submission -v

# 정답 코드로 검증 (기본값 = sample_submission)
python3 -m pytest missions/python/level1/mission01/tests/ -v

# 전체 미션 정답 검증 (137개 테스트)
python3 -m pytest missions/ entry/ -v
```

### 3. 미션별 채점 명령어

```bash
# ─── 입학 연수 ───

# 터미널 기초 - 디렉토리 탐색 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission01/tests/ -v

# Docker 기본 명령어 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission02/tests/ -v

# 터미널 파일 관리 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission03/tests/ -v

# Git 기본 명령어 (난이도 1, 4개 테스트)
python3 -m pytest entry/dev-environment/mission04/tests/ -v

# ─── 입학 연수 Python 코딩 ───

# Git 브랜치 워크플로우 (난이도 1, 4개 테스트)
python3 -m pytest entry/python/mission01/tests/ -v

# 미니 펫 시뮬레이터 (난이도 1, 10개 테스트)
python3 -m pytest entry/python/mission02/tests/ -v

# Git 워크플로우 시뮬레이터 (난이도 1, 10개 테스트)
python3 -m pytest entry/python/mission03/tests/ -v

# 프롬프트 관리 프로그램 (난이도 1, 16개 테스트)
python3 -m pytest entry/python/mission04/tests/ -v

# ─── missions ───

# Python 도서 관리 시스템 (난이도 1, 17개 테스트)
python3 -m pytest missions/python/level1/mission01/tests/ -v

# Python 서버 로그 분석기 (난이도 1, 7개 테스트)
python3 -m pytest missions/python/level1/mission02/tests/ -v

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

## 채점 메커니즘

### pytest 제출물 참조

```
conftest.py (루트)           → --submission-dir CLI 옵션 등록
missions/*/tests/conftest.py → submission_dir fixture 제공 (기본값: sample_submission/)
missions/*/tests/test_*.py   → submission_dir fixture로 제출물 경로 참조
```

- `--submission-dir` 미지정 시 해당 미션의 `sample_submission/` 디렉토리를 기본값으로 사용
- 테스트는 subprocess로 학생 코드를 실행하거나, AST 분석/모듈 import로 코드 구조를 검증

### 테스트 패턴

| 패턴 | 설명 | 사용 미션 |
|------|------|---------|
| **AST 분석형** | `ast` 모듈로 소스코드 구문 분석 | Python M1, DS, Algo |
| **subprocess 실행형** | `subprocess.run()`으로 학생 코드 실행 후 출력 검증 | 전체 |
| **파일 I/O형** | `tempfile`로 임시 환경 구성 | Python M1/M2, Linux, DB |
| **Popen형** | `subprocess.Popen()` + `time.sleep()`으로 시간 의존 테스트 | DS (TTL 만료) |
| **DB 쿼리형** | `sqlite3` 직접 연결하여 메타데이터 쿼리 | DB |

---

## 구현된 미션 목록

| 미션 ID | 카테고리 | 난이도 | 시간 | 테스트 수 | AI 트랩 | 제출물 |
|---------|---------|--------|------|----------|---------|--------|
| `entry_mission01` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission02` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission03` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_mission04` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_python_mission01` | 입학연수 | 1 | 5분 | 4 | 0 | answers.py |
| `entry_python_mission02` | 입학연수 | 1 | 15분 | 10 | 0 | pet_simulator.py |
| `entry_python_mission03` | 입학연수 | 1 | 15분 | 10 | 0 | git_simulator.py |
| `entry_python_mission04` | 입학연수 | 1 | 15분 | 16 | 3 | prompt_manager.py |
| `python_level1_mission01` | Python | 1 | 15분 | 17 | 4 | book_manager.py |
| `python_level1_mission02` | Python | 1 | 15분 | 7 | 3 | log_analyzer.py |
| `linux_level2_mission01` | Linux | 2 | 25분 | 7 | 4 | auditor.py |
| `ds_level1_mission01` | 자료구조 | 1 | 15분 | 15 | 4 | lru_cache.py |
| `algo_level2_mission01` | 알고리즘 | 2 | 25분 | 16 | 4 | mini_git.py |
| `db_level3_mission01` | 데이터베이스 | 3 | 40분 | 19 | 5 | commit_analyzer.py |

---

## AI 트랩 설계 철학

AI 트랩은 **AI가 흔히 범하는 실수를 의도적으로 유도하는 채점 항목**입니다.
학습자가 AI 도구의 출력물을 그대로 제출하면 Fail, 검토, 수정하면 Pass되도록 설계됩니다.

| 유형 | 설명 | 예시 |
|------|------|------|
| **엣지 케이스** | 빈 값, 경계값, 소수점 등 AI가 간과 | 소수점 응답시간, 0건 작성자 |
| **정렬/순서** | AI가 기본 정렬을 사용하지만 문제는 역순 요구 | 동점 IP 내림차순 |
| **보안/관례** | AI가 '일반적'인 답을 주지만 문제는 엄격한 답 요구 | `prohibit-password` vs `no` |
| **패턴 강제** | 특정 구현 패턴 요구 vs AI의 다른 패턴 사용 | yield 강제, pickle 금지 |
| **JOIN/집계** | SQL JOIN 유형이나 집계 함수 오용 | INNER→LEFT JOIN, COUNT(*)→DISTINCT |

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

## 기술 스택

| 항목 | 상세 |
|------|------|
| 언어 | Python 3.10+ |
| 외부 의존성 | pytest (자동 채점) |
| 표준 라이브러리 | `ast`, `subprocess`, `importlib`, `os`, `json`, `csv`, `pathlib`, `dataclasses`, `abc`, `inspect`, `tempfile`, `sqlite3`, `re`, `hashlib` |
| 코딩 컨벤션 | 변수/함수: 영어 snake_case, 문서/주석/커밋: 한국어 |

---

## 라이선스

MIT License

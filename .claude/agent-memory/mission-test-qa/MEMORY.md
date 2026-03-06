# QA Agent Memory

## 검증된 패턴

### answers.py 기반 미션 공통 패턴
- **헬퍼 3종 세트**: `_normalize()`, `_load_answers()`, `_check()` - 5개 미션에서 동일 구조 확인
- `_normalize`: `re.sub(r"\s+", " ", s.strip())` - 대소문자 미변환 (리눅스 명령어 특성상 의도적)
- `_load_answers`: `importlib.util.spec_from_file_location("answers", path)` - sys.modules 미등록으로 충돌 없음
- `_check`: 빈 문자열/None 모두 "답이 비어 있습니다" 메시지 출력
- fixture scope: conftest.py `submission_dir`는 session, 테스트 파일 `answers`는 module

### conftest.py 표준 패턴
- `_MISSION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` (2단계 상위)
- `_DEFAULT_SUBMISSION = os.path.join(_MISSION_DIR, "sample_submission")`
- CLI `--submission-dir` 옵션 우선, 없으면 `_DEFAULT_SUBMISSION` 폴더 사용

### importlib 기반 모듈 로드 패턴 (entry/python/mission02~03)
- `_SUBMISSION_DIR` 글로벌 변수 + `autouse` module-scoped fixture `_configure`
- `spec_from_file_location` + `module_from_spec` + `exec_module` + `sys.modules` 캐시 제거
- AST 최상위 함수 탐지: `ast.iter_child_nodes(tree)` 사용 (ast.walk 중첩보다 정확)

### subprocess REPL 테스트 패턴 (entry/python/mission04)
- `_run_session()` 헬퍼: `subprocess.run()` + `stdin` + `timeout=5` + `cwd=_BASE_DIR`
- stderr 무시 (stdout만 반환) - 학습자 디버깅에 불리하지만 기능적 문제 없음
- 조건부 실패 시 `pytest.fail()` 사용 권장 (`raise AssertionError` 대신)
- AI 트랩 검증: 3개 트랩 실수 포함 코드로 `--submission-dir` 실행하여 정확히 3개만 FAIL 확인
- **수정 이력**: `test_favorite_toggle`에서 메뉴 구분자 기반 섹션 분할 적용 (manage_favorite 출력 오판 방지)
- **REPL 출력 구간 분할 패턴**: `output.split("=== 프롬프트 관리 프로그램 ===")` -> sections[-2]가 직전 메뉴 호출 결과

### importlib + data_path fixture 패턴 (entry/cs/mission01~02)
- conftest.py에 `_DATA` dict + `data_path` session-scoped fixture (tmp_path_factory)
- JSON 데이터를 임시 파일로 생성하여 `load_data()` 테스트에 활용
- `_SUBMISSION_DIR` 글로벌 변수 + `autouse` module-scoped fixture `_configure`
- 동일한 mktemp("data") 사용해도 tmp_path_factory가 고유 suffix 추가하여 충돌 없음
- AST 함수 탐지: `ast.walk(tree)`로 FunctionDef 수집 (중첩 함수도 포함)

### 검증 완료 미션 (2026-03-06)
- entry/dev-environment/mission01~04: 4x4=16 tests all PASS
- entry/python/mission01 (Git 브랜치 워크플로우): 4 tests all PASS
- entry/python/mission02 (미니 펫 시뮬레이터): 10 tests all PASS
- entry/python/mission03 (Git 워크플로우 시뮬레이터): 10 tests all PASS (데드코드 수정)
- entry/python/mission04 (프롬프트 관리 프로그램): 16 tests all PASS, AI 트랩 3개 유효성 확인
- entry/cs/mission01 (MAC 연산 기반 패턴 매칭): 11 tests all PASS
- entry/cs/mission02 (2D 컨볼루션 기반 특징 추출): 12 tests all PASS
- missions/ 전체 (6개 미션): 81 tests all PASS (단일 파일 통합 후)
- 전체 동시 실행 시에도 모듈 충돌 없음 확인 (160개 테스트)

### missions/ 디렉토리 QA 결과 (2026-03-06)
- [missions-qa-details.md](./missions-qa-details.md) - 6개 미션 상세 검증 기록

## 알려진 문서 불일치
- (수정완료) CLAUDE.md에서 entry/python/mission01이 "Git 브랜치 워크플로우"로 올바르게 기재됨
- (수정완료) CLAUDE.md에 entry_python_mission04까지 등재 확인
- **DB M01 배점 합계 오류**: solution.md 배점 합계 101점 (100점이어야 함)
- **Python M01 배점 불일치**: problem.md vs solution.md/test 간 yield(8->7점), type_hints(5->6점)
- **Algo M01 잔여 참조**: test_mini_git.py에 "cli.py" docstring 3곳 잔존 (mini_git.py가 올바름)
- **DS M01 과도한 import 차단**: test_no_builtin_cache가 `import collections` 전체 차단 (defaultdict 사용 불가)

## _check() 엣지 케이스 검증 결과 (answers.py 패턴)
- None: AssertionError 정상 발생
- int: AssertionError 정상 발생 (isinstance(raw, str) 체크)
- list: AssertionError 정상 발생
- 빈 문자열: AssertionError 정상 발생
- 공백만: AssertionError 정상 발생
- 키 누락: `answers.get(qid, "")` -> 빈 문자열 -> AssertionError
- **미처리**: answers 변수 자체가 dict가 아닌 경우 (list 등) -> AttributeError 발생 (개선 권장)

## _normalize() 동작 특성
- 따옴표 내부 공백도 정규화됨: `"initial  commit"` -> `"initial commit"` (Minor)
- 대소문자 보존: `PWD` != `pwd` (의도적)
- 탭/개행도 공백으로 변환

## 알려진 동점 처리 의존성
- **entry/cs/mission02 img_03**: edge_v와 sharpen의 relu sum이 동일(9)하여 dict 순회 순서에 의존
  - `>` 비교 사용 시 먼저 순회되는 edge_v 선택 (현재 기대값)
  - `>=` 비교 사용 시 마지막 sharpen 선택 -> FAIL
  - problem.md에 동점 처리 규칙 미명시 -> Minor 불공정 소지

## 참고 파일
- [entry-answers-qa-details.md](./entry-answers-qa-details.md) - 상세 정합성 검증 기록
- [entry-cs-qa-details.md](./entry-cs-qa-details.md) - entry/cs mission01~02 상세 검증 기록

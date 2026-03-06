# missions/ 디렉토리 QA 상세 검증 기록

## 검증 일시: 2026-03-06

## 검증 범위
- missions/python/level1/mission01 (Python 도서 관리 시스템) - 17 tests
- missions/python/level1/mission02 (서버 접근 로그 분석기) - 7 tests
- missions/linux/level2/mission01 (리눅스 서버 보안 감사 도구) - 7 tests
- missions/ds/level1/mission01 (Mini LRU 캐시) - 15 tests
- missions/algo/level2/mission01 (Mini Git 커밋 그래프 시뮬레이터) - 16 tests
- missions/db/level3/mission01 (커밋 이력 DB 분석기) - 19 tests

## 전체 테스트 실행 결과
- `python3 -m pytest missions/ -v` -> 81 passed in 3.04s (ALL PASS)

## 기대값 검증 결과
- Python M02 TRAP_CSV: IP TOP 5, Status ratios, Slow endpoints - 모두 수동 계산 결과와 일치
- Linux M01 모니터 로그: CPU 평균 36.32% 수동 계산 일치
- DB M01 CSV 데이터: 작성자별 커밋수/파일수, 브랜치별 커밋수, 히스토리 - 모두 수동 계산 일치

## 발견된 문제

### Critical
1. **DB M01 배점 합계 오류**: solution.md 19개 체크항목 배점 합계 = 101 (100이어야 함)
2. **DS M01 test_no_builtin_cache 과도한 차단**: `import collections` 자체를 차단하여 defaultdict 사용 불가

### Minor
1. **Python M01 배점 불일치**: problem.md(yield=8, type_hints=5) vs test/solution.md(yield=7, type_hints=6)
2. **Algo M01 cli.py 잔여 참조**: test_mini_git.py:238,240,242 docstring/에러메시지에 "cli.py" 잔존
3. **CLAUDE.md 다중파일 패턴 기술**: `_SUBMISSION_DIR` + `autouse` 패턴 설명이 남아있으나 missions/ 내에서도 사용 중이므로 유효

## 미션별 상세

### Python M01 (book_manager.py) - 17 tests, 4 AI traps
- conftest.py: 표준 패턴 ✅
- AST 분석: Book dataclass, yield, decorator, Any ratio - 정확
- CLI: subprocess + tmpdir - 적절
- Persistence: JSONL roundtrip - 적절
- AI 트랩 유효성: yield(✅), no_any(✅), cli_help(✅), no_pickle(✅)

### Python M02 (log_analyzer.py) - 7 tests, 3 AI traps
- conftest.py: 표준 패턴 ✅
- TRAP_CSV 24행 데이터: 빈 IP, 1xx 상태코드, 소수점 response_time 포함
- AI 트랩 유효성: ip_order(✅), status_ratio(✅), slow_values(✅)

### Linux M01 (auditor.py) - 7 tests, 4 AI traps
- conftest.py: 표준 패턴 ✅
- 6개 설정파일 tmpdir 생성 후 subprocess 실행
- 라인 기반 매칭: 토픽+취약 키워드 조합 검색 (섹션 간 오염 방지)
- AI 트랩 유효성: ssh_audit(✅), firewall_audit(✅), account_audit(✅), permission_audit(✅)

### DS M01 (lru_cache.py) - 15 tests, 4 AI traps
- conftest.py: 표준 패턴 ✅
- REPL 파싱: _parse_responses 헬퍼 - 프롬프트 제거 + 응답 추출
- Popen + sleep: TTL lazy deletion 검증 (2초 대기)
- AI 트랩 유효성: no_builtin_cache(⚠️과도), output_format(✅), lru_get_refresh(✅), ttl_expired_get(✅)

### Algo M01 (mini_git.py) - 16 tests, 4 AI traps
- conftest.py: 표준 패턴 ✅
- 결정적 해시: generate_hash로 사전 계산 가능
- 2세션 독립성: linear_responses(path_same_branch) / branch_responses(나머지)
- AI 트랩 유효성: no_builtin_sort(✅), commit_parent(✅), log_all_branches(✅), path_cross_branch(✅)

### DB M01 (commit_analyzer.py) - 19 tests, 5 AI traps
- conftest.py: 표준 패턴 ✅
- sqlite3 직접 연결 + subprocess + 라인 매칭 조합
- Recursive CTE로 히스토리 추적 (self_join_parent 트랩 관련)
- AI 트랩 유효성: root_commit_null(✅), author_left_join(✅), branch_no_commits(✅), distinct_file_count(✅), self_join_parent(✅)

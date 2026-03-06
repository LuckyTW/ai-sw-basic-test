## 문항 정답지 - Git 워크플로우 시뮬레이터

### 정답 코드 (TODO 3개 부분만)

```python
def add(self, filename):
    if filename not in self.staged:
        self.staged.append(filename)

def commit(self, message):
    if not self.staged:
        return "nothing to commit"
    commit_record = {
        "message": message,
        "files": list(self.staged),
        "branch": self.branch,
    }
    self.commits.append(commit_record)
    self.staged = []
    return f"committed: {message}"

def status(self):
    return f"브랜치: {self.branch}, 스테이징: {len(self.staged)}개, 커밋: {len(self.commits)}개"
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 |
|------|----------|------|----------|
| 1 | GitSimulator 클래스 + summarize 함수 정의 | 10점 | AST 자동 |
| 2 | 외부 라이브러리 미사용 | 10점 | AST 자동 |
| 3 | 초기 상태 (branch="main", staged=[], commits=[], branches=["main"]) | 10점 | import 자동 |
| 4 | **[TODO]** add() 파일 스테이징 + 중복 무시 | 10점 | import 자동 |
| 5 | **[TODO]** commit() 정상 커밋 + 빈 스테이징 처리 | 10점 | import 자동 |
| 6 | log() 역순 반환 + 원본 불변 (commit 정상 구현 시 통과) | 10점 | import 자동 |
| 7 | create_branch() 생성 + 중복 방지 | 10점 | import 자동 |
| 8 | switch() 전환 + 전환 후 커밋 branch 반영 (commit 정상 구현 시 통과) | 10점 | import 자동 |
| 9 | **[TODO]** status() 정확한 포맷 | 10점 | import 자동 |
| 10 | summarize() 정상 + 빈 시뮬레이터 (commit 정상 구현 시 통과) | 10점 | import 자동 |

- Pass 기준: 총 100점 중 100점 (10개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)
- 학생 구현 범위: add, commit, status (3개 메서드)
- 나머지 7개 테스트는 제공된 코드 + commit 정상 구현 시 자동 통과

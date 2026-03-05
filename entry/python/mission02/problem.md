## 문항: Git 워크플로우 시뮬레이터

### 문제

Git의 기본 워크플로우를 시뮬레이션하는 `GitSimulator` 클래스의 **일부 메서드**를 완성하세요.

대부분의 코드는 이미 작성되어 있습니다.
`template/git_simulator.py`에서 `# TODO` 표시된 **3개 메서드만** 구현하면 됩니다.

---

### 이미 구현된 코드 (수정하지 마세요)

| 메서드/함수 | 설명 |
|------------|------|
| `__init__(self)` | 초기 상태 설정 - `staged=[]`, `commits=[]`, `branch="main"`, `branches=["main"]` |
| `log(self)` | 커밋 이력을 역순(최신 먼저)으로 반환 |
| `create_branch(self, name)` | 브랜치 생성 (중복 시 `False`) |
| `switch(self, name)` | 브랜치 전환 (없으면 `False`) |
| `summarize(simulator)` | 전체 현황 요약 문자열 반환 |

---

### 구현할 메서드 (TODO 3개)

#### 1. `add(self, filename)`
- 파일을 스테이징 영역(`self.staged`)에 추가합니다
- 이미 `self.staged`에 있는 파일이면 추가하지 않습니다 (중복 방지)

#### 2. `commit(self, message)`
- `self.staged`가 비어있으면 → `"nothing to commit"` 반환
- 비어있지 않으면:
  - `self.commits`에 딕셔너리 추가: `{"message": message, "files": staged 복사본, "branch": self.branch}`
  - `self.staged`를 빈 리스트로 초기화
  - `"committed: {message}"` 반환

> **힌트**: `staged 복사본`은 `list(self.staged)` 로 만들 수 있습니다.

#### 3. `status(self)`
- 아래 형식의 문자열을 반환합니다.
  - `"브랜치: {self.branch}, 스테이징: {N}개, 커밋: {M}개"`
  - `N` = `self.staged`의 길이, `M` = `self.commits`의 길이

---

### 실행 예시

```python
sim = GitSimulator()
sim.add("README.md")
sim.add("main.py")
sim.add("README.md")             # 이미 있으므로 무시됨

print(len(sim.staged))            # 2
print(sim.commit("initial commit"))  # committed: initial commit
print(sim.status())               # 브랜치: main, 스테이징: 0개, 커밋: 1개
print(sim.commit("empty"))        # nothing to commit
```

### 제약 사항
- **외부 라이브러리 사용 금지** - `import` 문을 추가하지 마세요
- 이미 구현된 코드를 수정하지 마세요
- `# TODO` 표시된 3개 메서드만 구현하세요

### 제출 방식
- `git_simulator.py` 파일 1개를 제출합니다.
- `template/git_simulator.py`의 `# TODO` 부분을 채우세요.

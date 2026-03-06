## 문항: Git 브랜치 워크플로우

### 문제

Git 브랜치를 활용한 워크플로우의 기본 명령어를 작성하세요.

#### 작성 예시

> **상황:** 최신 커밋의 변경 내용을 확인하고 싶다

```python
"q0": "git show"
```

위와 같이, 각 상황에 맞는 Git 명령어를 `answers.py`에 문자열로 작성하세요.

#### Q1. 커밋 생성

스테이징된 파일을 커밋하세요. `-m` 옵션으로 커밋 메시지를 `initial commit`으로 작성합니다. 메시지는 반드시 따옴표로 감싸야 합니다.

**실행 결과:**
```
[main (root-commit) a1b2c3d] initial commit
 1 file changed, 1 insertion(+)
```

#### Q2. 브랜치 생성

`feature`라는 이름의 새 브랜치를 생성하세요. 현재 브랜치에서 전환하지 않습니다.

**실행 결과:**
```
(브랜치가 생성되며, 출력 없음)
```

#### Q3. 브랜치 전환

`feature` 브랜치로 전환하세요.

**실행 결과:**
```
Switched to branch 'feature'
```

#### Q4. 브랜치 병합

`feature` 브랜치의 변경 사항을 현재 브랜치에 병합하세요.

**실행 결과:**
```
Updating a1b2c3d..d4e5f6a
Fast-forward
 feature.txt | 1 +
 1 file changed, 1 insertion(+)
```

### 제약 사항
- 각 답안은 한 줄짜리 명령어 문자열입니다.
- 불필요한 옵션 없이 가장 간결한 형태로 작성하세요.

### 제출 방식
`answers.py` 파일의 `q1`~`q4` 값을 채워 제출하세요.

```python
# answers.py
answers = {
    "q1": "",
    "q2": "",
    "q3": "",
    "q4": "",
}
```

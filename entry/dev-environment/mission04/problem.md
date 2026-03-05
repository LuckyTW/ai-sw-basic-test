## 문항: Git 기본 명령어

### 문제

Git을 사용하여 버전 관리를 시작하기 위한 기본 명령어를 작성하세요.

#### 작성 예시

> **상황:** 최신 커밋의 변경 내용을 확인하고 싶다

```python
"q0": "git show"
```

위와 같이, 각 상황에 맞는 Git 명령어를 `answers.py`에 문자열로 작성하세요.

#### Q1. 저장소 초기화

현재 디렉토리를 새로운 Git 저장소로 초기화하세요.

**실행 결과:**
```
Initialized empty Git repository in /home/user/project/.git/
```

#### Q2. 전체 파일 스테이징

현재 디렉토리의 모든 변경 파일을 스테이징 영역에 추가하세요. `.`(현재 디렉토리 전체)을 인자로 사용합니다.

#### Q3. 상태 확인

현재 저장소의 상태(변경사항, 스테이징 여부)를 확인하세요.

**실행 결과:**
```
On branch main
Changes to be committed:
  new file:   README.md
```

#### Q4. 커밋 이력 확인

지금까지의 커밋 이력을 확인하세요.

**실행 결과:**
```
commit a1b2c3d (HEAD -> main)
Author: user <user@example.com>
Date:   Mon Mar 1 10:00:00 2026

    Initial commit
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

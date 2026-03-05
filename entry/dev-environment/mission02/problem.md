## 문항: Docker 기본 명령어

### 문제

Docker를 사용하기 위한 기본 명령어를 작성하세요.

#### 작성 예시

> **상황:** Docker 서비스의 상세 시스템 정보를 확인하고 싶다

```python
"q0": "docker info"
```

위와 같이, 각 상황에 맞는 Docker 명령어를 `answers.py`에 문자열로 작성하세요.

#### Q1. Docker 버전 확인

설치된 Docker의 버전 정보를 출력하세요.

**실행 결과:**
```
Docker version 24.0.7, build afdd53b
```

#### Q2. 이미지 다운로드

Docker Hub에서 `nginx` 이미지를 다운로드하세요. 태그는 지정하지 않습니다.

#### Q3. 이미지 목록 확인

로컬에 저장된 Docker 이미지 목록을 확인하세요.

**실행 결과:**
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    a8758716bb6a   2 weeks ago    187MB
```

#### Q4. 컨테이너 목록 확인

중지된 컨테이너를 포함하여 모든 컨테이너 목록을 출력하세요. `docker ps` 명령어에 `-a` 옵션을 사용합니다.

**실행 결과:**
```
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS    PORTS   NAMES
a1b2c3d4e5f6   nginx   ...       ...       Exited    ...     my-nginx
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

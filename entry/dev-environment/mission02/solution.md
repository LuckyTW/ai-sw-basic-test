## 문항 2 정답지

### 정답 코드

```python
answers = {
    "q1": "docker --version",
    "q2": "docker pull nginx",
    "q3": "docker images",
    "q4": "docker ps -a",
}
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 | 허용 변형 |
|------|----------|------|----------|---------|
| 1 | Docker 버전 확인: `docker --version` | 25점 | 자동 | `docker -v`, `docker version` |
| 2 | nginx 이미지 다운로드: `docker pull nginx` | 25점 | 자동 | `docker pull nginx:latest` |
| 3 | 로컬 이미지 목록: `docker images` | 25점 | 자동 | `docker image ls` |
| 4 | 모든 컨테이너 목록 (중지 포함): `docker ps -a` | 25점 | 자동 | `docker ps --all` |

- Pass 기준: 총 100점 중 100점 (4개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)

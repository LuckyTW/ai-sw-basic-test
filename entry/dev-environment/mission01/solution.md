## 문항 1 정답지

### 정답 코드

```python
answers = {
    "q1": "pwd",
    "q2": "mkdir projects",
    "q3": "cd projects",
    "q4": "ls -la",
}
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 | 허용 변형 |
|------|----------|------|----------|---------|
| 1 | 현재 작업 디렉토리 경로 출력: `pwd` | 25점 | 자동 | - |
| 2 | 'projects' 폴더 생성: `mkdir projects` | 25점 | 자동 | `mkdir -p projects` |
| 3 | 'projects' 폴더로 이동: `cd projects` | 25점 | 자동 | `cd projects/`, `cd ./projects` |
| 4 | 숨김 파일 포함 상세 목록: `ls -la` | 25점 | 자동 | `ls -al`, `ls -l -a`, `ls -a -l` |

- Pass 기준: 총 100점 중 100점 (4개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)

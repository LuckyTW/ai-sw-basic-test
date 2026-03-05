## 문항 3 정답지

### 정답 코드

```python
answers = {
    "q1": "touch README.md",
    "q2": "cat README.md",
    "q3": "cp README.md docs/",
    "q4": "rm temp.txt",
}
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 | 허용 변형 |
|------|----------|------|----------|---------|
| 1 | 빈 파일 생성: `touch README.md` | 25점 | 자동 | - |
| 2 | 파일 내용 출력: `cat README.md` | 25점 | 자동 | - |
| 3 | 파일 복사: `cp README.md docs/` | 25점 | 자동 | `cp README.md docs`, `cp README.md docs/README.md` |
| 4 | 파일 삭제: `rm temp.txt` | 25점 | 자동 | - |

- Pass 기준: 총 100점 중 100점 (4개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)

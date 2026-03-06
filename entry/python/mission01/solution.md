## 문항 정답지 - Git 브랜치 워크플로우

### 정답 코드

```python
answers = {
    "q1": 'git commit -m "initial commit"',
    "q2": "git branch feature",
    "q3": "git checkout feature",
    "q4": "git merge feature",
}
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 | 허용 변형 |
|------|----------|------|----------|---------|
| 1 | 커밋 생성: `git commit -m "initial commit"` | 25점 | 자동 | `git commit -m 'initial commit'` (작은따옴표) |
| 2 | 브랜치 생성: `git branch feature` | 25점 | 자동 | - |
| 3 | 브랜치 전환: `git checkout feature` | 25점 | 자동 | `git switch feature` |
| 4 | 브랜치 병합: `git merge feature` | 25점 | 자동 | - |

- Pass 기준: 총 100점 중 100점 (4개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)

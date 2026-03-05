## 문항: 미니 펫 시뮬레이터

### 시험 정보
- 과정: AI 올인원 / AI 네이티브
- 단계: 입학연수
- 난이도: 1
- 권장 시간: 15분
- Pass 기준: 정답 체크리스트 10개 전체 충족 (100점)

### 문제

가상 펫을 관리하는 **미니 펫 시뮬레이터**를 구현하세요.

펫에게 밥을 주고(`feed`) 놀아주면(`play`) 배고픔과 행복 수치가 변합니다.
여러 마리를 관리하는 펫샵(`PetShop`) 클래스와, 전체 현황을 요약하는 함수(`summarize`)도 구현해야 합니다.

---

### 구현 요구사항

#### 1. `Pet` 클래스

| 메서드 | 설명 |
|--------|------|
| `__init__(self, name, species, hunger=50, happiness=50)` | 이름(str), 종류(str), 배고픔(int, 0~100), 행복(int, 0~100) |
| `feed(self)` | 배고픔 20 감소 (최소 0) |
| `play(self)` | 행복 20 증가 (최대 100), 배고픔 10 증가 (최대 100) |
| `status(self) -> str` | `"[종류] 이름 - 배고픔: N, 행복: N"` 형식 문자열 반환 |

**예시:**
```python
pet = Pet("나비", "고양이")
pet.feed()
print(pet.status())  # [고양이] 나비 - 배고픔: 30, 행복: 50
pet.play()
print(pet.status())  # [고양이] 나비 - 배고픔: 40, 행복: 70
```

#### 2. `PetShop` 클래스

| 메서드 | 설명 |
|--------|------|
| `__init__(self)` | 빈 펫 목록으로 시작 |
| `add_pet(self, pet)` | 펫 추가 |
| `find_pet(self, name)` | 이름으로 검색, 없으면 `None` 반환 |
| `get_hungry_pets(self, threshold=70)` | 배고픔이 threshold **이상**인 펫 리스트 반환 |
| `to_dict_list(self)` | `[{"name": ..., "species": ..., "hunger": ..., "happiness": ...}]` 형식 반환 |

#### 3. `summarize(shop)` 독립 함수

- 형식: `"총 N마리 | 평균 행복도: X.X"`
- 빈 펫샵: `"총 0마리 | 평균 행복도: 0.0"`

### 제약 사항
- **외부 라이브러리 사용 금지** — `import` 문을 사용하지 마세요 (표준 라이브러리 포함)
- Python 기본 문법(클래스, 메서드, 조건문, 반복문, 리스트, 딕셔너리)만으로 구현하세요

### 제출 방식
- `pet_simulator.py` 파일 1개를 제출합니다.
- `template/pet_simulator.py`의 빈 구현(`pass`)을 채우세요.

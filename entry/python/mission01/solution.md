## 문항 정답지 — 미니 펫 시뮬레이터

### 정답 코드

```python
class Pet:
    def __init__(self, name, species, hunger=50, happiness=50):
        self.name = name
        self.species = species
        self.hunger = hunger
        self.happiness = happiness

    def feed(self):
        self.hunger = max(0, self.hunger - 20)

    def play(self):
        self.happiness = min(100, self.happiness + 20)
        self.hunger = min(100, self.hunger + 10)

    def status(self):
        return f"[{self.species}] {self.name} - 배고픔: {self.hunger}, 행복: {self.happiness}"


class PetShop:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def find_pet(self, name):
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_hungry_pets(self, threshold=70):
        result = []
        for pet in self.pets:
            if pet.hunger >= threshold:
                result.append(pet)
        return result

    def to_dict_list(self):
        result = []
        for pet in self.pets:
            result.append({
                "name": pet.name,
                "species": pet.species,
                "hunger": pet.hunger,
                "happiness": pet.happiness,
            })
        return result


def summarize(shop):
    count = len(shop.pets)
    if count == 0:
        return "총 0마리 | 평균 행복도: 0.0"
    total_happiness = 0
    for pet in shop.pets:
        total_happiness += pet.happiness
    avg = total_happiness / count
    return f"총 {count}마리 | 평균 행복도: {avg}"
```

### 정답 체크리스트

| 번호 | 체크 항목 | 배점 | 검증 방법 |
|------|----------|------|----------|
| 1 | Pet, PetShop 클래스 정의 | 10점 | AST 자동 |
| 2 | 외부 라이브러리 미사용 | 10점 | AST 자동 |
| 3 | Pet 생성 시 기본값 (hunger=50, happiness=50) | 10점 | import 자동 |
| 4 | feed() 배고픔 20 감소 + 0 이하 경계값 | 10점 | import 자동 |
| 5 | play() 행복 +20(최대100), 배고픔 +10(최대100) | 10점 | import 자동 |
| 6 | status() 문자열 포맷 정확성 | 10점 | import 자동 |
| 7 | add_pet + find_pet 동작 + None 반환 | 10점 | import 자동 |
| 8 | get_hungry_pets threshold 필터 | 10점 | import 자동 |
| 9 | to_dict_list dict 키/값 정확성 | 10점 | import 자동 |
| 10 | summarize 정상 + 빈 펫샵 처리 | 10점 | import 자동 |

- Pass 기준: 총 100점 중 100점 (10개 전체 정답)
- AI 트랩: 없음 (입학 연수, 난이도 1)

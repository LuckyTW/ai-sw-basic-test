# pet_simulator.py - 미니 펫 시뮬레이터 (정답)


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

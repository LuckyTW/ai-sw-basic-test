# pet_simulator.py


class Pet:
    def __init__(self, name, species, hunger=50, happiness=50):
        pass  # TODO

    def feed(self):
        """배고픔 20 감소 (최소 0)"""
        pass  # TODO

    def play(self):
        """행복 20 증가 (최대 100), 배고픔 10 증가 (최대 100)"""
        pass  # TODO

    def status(self):
        """'[종류] 이름 - 배고픔: N, 행복: N' 형식 반환"""
        pass  # TODO


class PetShop:
    def __init__(self):
        pass  # TODO

    def add_pet(self, pet):
        """펫 추가"""
        pass  # TODO

    def find_pet(self, name):
        """이름으로 검색, 없으면 None"""
        pass  # TODO

    def get_hungry_pets(self, threshold=70):
        """배고픔이 threshold 이상인 펫 리스트"""
        pass  # TODO

    def to_dict_list(self):
        """[{"name": ..., "species": ..., "hunger": ..., "happiness": ...}]"""
        pass  # TODO


def summarize(shop):
    """'총 N마리 | 평균 행복도: X.X' (빈 펫샵이면 '총 0마리 | 평균 행복도: 0.0')"""
    pass  # TODO

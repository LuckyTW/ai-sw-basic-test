# pet_simulator.py — 미니 펫 시뮬레이터
# 아래 클래스와 함수를 완성하세요.


class Pet:
    def __init__(self, name, species, hunger=50, happiness=50):
        pass

    def feed(self):
        """배고픔 20 감소 (최소 0)"""
        pass

    def play(self):
        """행복 20 증가 (최대 100), 배고픔 10 증가 (최대 100)"""
        pass

    def status(self):
        """'[종류] 이름 - 배고픔: N, 행복: N' 형식 문자열 반환"""
        pass


class PetShop:
    def __init__(self):
        pass

    def add_pet(self, pet):
        """펫 추가"""
        pass

    def find_pet(self, name):
        """이름으로 검색, 없으면 None"""
        pass

    def get_hungry_pets(self, threshold=70):
        """배고픔이 threshold 이상인 펫 리스트"""
        pass

    def to_dict_list(self):
        """[{"name": ..., "species": ..., "hunger": ..., "happiness": ...}]"""
        pass


def summarize(shop):
    """'총 N마리 | 평균 행복도: X.X' (빈 펫샵이면 '총 0마리 | 평균 행복도: 0.0')"""
    pass

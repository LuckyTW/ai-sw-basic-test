"""미니 펫 시뮬레이터 — pytest 검증 (10개 테스트)

검증 방식: AST 구조 분석 + importlib 모듈 import 후 기능 검증
제출물: pet_simulator.py (1파일)
"""
import ast
import importlib.util
import os
import sys

import pytest

# ─── 모듈 레벨 변수 ───

_SUBMISSION_DIR = None


@pytest.fixture(autouse=True, scope="module")
def _configure(submission_dir):
    """submission_dir fixture로 모듈 경로 설정"""
    global _SUBMISSION_DIR
    _SUBMISSION_DIR = submission_dir


# ─── 공통 헬퍼 ───


def _load_module():
    """제출물 pet_simulator.py를 동적 import"""
    path = os.path.join(_SUBMISSION_DIR, "pet_simulator.py")
    assert os.path.isfile(path), f"pet_simulator.py 파일 없음: {path}"
    spec = importlib.util.spec_from_file_location("pet_simulator", path)
    mod = importlib.util.module_from_spec(spec)
    # 이전 캐시 제거
    if "pet_simulator" in sys.modules:
        del sys.modules["pet_simulator"]
    spec.loader.exec_module(mod)
    return mod


def _parse_ast():
    """제출물 pet_simulator.py를 AST로 파싱"""
    path = os.path.join(_SUBMISSION_DIR, "pet_simulator.py")
    assert os.path.isfile(path), f"pet_simulator.py 파일 없음: {path}"
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source, filename=path)


# ========================================================================
# TestStructure (AST 분석형) — 2개
# ========================================================================


class TestStructure:
    """코드 구조 검증"""

    def test_classes_exist(self):
        """Pet, PetShop 클래스가 정의되어 있는지 확인 (10점)"""
        tree = _parse_ast()
        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }
        assert "Pet" in class_names, "Pet 클래스가 정의되어 있지 않습니다"
        assert "PetShop" in class_names, "PetShop 클래스가 정의되어 있지 않습니다"

    def test_no_external_lib(self):
        """외부 라이브러리를 import하지 않는지 확인 (10점)"""
        tree = _parse_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert False, f"import 문이 있습니다: import {alias.name}"
            if isinstance(node, ast.ImportFrom):
                assert False, f"import 문이 있습니다: from {node.module} import ..."


# ========================================================================
# TestPet (import + 기능 검증형) — 4개
# ========================================================================


class TestPet:
    """Pet 클래스 기능 검증"""

    def test_pet_init(self):
        """Pet 생성 시 기본값(hunger=50, happiness=50) 검증 (10점)"""
        mod = _load_module()
        pet = mod.Pet("나비", "고양이")
        assert pet.name == "나비", f"name이 '나비'가 아닙니다: {pet.name}"
        assert pet.species == "고양이", f"species가 '고양이'가 아닙니다: {pet.species}"
        assert pet.hunger == 50, f"hunger 기본값이 50이 아닙니다: {pet.hunger}"
        assert pet.happiness == 50, f"happiness 기본값이 50이 아닙니다: {pet.happiness}"

    def test_feed(self):
        """feed() 배고픔 20 감소 + 0 이하 경계값 검증 (10점)"""
        mod = _load_module()

        # 일반 케이스: 50 → 30
        pet = mod.Pet("나비", "고양이")
        pet.feed()
        assert pet.hunger == 30, f"feed 후 hunger가 30이 아닙니다: {pet.hunger}"

        # 경계값: hunger=10 → feed → 0 (음수 방지)
        pet2 = mod.Pet("뽀삐", "강아지", hunger=10, happiness=50)
        pet2.feed()
        assert pet2.hunger == 0, f"hunger=10에서 feed 후 0이 아닙니다: {pet2.hunger}"

    def test_play(self):
        """play() 행복 +20(최대100), 배고픔 +10(최대100) 경계값 검증 (10점)"""
        mod = _load_module()

        # 일반 케이스: happiness 50→70, hunger 50→60
        pet = mod.Pet("나비", "고양이")
        pet.play()
        assert pet.happiness == 70, f"play 후 happiness가 70이 아닙니다: {pet.happiness}"
        assert pet.hunger == 60, f"play 후 hunger가 60이 아닙니다: {pet.hunger}"

        # 경계값: happiness=90 → play → 100 (초과 방지)
        pet2 = mod.Pet("뽀삐", "강아지", hunger=95, happiness=90)
        pet2.play()
        assert pet2.happiness == 100, f"happiness=90에서 play 후 100이 아닙니다: {pet2.happiness}"
        assert pet2.hunger == 100, f"hunger=95에서 play 후 100이 아닙니다: {pet2.hunger}"

    def test_status(self):
        """status() 문자열 포맷 검증 (10점)"""
        mod = _load_module()
        pet = mod.Pet("나비", "고양이", hunger=30, happiness=75)
        result = pet.status()
        expected = "[고양이] 나비 - 배고픔: 30, 행복: 75"
        assert result == expected, f"status 출력이 다릅니다:\n기대: {expected}\n실제: {result}"


# ========================================================================
# TestPetShop (import + 기능 검증형) — 3개
# ========================================================================


class TestPetShop:
    """PetShop 클래스 기능 검증"""

    def test_shop_add_find(self):
        """add_pet 후 find_pet 성공 + 없는 이름 None (10점)"""
        mod = _load_module()
        shop = mod.PetShop()

        pet1 = mod.Pet("나비", "고양이")
        pet2 = mod.Pet("뽀삐", "강아지")
        shop.add_pet(pet1)
        shop.add_pet(pet2)

        found = shop.find_pet("나비")
        assert found is not None, "find_pet('나비')가 None을 반환했습니다"
        assert found.name == "나비", f"find_pet 결과 name이 '나비'가 아닙니다: {found.name}"

        not_found = shop.find_pet("없는이름")
        assert not_found is None, f"존재하지 않는 이름 검색 시 None이 아닙니다: {not_found}"

    def test_hungry_pets(self):
        """get_hungry_pets(threshold=70) 필터 검증 (10점)"""
        mod = _load_module()
        shop = mod.PetShop()

        shop.add_pet(mod.Pet("나비", "고양이", hunger=80, happiness=50))
        shop.add_pet(mod.Pet("뽀삐", "강아지", hunger=50, happiness=60))
        shop.add_pet(mod.Pet("짹짹이", "새", hunger=90, happiness=40))

        hungry = shop.get_hungry_pets(threshold=70)
        names = [p.name for p in hungry]
        assert "나비" in names, "hunger=80인 '나비'가 목록에 없습니다"
        assert "짹짹이" in names, "hunger=90인 '짹짹이'가 목록에 없습니다"
        assert "뽀삐" not in names, "hunger=50인 '뽀삐'가 목록에 포함되었습니다"
        assert len(hungry) == 2, f"배고픈 펫이 2마리여야 하지만 {len(hungry)}마리입니다"

    def test_to_dict_list(self):
        """to_dict_list() dict 키/값 정확성 검증 (10점)"""
        mod = _load_module()
        shop = mod.PetShop()

        shop.add_pet(mod.Pet("나비", "고양이", hunger=30, happiness=75))
        result = shop.to_dict_list()

        assert isinstance(result, list), f"반환 타입이 list가 아닙니다: {type(result)}"
        assert len(result) == 1, f"리스트 길이가 1이 아닙니다: {len(result)}"

        pet_dict = result[0]
        assert isinstance(pet_dict, dict), f"요소 타입이 dict가 아닙니다: {type(pet_dict)}"
        assert pet_dict.get("name") == "나비", f"name 값 오류: {pet_dict.get('name')}"
        assert pet_dict.get("species") == "고양이", f"species 값 오류: {pet_dict.get('species')}"
        assert pet_dict.get("hunger") == 30, f"hunger 값 오류: {pet_dict.get('hunger')}"
        assert pet_dict.get("happiness") == 75, f"happiness 값 오류: {pet_dict.get('happiness')}"


# ========================================================================
# TestFunction (독립 함수 검증) — 1개
# ========================================================================


class TestFunction:
    """독립 함수 검증"""

    def test_summarize(self):
        """summarize() 정상 케이스 + 빈 펫샵 처리 (10점)"""
        mod = _load_module()

        # 정상 케이스: 2마리, 평균 행복도 (75+50)/2 = 62.5
        shop = mod.PetShop()
        shop.add_pet(mod.Pet("나비", "고양이", hunger=30, happiness=75))
        shop.add_pet(mod.Pet("뽀삐", "강아지", hunger=40, happiness=50))

        result = mod.summarize(shop)
        expected = "총 2마리 | 평균 행복도: 62.5"
        assert result == expected, f"summarize 출력 오류:\n기대: {expected}\n실제: {result}"

        # 빈 펫샵
        empty_shop = mod.PetShop()
        empty_result = mod.summarize(empty_shop)
        expected_empty = "총 0마리 | 평균 행복도: 0.0"
        assert empty_result == expected_empty, (
            f"빈 펫샵 summarize 오류:\n기대: {expected_empty}\n실제: {empty_result}"
        )

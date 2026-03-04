"""
프롬프트 관리 프로그램 (python_level1_mission03) — standalone pytest 테스트

3개 Validator(PMStructureValidator, PMCLIValidator, PMInteractionValidator)의
총 16개 CheckItem을 각각 독립 pytest 함수로 변환.

패턴 A (AST 분석): test_func_separation, test_data_structure, test_initial_data, test_no_external_lib
패턴 C (subprocess REPL): 나머지 12개
"""
import ast
import os
import subprocess
import sys

# ── 공통 설정 ──────────────────────────────────────────────
SUBMISSION_FILE = "prompt_manager.py"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_PATH = os.path.join(BASE_DIR, SUBMISSION_FILE)

# 허용 import 목록 (표준 라이브러리)
_ALLOWED_MODULES = frozenset({
    "os", "sys", "json", "csv", "re", "math", "random",
    "datetime", "time", "pathlib", "collections", "itertools",
    "functools", "typing", "dataclasses", "abc", "io",
    "string", "textwrap", "copy", "enum", "operator",
})


def _read_source() -> str:
    """제출물 소스코드를 읽어 반환"""
    with open(SUBMISSION_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _parse_tree() -> ast.Module:
    """제출물을 AST 파싱하여 반환"""
    return ast.parse(_read_source())


def _run_session(stdin_text: str, timeout: int = 5) -> str:
    """prompt_manager.py를 subprocess로 실행하고 stdout 반환"""
    result = subprocess.run(
        [sys.executable, SUBMISSION_FILE],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=BASE_DIR,
    )
    return result.stdout


# ═══════════════════════════════════════════════════════════
# PMStructureValidator (AST 분석, 패턴 A) — 4개
# ═══════════════════════════════════════════════════════════


def test_func_separation():
    """소스코드에 def 5개 이상 존재하는지 확인"""
    tree = _parse_tree()
    total_funcs = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            total_funcs += 1
    assert total_funcs >= 5, f"함수 {total_funcs}개 발견 (최소 5개 필요)"


def test_data_structure():
    """AST에서 List + Dict 리터럴 사용 확인"""
    tree = _parse_tree()
    has_list = False
    has_dict = False

    for node in ast.walk(tree):
        if isinstance(node, ast.List):
            has_list = True
        if isinstance(node, ast.Dict):
            has_dict = True
        if has_list and has_dict:
            break

    assert has_list and has_dict, "List와 Dict 리터럴이 모두 존재해야 합니다"


def test_initial_data():
    """dict 3개 이상을 포함하는 list 리터럴이 있는지 확인"""
    tree = _parse_tree()
    found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.List):
            dict_count = sum(
                1 for elt in node.elts
                if isinstance(elt, ast.Dict)
            )
            if dict_count >= 3:
                found = True
                break

    assert found, "dict 3개 이상을 포함하는 list 리터럴이 필요합니다"


def test_no_external_lib():
    """import 문에서 외부 라이브러리를 사용하지 않는지 확인"""
    tree = _parse_tree()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_module = alias.name.split(".")[0]
                assert top_module in _ALLOWED_MODULES, (
                    f"외부 라이브러리 '{top_module}' 사용 금지"
                )
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                top_module = node.module.split(".")[0]
                assert top_module in _ALLOWED_MODULES, (
                    f"외부 라이브러리 '{top_module}' 사용 금지"
                )


# ═══════════════════════════════════════════════════════════
# PMCLIValidator (subprocess REPL, 패턴 C) — 7개
# ═══════════════════════════════════════════════════════════


def test_menu_display():
    """메뉴에 핵심 키워드가 있고 '0'으로 종료되는지"""
    output = _run_session("0\n")
    assert output, "프로그램 출력이 없습니다"

    keywords = ["추가", "목록", "검색", "즐겨찾기", "종료"]
    found = sum(1 for kw in keywords if kw in output)
    assert found >= 4, f"메뉴 키워드 {found}개 발견 (최소 4개 필요): {keywords}"


def test_add_prompt():
    """프롬프트 추가 후 목록에서 확인 가능한지"""
    # 메뉴1(추가): 제목=테스트 프롬프트, 내용=테스트 내용, 카테고리=1번
    # 메뉴2(목록): 추가된 항목 확인
    stdin = "1\n테스트 프롬프트\n테스트 내용입니다\n1\n2\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "테스트 프롬프트" in output, "추가한 프롬프트가 출력에 없습니다"


def test_list_prompts():
    """초기 3개 프롬프트가 모두 목록에 표시되는지"""
    stdin = "2\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"

    initial_titles = [
        "블로그 글 작성 도우미",
        "제품 썸네일 생성",
        "IT 컨설턴트 페르소나",
    ]
    for title in initial_titles:
        assert title in output, f"초기 프롬프트 '{title}'이 목록에 없습니다"


def test_category_filter():
    """카테고리 '텍스트 생성'(1번) 선택 시 해당 프롬프트 존재"""
    stdin = "3\n1\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "블로그 글 작성 도우미" in output, (
        "카테고리 '텍스트 생성' 필터링 결과에 '블로그 글 작성 도우미'가 없습니다"
    )


def test_search_title():
    """'블로그' 검색 시 '블로그 글 작성 도우미' 존재"""
    stdin = "4\n블로그\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "블로그 글 작성 도우미" in output, (
        "'블로그' 키워드 검색 결과에 '블로그 글 작성 도우미'가 없습니다"
    )


def test_search_content():
    """AI 트랩: 'SEO' 검색 시 '블로그 글 작성 도우미' 존재 (content에만 SEO 포함)"""
    stdin = "4\nSEO\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "블로그 글 작성 도우미" in output, (
        "'SEO' 검색 시 content 필드도 검색 대상에 포함해야 합니다"
    )


def test_add_validation():
    """AI 트랩: 빈 제목 입력 시 추가 거부 (목록에 4번째 항목이 없어야 함)

    정상 구현: 메뉴1 -> 빈 제목(return) -> 메뉴2(목록: 3개) -> 종료. extra 입력 미소비.
    트랩 구현: 메뉴1 -> 빈 제목 -> 내용("2") -> 카테고리("0") -> 메뉴2(목록: 4개!) -> 종료.
    """
    stdin = "1\n\n2\n0\n2\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"

    # 4번째 프롬프트가 없어야 함 (초기 3개만 유지)
    # "4." 뒤에 "[" 패턴이 있으면 4번째 항목이 존재
    lines = output.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("4.") and "[" in stripped:
            raise AssertionError(
                "빈 제목 입력 시 프롬프트가 추가되어서는 안 됩니다 (4번째 항목 발견)"
            )


# ═══════════════════════════════════════════════════════════
# PMInteractionValidator (subprocess REPL, 패턴 C) — 5개
# ═══════════════════════════════════════════════════════════


def test_detail_view():
    """상세 보기: 제목 + 카테고리 + 내용(SEO) 모두 출력"""
    stdin = "5\n1\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"

    required = ["블로그 글 작성 도우미", "텍스트 생성", "SEO"]
    for kw in required:
        assert kw in output, f"상세 보기에 '{kw}'가 출력되지 않았습니다"


def test_favorite_toggle():
    """AI 트랩: #1 토글(True->False) 후 즐겨찾기 목록에서 사라져야 함

    stdin: 메뉴6(즐겨찾기 관리) -> 1번 선택 -> 메뉴7(즐겨찾기 목록) -> 종료
    #1은 초기 favorite=True -> 토글 후 False -> 목록에 없어야 함

    검증 방식: show_favorites 출력은 "제목 ⭐" 형식을 사용.
    토글이 정상 동작하면 "블로그 글 작성 도우미"와 "⭐"가 같은 줄에 나타나지 않아야 함.
    """
    stdin = "6\n1\n7\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"

    # show_favorites는 "제목 ⭐" 형식으로 출력
    # 토글이 제대로 동작했으면(True->False) 블로그 글이 즐겨찾기 목록에서 사라짐
    for line in output.split("\n"):
        if "블로그 글 작성 도우미" in line and "\u2b50" in line:
            raise AssertionError(
                "즐겨찾기 토글 실패: True->False 해제 후에도 "
                "'블로그 글 작성 도우미'가 즐겨찾기 목록에 남아있습니다"
            )


def test_favorite_list():
    """초기 상태에서 즐겨찾기 목록에 '블로그 글 작성 도우미' 존재"""
    stdin = "7\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "블로그 글 작성 도우미" in output, (
        "초기 즐겨찾기 목록에 '블로그 글 작성 도우미'가 없습니다"
    )


def test_invalid_input():
    """잘못된 메뉴 입력 '99' 시 크래시 없이 안내 메시지"""
    stdin = "99\n0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"

    # 크래시 없이 정상 종료 + 안내 키워드 존재
    keywords = ["잘못", "다시", "올바", "없는", "유효"]
    assert any(kw in output for kw in keywords), (
        f"잘못된 입력 시 안내 메시지가 없습니다 (기대 키워드: {keywords})"
    )


def test_exit_message():
    """'0' 입력 시 '종료' 키워드 존재"""
    stdin = "0\n"
    output = _run_session(stdin)
    assert output, "프로그램 출력이 없습니다"
    assert "종료" in output, "'0' 입력 시 종료 안내 메시지에 '종료' 키워드가 없습니다"

"""Git 워크플로우 시뮬레이터 - pytest 검증 (10개 테스트)

검증 방식: AST 구조 분석 + importlib 모듈 import 후 기능 검증
제출물: git_simulator.py (1파일)
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
    """제출물 git_simulator.py를 동적 import"""
    path = os.path.join(_SUBMISSION_DIR, "git_simulator.py")
    assert os.path.isfile(path), f"git_simulator.py 파일 없음: {path}"
    spec = importlib.util.spec_from_file_location("git_simulator", path)
    mod = importlib.util.module_from_spec(spec)
    if "git_simulator" in sys.modules:
        del sys.modules["git_simulator"]
    spec.loader.exec_module(mod)
    return mod


def _parse_ast():
    """제출물 git_simulator.py를 AST로 파싱"""
    path = os.path.join(_SUBMISSION_DIR, "git_simulator.py")
    assert os.path.isfile(path), f"git_simulator.py 파일 없음: {path}"
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source, filename=path)


# ========================================================================
# TestStructure (AST 분석형) - 2개
# ========================================================================


class TestStructure:
    """코드 구조 검증"""

    def test_class_exists(self):
        """GitSimulator 클래스와 summarize 함수가 정의되어 있는지 확인 (10점)"""
        tree = _parse_ast()
        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }
        assert "GitSimulator" in class_names, "GitSimulator 클래스가 정의되어 있지 않습니다"

        func_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
               and not isinstance(
                   next(
                       (p for p in ast.walk(tree)
                        if isinstance(p, ast.ClassDef)
                        and node in ast.walk(p)),
                       None,
                   ),
                   ast.ClassDef,
               )
        }
        # 모듈 최상위 함수 중 summarize 확인
        top_level_funcs = {
            node.name
            for node in ast.iter_child_nodes(tree)
            if isinstance(node, ast.FunctionDef)
        }
        assert "summarize" in top_level_funcs, "summarize 독립 함수가 정의되어 있지 않습니다"

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
# TestGitBasic (import + 기능 검증형) - 4개
# ========================================================================


class TestGitBasic:
    """Git 기본 기능 검증"""

    def test_init(self):
        """초기 상태: branch='main', staged=[], commits=[], branches=['main'] (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        assert sim.branch == "main", f"초기 branch가 'main'이 아닙니다: {sim.branch}"
        assert sim.staged == [], f"초기 staged가 빈 리스트가 아닙니다: {sim.staged}"
        assert sim.commits == [], f"초기 commits가 빈 리스트가 아닙니다: {sim.commits}"
        assert sim.branches == ["main"], f"초기 branches가 ['main']이 아닙니다: {sim.branches}"

    def test_add(self):
        """파일 스테이징 + 중복 추가 시 무시 (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        sim.add("README.md")
        sim.add("main.py")
        assert len(sim.staged) == 2, f"2개 파일 add 후 staged 길이가 2가 아닙니다: {len(sim.staged)}"
        assert "README.md" in sim.staged, "README.md가 staged에 없습니다"
        assert "main.py" in sim.staged, "main.py가 staged에 없습니다"

        # 중복 추가 무시
        sim.add("README.md")
        assert len(sim.staged) == 2, f"중복 add 후 staged 길이가 2가 아닙니다: {len(sim.staged)}"

    def test_commit(self):
        """정상 커밋 + 빈 스테이징 시 'nothing to commit' (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        # 빈 스테이징
        result = sim.commit("empty")
        assert result == "nothing to commit", f"빈 스테이징 커밋 반환값 오류: {result}"
        assert len(sim.commits) == 0, "빈 스테이징에서 커밋이 추가되었습니다"

        # 정상 커밋
        sim.add("README.md")
        sim.add("main.py")
        result = sim.commit("initial commit")
        assert result == "committed: initial commit", f"커밋 반환값 오류: {result}"
        assert len(sim.commits) == 1, f"커밋 후 commits 길이가 1이 아닙니다: {len(sim.commits)}"
        assert sim.staged == [], f"커밋 후 staged가 비워지지 않았습니다: {sim.staged}"

        # 커밋 내용 검증
        c = sim.commits[0]
        assert c["message"] == "initial commit", f"커밋 메시지 오류: {c['message']}"
        assert c["branch"] == "main", f"커밋 branch 오류: {c['branch']}"
        assert "README.md" in c["files"] and "main.py" in c["files"], f"커밋 files 오류: {c['files']}"

    def test_log(self):
        """2개 커밋 후 역순 반환 + 원본 불변 검증 (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        sim.add("file1.py")
        sim.commit("first")
        sim.add("file2.py")
        sim.commit("second")

        log = sim.log()
        assert len(log) == 2, f"log 길이가 2가 아닙니다: {len(log)}"
        assert log[0]["message"] == "second", f"log[0]이 최신 커밋이 아닙니다: {log[0]['message']}"
        assert log[1]["message"] == "first", f"log[1]이 첫 커밋이 아닙니다: {log[1]['message']}"

        # 원본 불변
        assert sim.commits[0]["message"] == "first", "log() 호출 후 원본 commits 순서가 변경되었습니다"


# ========================================================================
# TestBranch (import + 기능 검증형) - 3개
# ========================================================================


class TestBranch:
    """브랜치 기능 검증"""

    def test_create_branch(self):
        """브랜치 생성(True) + 중복 생성(False) (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        result = sim.create_branch("feature")
        assert result is True, f"브랜치 생성 반환값이 True가 아닙니다: {result}"
        assert "feature" in sim.branches, "feature 브랜치가 branches에 없습니다"

        # 중복 브랜치
        result2 = sim.create_branch("feature")
        assert result2 is False, f"중복 브랜치 생성 반환값이 False가 아닙니다: {result2}"

        # main 중복
        result3 = sim.create_branch("main")
        assert result3 is False, f"main 중복 생성 반환값이 False가 아닙니다: {result3}"

    def test_switch(self):
        """브랜치 전환(True) + 없는 브랜치(False) + 전환 후 커밋의 branch 확인 (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        # 없는 브랜치 전환 실패
        result = sim.switch("nonexistent")
        assert result is False, f"없는 브랜치 전환 반환값이 False가 아닙니다: {result}"

        # 브랜치 생성 후 전환
        sim.create_branch("dev")
        result2 = sim.switch("dev")
        assert result2 is True, f"브랜치 전환 반환값이 True가 아닙니다: {result2}"
        assert sim.branch == "dev", f"전환 후 branch가 'dev'가 아닙니다: {sim.branch}"

        # 전환 후 커밋의 branch 확인
        sim.add("dev_file.py")
        sim.commit("dev commit")
        assert sim.commits[-1]["branch"] == "dev", (
            f"dev 브랜치에서 커밋한 branch가 'dev'가 아닙니다: {sim.commits[-1]['branch']}"
        )

    def test_status(self):
        """status() 정확한 포맷 검증 (10점)"""
        mod = _load_module()
        sim = mod.GitSimulator()

        sim.add("file1.py")
        sim.add("file2.py")
        sim.commit("first commit")
        sim.add("file3.py")

        result = sim.status()
        expected = "브랜치: main, 스테이징: 1개, 커밋: 1개"
        assert result == expected, f"status 출력이 다릅니다:\n기대: {expected}\n실제: {result}"


# ========================================================================
# TestFunction (독립 함수 검증) - 1개
# ========================================================================


class TestFunction:
    """독립 함수 검증"""

    def test_summarize(self):
        """summarize 정상 + 빈 시뮬레이터 처리 (10점)"""
        mod = _load_module()

        # 정상 케이스: 2개 커밋, 2개 브랜치, 3개 고유 파일
        sim = mod.GitSimulator()
        sim.add("README.md")
        sim.add("main.py")
        sim.commit("first")

        sim.create_branch("feature")
        sim.add("main.py")  # 중복 파일
        sim.add("utils.py")
        sim.commit("second")

        result = mod.summarize(sim)
        expected = "총 2개 커밋 | 브랜치: 2개 | 파일: 3개"
        assert result == expected, f"summarize 출력 오류:\n기대: {expected}\n실제: {result}"

        # 빈 시뮬레이터
        empty_sim = mod.GitSimulator()
        empty_result = mod.summarize(empty_sim)
        expected_empty = "총 0개 커밋 | 브랜치: 1개 | 파일: 0개"
        assert empty_result == expected_empty, (
            f"빈 시뮬레이터 summarize 오류:\n기대: {expected_empty}\n실제: {empty_result}"
        )

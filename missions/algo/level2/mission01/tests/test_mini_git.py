"""
Mini Git 커밋 그래프 시뮬레이터 — pytest 테스트 (16개)

4개 Validator에서 변환:
- StructureValidator (AST 분석) — 3개
- BasicCommandValidator (subprocess REPL) — 4개
- GraphAlgorithmValidator (subprocess REPL) — 5개
- SearchSortValidator (subprocess REPL) — 4개

제출물: mini_git.py, cli.py (2파일)
"""
import ast
import hashlib
import os
import subprocess
import sys
from typing import List, Optional

import pytest

# ---------------------------------------------------------------------------
# 모듈 레벨 변수 (fixture에서 설정)
# ---------------------------------------------------------------------------
_SUBMISSION_DIR = None


@pytest.fixture(autouse=True, scope="module")
def _configure(submission_dir):
    """submission_dir fixture로 모듈 경로 설정"""
    global _SUBMISSION_DIR
    _SUBMISSION_DIR = submission_dir


# ---------------------------------------------------------------------------
# 헬퍼 함수
# ---------------------------------------------------------------------------

def _generate_hash(message: str, seq: int) -> str:
    """검증용 해시 생성 (학생 코드와 동일한 함수)"""
    return hashlib.sha256(f"{message}:{seq}".encode()).hexdigest()[:7]


def _parse_responses(stdout: str) -> List[str]:
    """REPL stdout에서 프롬프트를 제거하고 응답만 추출"""
    responses: List[str] = []
    lines = stdout.split("\n")
    current_response_lines: List[str] = []

    for line in lines:
        if "mini-git>" in line:
            if current_response_lines:
                responses.append("\n".join(current_response_lines))
                current_response_lines = []

            after_prompt = line.split("mini-git>", 1)[1].strip()
            if after_prompt:
                current_response_lines.append(after_prompt)
        elif line.strip():
            current_response_lines.append(line.strip())

    if current_response_lines:
        responses.append("\n".join(current_response_lines))

    return responses


def _run_session(stdin_text: str, timeout: int = 10) -> Optional[str]:
    """REPL 세션 실행 후 stdout 반환"""
    cli_path = os.path.join(_SUBMISSION_DIR, "cli.py")
    try:
        result = subprocess.run(
            [sys.executable, cli_path],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=_SUBMISSION_DIR,
        )
        return result.stdout
    except (subprocess.TimeoutExpired, OSError):
        return None


def _run_and_parse(stdin_text: str, timeout: int = 10) -> Optional[List[str]]:
    """REPL 세션 실행 + 응답 파싱"""
    stdout = _run_session(stdin_text, timeout)
    if stdout is None:
        return None
    return _parse_responses(stdout)


def _load_source() -> str:
    """mini_git.py 소스코드 로드"""
    path = os.path.join(_SUBMISSION_DIR, "mini_git.py")
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse_ast() -> ast.Module:
    """mini_git.py AST 파싱"""
    source = _load_source()
    return ast.parse(source)


# ===========================================================================
# StructureValidator (AST 분석형) — 3개
# ===========================================================================

class TestStructure:
    """코드 구조 검증 (Commit 클래스, 금지 정렬, dict 저장소)"""

    def test_commit_class(self):
        """Commit 클래스에 hash/message/author/timestamp/parents 속성이 존재하는지 확인"""
        required_attrs = {"hash", "message", "author", "timestamp", "parents"}
        tree = _parse_ast()
        found = False

        for node in ast.walk(tree):
            if not (isinstance(node, ast.ClassDef) and node.name == "Commit"):
                continue

            found_attrs = set()
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    for stmt in ast.walk(item):
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if (isinstance(target, ast.Attribute)
                                        and isinstance(target.value, ast.Name)
                                        and target.value.id == "self"):
                                    found_attrs.add(target.attr)
                        if isinstance(stmt, ast.AnnAssign):
                            if (isinstance(stmt.target, ast.Attribute)
                                    and isinstance(stmt.target.value, ast.Name)
                                    and stmt.target.value.id == "self"):
                                found_attrs.add(stmt.target.attr)

            if required_attrs.issubset(found_attrs):
                found = True
                break

        assert found, (
            "Commit 클래스에 hash, message, author, timestamp, parents "
            "속성이 모두 정의되어야 합니다"
        )

    def test_no_builtin_sort(self):
        """[AI 트랩] sorted()/list.sort()/heapq를 사용하지 않는지 확인"""
        tree = _parse_ast()

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "sorted":
                    pytest.fail("sorted() 사용 금지 — merge sort를 직접 구현하세요")
                if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                    pytest.fail(".sort() 사용 금지 — merge sort를 직접 구현하세요")

            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "heapq":
                        pytest.fail("heapq 사용 금지 — merge sort를 직접 구현하세요")

            if isinstance(node, ast.ImportFrom):
                if node.module == "heapq":
                    pytest.fail("heapq 사용 금지 — merge sort를 직접 구현하세요")

    def test_graph_structure(self):
        """커밋 저장소가 dict(해시맵) 기반인지 확인"""
        dict_attr_names = {"commits", "store", "commit_store", "graph", "nodes"}
        tree = _parse_ast()
        found = False

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            for item in node.body:
                if not (isinstance(item, ast.FunctionDef)
                        and item.name == "__init__"):
                    continue

                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if (isinstance(target, ast.Attribute)
                                    and isinstance(target.value, ast.Name)
                                    and target.value.id == "self"
                                    and target.attr in dict_attr_names):
                                if isinstance(stmt.value, ast.Dict):
                                    found = True
                                if (isinstance(stmt.value, ast.Call)
                                        and isinstance(stmt.value.func, ast.Name)
                                        and stmt.value.func.id == "dict"):
                                    found = True

                    if isinstance(stmt, ast.AnnAssign):
                        if (isinstance(stmt.target, ast.Attribute)
                                and isinstance(stmt.target.value, ast.Name)
                                and stmt.target.value.id == "self"
                                and stmt.target.attr in dict_attr_names):
                            if stmt.value is not None:
                                if isinstance(stmt.value, ast.Dict):
                                    found = True
                                if (isinstance(stmt.value, ast.Call)
                                        and isinstance(stmt.value.func, ast.Name)
                                        and stmt.value.func.id == "dict"):
                                    found = True

        assert found, (
            "커밋 저장소를 dict 또는 {} 로 초기화하세요 "
            "(예: self.commits = {})"
        )


# ===========================================================================
# BasicCommandValidator (subprocess REPL) — 4개
# ===========================================================================

class TestBasicCommand:
    """기본 명령어 동작 검증 (INIT/COMMIT/BRANCH/SWITCH)"""

    @pytest.fixture(autouse=True)
    def setup_session(self):
        """테스트 시나리오 실행 — 기본 명령어 세트"""
        commands = (
            'INIT Alice\n'
            'COMMIT "Initial commit"\n'
            'COMMIT "Add feature"\n'
            'BRANCH dev\n'
            'SWITCH dev\n'
            'COMMIT "Dev work"\n'
            'SWITCH main\n'
            'exit\n'
        )
        self.responses = _run_and_parse(commands)

    def test_cli_runnable(self):
        """cli.py 실행 + mini-git> 프롬프트 출력 확인"""
        stdout = _run_session("exit\n")
        assert stdout is not None, "cli.py 실행 실패"
        assert "mini-git>" in stdout, (
            "cli.py에서 'mini-git> ' 프롬프트를 출력하세요"
        )

    def test_init_command(self):
        """INIT 명령어 정상 동작 (저장소 초기화 + 사용자 설정)"""
        assert self.responses is not None and len(self.responses) >= 1, (
            "REPL 응답을 파싱할 수 없습니다"
        )
        init_resp = self.responses[0]
        assert "Initialized" in init_resp, (
            "INIT → 'Initialized repository.' 메시지가 필요합니다"
        )
        assert "Alice" in init_resp, (
            "INIT Alice → 'Current user: Alice' 메시지가 필요합니다"
        )

    def test_commit_basic(self):
        """COMMIT 후 [branch hash] message 형식 출력 확인"""
        assert self.responses is not None and len(self.responses) >= 3, (
            "COMMIT 응답이 부족합니다"
        )
        c1_hash = _generate_hash("Initial commit", 1)
        c2_hash = _generate_hash("Add feature", 2)

        resp1 = self.responses[1]
        resp2 = self.responses[2]

        assert c1_hash in resp1 and "[main" in resp1 and "Initial commit" in resp1, (
            f"COMMIT 'Initial commit' → '[main {c1_hash}] Initial commit' 형식 필요"
        )
        assert c2_hash in resp2 and "[main" in resp2 and "Add feature" in resp2, (
            f"COMMIT 'Add feature' → '[main {c2_hash}] Add feature' 형식 필요"
        )

    def test_branch_switch(self):
        """BRANCH/SWITCH 정상 동작 확인"""
        assert self.responses is not None and len(self.responses) >= 7, (
            "BRANCH/SWITCH 응답이 부족합니다"
        )
        c3_hash = _generate_hash("Dev work", 3)

        branch_resp = self.responses[3]
        switch_resp = self.responses[4]
        commit_resp = self.responses[5]
        switch_back = self.responses[6]

        assert "Created branch: dev" in branch_resp, (
            "BRANCH dev → 'Created branch: dev' 출력 필요"
        )
        assert "Switched to branch: dev" in switch_resp, (
            "SWITCH dev → 'Switched to branch: dev' 출력 필요"
        )
        assert "[dev" in commit_resp and c3_hash in commit_resp, (
            f"dev 브랜치에서 COMMIT → '[dev {c3_hash}] Dev work' 형식 필요"
        )
        assert "Switched to branch: main" in switch_back, (
            "SWITCH main → 'Switched to branch: main' 출력 필요"
        )


# ===========================================================================
# GraphAlgorithmValidator (subprocess REPL) — 5개
# ===========================================================================

class TestGraphAlgorithm:
    """그래프 알고리즘 검증 (PATH/ANCESTORS/LOG)"""

    # 사전 계산 해시값 — 세션 A: 선형 체인
    _p1 = _generate_hash("Init", 1)
    _p2 = _generate_hash("Second", 2)
    _p3 = _generate_hash("Third", 3)

    # 사전 계산 해시값 — 세션 B: 브랜치 분기
    _c1 = _generate_hash("Initial commit", 1)
    _c2 = _generate_hash("Add user auth", 2)
    _c3 = _generate_hash("Add login page", 3)
    _c4 = _generate_hash("Add dashboard", 4)
    _c5 = _generate_hash("Add payment", 5)

    @pytest.fixture()
    def linear_responses(self):
        """세션 A: 선형 체인 (path_same_branch 독립 테스트)"""
        commands = (
            'INIT Alice\n'
            'COMMIT "Init"\n'
            'COMMIT "Second"\n'
            'COMMIT "Third"\n'
            f'PATH {self._p3} {self._p1}\n'
            'exit\n'
        )
        return _run_and_parse(commands)

    @pytest.fixture()
    def branch_responses(self):
        """세션 B: 브랜치 분기 (나머지 테스트)"""
        commands = (
            'INIT Alice\n'
            'COMMIT "Initial commit"\n'
            'COMMIT "Add user auth"\n'
            'BRANCH feature\n'
            'SWITCH feature\n'
            'COMMIT "Add login page"\n'
            'COMMIT "Add dashboard"\n'
            'SWITCH main\n'
            'LOG\n'
            'COMMIT "Add payment"\n'
            f'ANCESTORS {self._c5}\n'
            f'PATH {self._c4} {self._c5}\n'
            f'ANCESTORS {self._c4}\n'
            'exit\n'
        )
        return _run_and_parse(commands)

    def test_commit_parent_after_switch(self, branch_responses):
        """[AI 트랩] SWITCH 후 COMMIT이 올바른 부모 설정 (ANCESTORS 개수 검증)"""
        assert branch_responses is not None and len(branch_responses) >= 11, (
            "ANCESTORS 응답을 파싱할 수 없습니다"
        )
        ancestors_resp = branch_responses[10]

        assert self._c2 in ancestors_resp, (
            f"ANCESTORS c5: c2({self._c2})가 조상에 포함되어야 합니다"
        )
        assert self._c1 in ancestors_resp, (
            f"ANCESTORS c5: c1({self._c1})이 조상에 포함되어야 합니다"
        )
        assert self._c3 not in ancestors_resp, (
            f"ANCESTORS c5: c3({self._c3})는 다른 브랜치이므로 조상에 포함되면 안 됩니다. "
            "SWITCH 후 COMMIT의 부모는 해당 브랜치의 최신 커밋이어야 합니다"
        )
        assert self._c4 not in ancestors_resp, (
            f"ANCESTORS c5: c4({self._c4})는 다른 브랜치이므로 조상에 포함되면 안 됩니다. "
            "SWITCH 후 COMMIT의 부모는 해당 브랜치의 최신 커밋이어야 합니다"
        )

    def test_log_all_branches(self, branch_responses):
        """[AI 트랩] LOG가 모든 브랜치의 커밋을 출력하는지 확인"""
        assert branch_responses is not None and len(branch_responses) >= 9, (
            "LOG 응답을 파싱할 수 없습니다"
        )
        log_resp = branch_responses[8]

        assert self._c1 in log_resp, (
            f"LOG: c1({self._c1})이 출력되어야 합니다"
        )
        assert self._c2 in log_resp, (
            f"LOG: c2({self._c2})이 출력되어야 합니다"
        )
        assert self._c3 in log_resp, (
            f"LOG: c3({self._c3})이 출력되어야 합니다 "
            "(feature 브랜치 커밋도 포함)"
        )
        assert self._c4 in log_resp, (
            f"LOG: c4({self._c4})이 출력되어야 합니다 "
            "(feature 브랜치 커밋도 포함)"
        )

    def test_path_same_branch(self, linear_responses):
        """같은 브랜치 내 두 커밋 간 최단 경로 확인"""
        assert linear_responses is not None and len(linear_responses) >= 5, (
            "PATH 응답을 파싱할 수 없습니다"
        )
        path_resp = linear_responses[4]

        assert "Path:" in path_resp, "PATH 응답에 'Path:' 접두사가 필요합니다"
        assert "No path" not in path_resp, "선형 체인에서 경로가 존재해야 합니다"
        assert self._p1 in path_resp, (
            f"PATH p3->p1: p1({self._p1})이 경로에 포함되어야 합니다"
        )
        assert self._p2 in path_resp, (
            f"PATH p3->p1: p2({self._p2})이 경로에 포함되어야 합니다"
        )
        assert self._p3 in path_resp, (
            f"PATH p3->p1: p3({self._p3})이 경로에 포함되어야 합니다"
        )

    def test_path_cross_branch(self, branch_responses):
        """[AI 트랩] 다른 브랜치 간 두 커밋 최단 경로 확인"""
        assert branch_responses is not None and len(branch_responses) >= 12, (
            "PATH 응답을 파싱할 수 없습니다"
        )
        path_resp = branch_responses[11]

        assert "Path:" in path_resp, (
            "다른 브랜치 간 경로가 존재해야 합니다. "
            "DAG를 무방향 그래프로 취급하여 BFS하세요"
        )
        assert "No path" not in path_resp, (
            "다른 브랜치 간 경로가 존재해야 합니다. "
            "부모-자식 양방향으로 BFS해야 합니다"
        )
        assert self._c4 in path_resp, (
            f"PATH c4->c5: c4({self._c4})이 경로에 포함되어야 합니다"
        )
        assert self._c5 in path_resp, (
            f"PATH c4->c5: c5({self._c5})이 경로에 포함되어야 합니다"
        )

    def test_ancestors_complete(self, branch_responses):
        """ANCESTORS가 모든 조상을 출력하는지 확인"""
        assert branch_responses is not None and len(branch_responses) >= 13, (
            "ANCESTORS 응답을 파싱할 수 없습니다"
        )
        ancestors_resp = branch_responses[12]

        assert self._c3 in ancestors_resp, (
            f"ANCESTORS c4: c3({self._c3})이 조상에 포함되어야 합니다"
        )
        assert self._c2 in ancestors_resp, (
            f"ANCESTORS c4: c2({self._c2})이 조상에 포함되어야 합니다"
        )
        assert self._c1 in ancestors_resp, (
            f"ANCESTORS c4: c1({self._c1})이 조상에 포함되어야 합니다"
        )


# ===========================================================================
# SearchSortValidator (subprocess REPL) — 4개
# ===========================================================================

class TestSearchSort:
    """검색/정렬 검증 (SEARCH 키워드/작성자, LOG --sort-by)"""

    # 사전 계산 해시값
    _s1 = _generate_hash("Initial commit", 1)
    _s2 = _generate_hash("Add user auth", 2)
    _s3 = _generate_hash("Add login page", 3)
    _s4 = _generate_hash("Fix login bug", 4)

    @pytest.fixture(autouse=True)
    def setup_session(self):
        """검색/정렬 테스트 시나리오 (선형, 브랜치 없음)"""
        commands = (
            'INIT Alice\n'
            'COMMIT "Initial commit"\n'
            'COMMIT "Add user auth"\n'
            'COMMIT "Add login page"\n'
            'COMMIT "Fix login bug"\n'
            'SEARCH "login"\n'
            'SEARCH "nonexistent"\n'
            'SEARCH --author=Alice\n'
            'LOG --sort-by=date\n'
            'exit\n'
        )
        self.responses = _run_and_parse(commands)

    def test_search_keyword(self):
        """SEARCH 키워드 검색 (정확한 매칭 + 결과 수)"""
        assert self.responses is not None and len(self.responses) >= 6, (
            "SEARCH 응답을 파싱할 수 없습니다"
        )
        search_resp = self.responses[5]

        assert "Found 2 commit(s):" in search_resp, (
            "SEARCH 'login' -> 'Found 2 commit(s):' 출력 필요"
        )
        assert self._s3 in search_resp, (
            f"SEARCH 'login': 'Add login page'({self._s3})이 결과에 포함되어야 합니다"
        )
        assert self._s4 in search_resp, (
            f"SEARCH 'login': 'Fix login bug'({self._s4})이 결과에 포함되어야 합니다"
        )

    def test_search_no_result(self):
        """미존재 키워드 SEARCH -> 'Found 0 commit(s):'"""
        assert self.responses is not None and len(self.responses) >= 7, (
            "SEARCH 응답을 파싱할 수 없습니다"
        )
        search_resp = self.responses[6]

        assert "Found 0 commit(s):" in search_resp, (
            "SEARCH 'nonexistent' -> 'Found 0 commit(s):' 출력 필요"
        )

    def test_search_author(self):
        """SEARCH --author 작성자 검색"""
        assert self.responses is not None and len(self.responses) >= 8, (
            "SEARCH 응답을 파싱할 수 없습니다"
        )
        search_resp = self.responses[7]

        assert "Found 4 commit(s):" in search_resp, (
            "SEARCH --author=Alice -> 'Found 4 commit(s):' 출력 필요"
        )
        assert self._s1 in search_resp, (
            f"SEARCH --author=Alice: s1({self._s1})이 결과에 포함되어야 합니다"
        )
        assert self._s2 in search_resp, (
            f"SEARCH --author=Alice: s2({self._s2})이 결과에 포함되어야 합니다"
        )
        assert self._s3 in search_resp, (
            f"SEARCH --author=Alice: s3({self._s3})이 결과에 포함되어야 합니다"
        )
        assert self._s4 in search_resp, (
            f"SEARCH --author=Alice: s4({self._s4})이 결과에 포함되어야 합니다"
        )

    def test_sort_by_date(self):
        """LOG --sort-by=date 날짜순 정렬 확인"""
        assert self.responses is not None and len(self.responses) >= 9, (
            "LOG 응답을 파싱할 수 없습니다"
        )
        log_resp = self.responses[8]

        assert self._s1 in log_resp, (
            f"LOG --sort-by=date: s1({self._s1})이 출력되어야 합니다"
        )
        assert self._s2 in log_resp, (
            f"LOG --sort-by=date: s2({self._s2})이 출력되어야 합니다"
        )
        assert self._s3 in log_resp, (
            f"LOG --sort-by=date: s3({self._s3})이 출력되어야 합니다"
        )
        assert self._s4 in log_resp, (
            f"LOG --sort-by=date: s4({self._s4})이 출력되어야 합니다"
        )

        # 시간순 정렬: s1의 위치 < s2 < s3 < s4
        pos1 = log_resp.find(self._s1)
        pos2 = log_resp.find(self._s2)
        pos3 = log_resp.find(self._s3)
        pos4 = log_resp.find(self._s4)

        assert pos1 < pos2 < pos3 < pos4, (
            "LOG --sort-by=date: 커밋이 시간순으로 정렬되어야 합니다 "
            f"(s1@{pos1} < s2@{pos2} < s3@{pos3} < s4@{pos4})"
        )

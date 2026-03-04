"""
ds_level1_mission01 — Mini LRU 캐시 구현 시험 (standalone pytest)

4개 Validator에서 총 15개 CheckItem을 각각 pytest 테스트로 변환:
- StructureValidator  (AST 분석형, 3개)
- BasicCommandValidator (subprocess REPL, 5개)
- LRUValidator (subprocess REPL, 4개)
- TTLValidator (Popen + time.sleep, 3개)
"""
import ast
import os
import subprocess
import sys
import time
from typing import Optional

import pytest

# ── 경로 설정 ──────────────────────────────────────────────

SUBMISSION_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_FILE = os.path.join(SUBMISSION_DIR, "mini_redis.py")


# ── 공통 헬퍼 ──────────────────────────────────────────────


def _parse_responses(stdout: str) -> list[str]:
    """REPL stdout에서 프롬프트를 제거하고 응답만 추출

    "mini-redis> OK" → "OK"
    여러 줄 응답(INFO memory 등)은 하나로 합침
    """
    responses = []
    lines = stdout.split("\n")
    current_response_lines = []

    for line in lines:
        if "mini-redis>" in line:
            if current_response_lines:
                responses.append("\n".join(current_response_lines))
                current_response_lines = []

            after_prompt = line.split("mini-redis>", 1)[1].strip()
            if after_prompt:
                current_response_lines.append(after_prompt)
        elif line.strip():
            current_response_lines.append(line.strip())

    if current_response_lines:
        responses.append("\n".join(current_response_lines))

    return responses


def _run_repl(commands: str, timeout: int = 10) -> Optional[list[str]]:
    """mini_redis.py REPL을 subprocess.run으로 실행하고 응답 리스트 반환"""
    try:
        result = subprocess.run(
            [sys.executable, SUBMISSION_FILE],
            input=commands,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=SUBMISSION_DIR,
        )
        return _parse_responses(result.stdout)
    except (subprocess.TimeoutExpired, OSError):
        return None


def _extract_int_value(response: str) -> Optional[int]:
    """'(integer) N' 또는 'N' 형식에서 정수 추출"""
    response = response.strip()
    if response.startswith("(integer)"):
        try:
            return int(response.split("(integer)")[1].strip())
        except (ValueError, IndexError):
            return None
    try:
        return int(response)
    except ValueError:
        return None


def _is_nil_response(response: str) -> bool:
    """(nil) 또는 None을 nil 응답으로 인식"""
    return response.strip().lower() in ("(nil)", "none", "nil", "null")


def _run_popen_session(
    commands_before_sleep: str,
    commands_after_sleep: str,
    sleep_sec: float = 2,
    timeout: int = 10,
) -> Optional[list[str]]:
    """Popen으로 REPL 실행 → 명령 전송 → sleep → 추가 명령 → 결과 수집"""
    proc = None
    try:
        proc = subprocess.Popen(
            [sys.executable, "-u", SUBMISSION_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=SUBMISSION_DIR,
        )

        proc.stdin.write(commands_before_sleep)
        proc.stdin.flush()

        time.sleep(sleep_sec)

        proc.stdin.write(commands_after_sleep)
        proc.stdin.flush()

        stdout, _ = proc.communicate(timeout=timeout)
        return _parse_responses(stdout)

    except (subprocess.TimeoutExpired, OSError, BrokenPipeError):
        if proc is not None:
            try:
                proc.kill()
                proc.wait(timeout=2)
            except Exception:
                pass
        return None


# ── AST 파싱 헬퍼 ──────────────────────────────────────────


def _parse_submission_ast() -> ast.Module:
    """mini_redis.py를 AST로 파싱"""
    with open(SUBMISSION_FILE, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source, filename=SUBMISSION_FILE)


# ══════════════════════════════════════════════════════════
# StructureValidator (패턴 A, AST 분석) — 3개
# ══════════════════════════════════════════════════════════


class TestStructure:
    """LRU 캐시 코드 구조 검증 (Node 클래스, 금지 import, 연결 리스트 메서드)"""

    def test_node_class(self):
        """Node 클래스에 prev/next/key/value 속성이 존재하는지 확인 (11점)"""
        tree = _parse_submission_ast()
        required_attrs = {"prev", "next", "key", "value"}

        for node in ast.walk(tree):
            if not (isinstance(node, ast.ClassDef) and node.name == "Node"):
                continue

            found_attrs = set()
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    for stmt in ast.walk(item):
                        # self.attr = ... 패턴
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if (
                                    isinstance(target, ast.Attribute)
                                    and isinstance(target.value, ast.Name)
                                    and target.value.id == "self"
                                ):
                                    found_attrs.add(target.attr)
                        # self.attr: type = ... (AnnAssign)
                        if isinstance(stmt, ast.AnnAssign):
                            if (
                                isinstance(stmt.target, ast.Attribute)
                                and isinstance(stmt.target.value, ast.Name)
                                and stmt.target.value.id == "self"
                            ):
                                found_attrs.add(stmt.target.attr)

            assert required_attrs.issubset(found_attrs), (
                f"Node.__init__에 필수 속성 누락: {required_attrs - found_attrs}"
            )
            return

        pytest.fail("Node 클래스를 찾을 수 없습니다")

    def test_no_builtin_cache(self):
        """[AI 트랩] OrderedDict/deque/functools.lru_cache를 사용하지 않는지 확인 (7점)"""
        tree = _parse_submission_ast()
        forbidden_names = {"OrderedDict", "deque", "lru_cache"}
        forbidden_modules = {"collections", "functools"}

        for node in ast.walk(tree):
            # import collections / import functools
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in forbidden_modules, (
                        f"금지 모듈 import 감지: {alias.name}"
                    )

            # from collections import OrderedDict / deque
            if isinstance(node, ast.ImportFrom):
                if node.module in forbidden_modules:
                    for alias in node.names:
                        assert alias.name not in forbidden_names, (
                            f"금지 import 감지: from {node.module} import {alias.name}"
                        )
                if node.module == "functools":
                    for alias in node.names:
                        assert alias.name != "lru_cache", (
                            "금지 import 감지: from functools import lru_cache"
                        )

    def test_linked_list_ops(self):
        """이중 연결 리스트 조작 메서드(move_to_front 등)가 2개 이상 존재하는지 확인 (7점)"""
        tree = _parse_submission_ast()
        linked_list_methods = {
            "move_to_front", "insert_front", "remove", "remove_back",
            "add_to_head", "add_to_front", "move_to_head",
            "remove_tail", "remove_last", "push_front", "pop_back",
        }

        found_methods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name in linked_list_methods:
                    found_methods.add(node.name)

        assert len(found_methods) >= 2, (
            f"연결 리스트 메서드가 2개 미만입니다 (발견: {found_methods})"
        )


# ══════════════════════════════════════════════════════════
# BasicCommandValidator (패턴 C, subprocess REPL) — 5개
# ══════════════════════════════════════════════════════════


class TestBasicCommand:
    """기본 명령어 동작 검증 (SET/GET/DEL/EXISTS/DBSIZE + 출력 형식)"""

    @pytest.fixture(autouse=True)
    def _setup_responses(self):
        """기본 테스트 시나리오 실행"""
        commands = (
            "SET name Alice\n"
            "GET name\n"
            "SET count 42\n"
            "GET count\n"
            "DEL name\n"
            "GET name\n"
            "EXISTS name\n"
            "EXISTS count\n"
            "DBSIZE\n"
            "exit\n"
        )
        self._responses = _run_repl(commands)

    def test_cli_runnable(self):
        """mini_redis.py 실행 + mini-redis> 프롬프트 출력 확인 (3점)"""
        result = subprocess.run(
            [sys.executable, SUBMISSION_FILE],
            input="exit\n",
            capture_output=True,
            text=True,
            timeout=5,
            cwd=SUBMISSION_DIR,
        )
        assert "mini-redis>" in result.stdout, (
            "mini-redis> 프롬프트가 출력되지 않습니다"
        )

    def test_set_get(self):
        """SET/GET 기본 동작이 정확한지 확인 (8점)"""
        assert self._responses is not None and len(self._responses) >= 4, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[0] = SET name Alice → "OK"
        # responses[1] = GET name → '"Alice"'
        # responses[2] = SET count 42 → "OK"
        # responses[3] = GET count → '"42"'
        assert self._responses[0].strip() == "OK", (
            f"SET name Alice → 'OK' 기대, 실제: '{self._responses[0].strip()}'"
        )
        assert "Alice" in self._responses[1], (
            f"GET name → 'Alice' 포함 기대, 실제: '{self._responses[1]}'"
        )
        assert self._responses[2].strip() == "OK", (
            f"SET count 42 → 'OK' 기대, 실제: '{self._responses[2].strip()}'"
        )
        assert "42" in self._responses[3], (
            f"GET count → '42' 포함 기대, 실제: '{self._responses[3]}'"
        )

    def test_del_command(self):
        """DEL 후 GET → (nil) 확인 (4점)"""
        assert self._responses is not None and len(self._responses) >= 6, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[4] = DEL name → "(integer) 1"
        # responses[5] = GET name → "(nil)"
        del_resp = self._responses[4].strip()
        get_resp = self._responses[5].strip()

        assert _extract_int_value(del_resp) == 1, (
            f"DEL name → 1 기대, 실제: '{del_resp}'"
        )
        assert _is_nil_response(get_resp), (
            f"GET name (삭제 후) → nil 기대, 실제: '{get_resp}'"
        )

    def test_exists_dbsize(self):
        """EXISTS/DBSIZE 정확한 카운트 확인 (5점)"""
        assert self._responses is not None and len(self._responses) >= 9, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[6] = EXISTS name → 0
        # responses[7] = EXISTS count → 1
        # responses[8] = DBSIZE → 1
        assert _extract_int_value(self._responses[6].strip()) == 0, (
            f"EXISTS name → 0 기대, 실제: '{self._responses[6].strip()}'"
        )
        assert _extract_int_value(self._responses[7].strip()) == 1, (
            f"EXISTS count → 1 기대, 실제: '{self._responses[7].strip()}'"
        )
        assert _extract_int_value(self._responses[8].strip()) == 1, (
            f"DBSIZE → 1 기대, 실제: '{self._responses[8].strip()}'"
        )

    def test_output_format(self):
        """[AI 트랩] Redis 출력 형식 준수 — OK/(nil)/(integer) N/"value" (5점)"""
        assert self._responses is not None and len(self._responses) >= 9, (
            "REPL 응답이 충분하지 않습니다"
        )

        # SET → "OK" (True/1이 아님)
        assert self._responses[0].strip() == "OK", (
            f"SET 응답이 'OK'이 아닙니다: '{self._responses[0].strip()}'"
        )

        # GET 값 → 쌍따옴표로 감싸야 함
        get_alice = self._responses[1].strip()
        assert get_alice.startswith('"') and get_alice.endswith('"'), (
            f"GET 값이 쌍따옴표로 감싸져 있지 않습니다: '{get_alice}'"
        )

        # GET 미존재 → "(nil)" (None이 아님)
        get_nil = self._responses[5].strip()
        assert get_nil == "(nil)", (
            f"GET 미존재 키 → '(nil)' 기대, 실제: '{get_nil}'"
        )

        # DEL → "(integer) 1"
        del_resp = self._responses[4].strip()
        assert del_resp.startswith("(integer)"), (
            f"DEL 응답이 '(integer)' 형식이 아닙니다: '{del_resp}'"
        )


# ══════════════════════════════════════════════════════════
# LRUValidator (패턴 C, subprocess REPL) — 4개
# ══════════════════════════════════════════════════════════


class TestLRU:
    """LRU 동작 검증 (maxmemory, 제거, GET 갱신, INFO memory)"""

    @pytest.fixture(autouse=True)
    def _setup_lru_responses(self):
        """LRU GET 갱신 핵심 테스트 시나리오 실행"""
        commands = (
            "CONFIG SET maxmemory 3\n"
            "SET k1 v1\n"
            "SET k2 v2\n"
            "SET k3 v3\n"
            "GET k1\n"
            "SET k4 v4\n"
            "GET k2\n"
            "GET k1\n"
            "GET k4\n"
            "INFO memory\n"
            "DBSIZE\n"
            "exit\n"
        )
        self._responses = _run_repl(commands)

    def test_config_maxmemory(self):
        """CONFIG SET maxmemory 설정이 동작하는지 확인 (5점)"""
        assert self._responses is not None and len(self._responses) >= 1, (
            "REPL 응답이 충분하지 않습니다"
        )
        assert self._responses[0].strip() == "OK", (
            f"CONFIG SET maxmemory 3 → 'OK' 기대, 실제: '{self._responses[0].strip()}'"
        )

    def test_lru_eviction(self):
        """메모리 초과 시 LRU 키가 제거되는지 확인 (11점)

        시나리오: k1,k2,k3 SET → GET k1(갱신) → SET k4(초과 → 제거)
        k2가 제거되어야 함 (GET k1으로 k1이 갱신되었으므로)
        DBSIZE가 3이어야 함
        """
        assert self._responses is not None and len(self._responses) >= 11, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[10] = DBSIZE → "(integer) 3"
        dbsize_resp = self._responses[10].strip()
        assert _extract_int_value(dbsize_resp) == 3, (
            f"DBSIZE → 3 기대 (maxmemory=3), 실제: '{dbsize_resp}'"
        )

    def test_lru_get_refresh(self):
        """[AI 트랩] GET 접근 시 LRU 순서가 갱신되는지 확인 (7점)

        핵심 트랩: GET k1으로 k1의 LRU 순서가 갱신됨
        → SET k4 시 k2가 제거됨 (가장 오래 접근 안 한 키)
        → GET k2 = (nil), GET k1 = "v1"
        """
        assert self._responses is not None and len(self._responses) >= 9, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[4] = GET k1 → '"v1"' (LRU 갱신!)
        # responses[5] = SET k4 → "OK" (초과 → k2 제거)
        # responses[6] = GET k2 → "(nil)" (제거됨)
        # responses[7] = GET k1 → '"v1"' (생존!)
        # responses[8] = GET k4 → '"v4"'

        get_k2 = self._responses[6].strip()
        get_k1 = self._responses[7].strip()

        assert _is_nil_response(get_k2), (
            f"GET k2 → nil 기대 (LRU 제거), 실제: '{get_k2}'"
        )
        assert "v1" in get_k1, (
            f"GET k1 → 'v1' 포함 기대 (GET 갱신으로 생존), 실제: '{get_k1}'"
        )

    def test_info_memory(self):
        """INFO memory 통계 (used_memory/maxmemory/evicted_keys) 정확성 확인 (7점)"""
        assert self._responses is not None and len(self._responses) >= 10, (
            "REPL 응답이 충분하지 않습니다"
        )
        # responses[9] = INFO memory 출력 (멀티라인)
        info_resp = self._responses[9]

        assert "used_memory:3" in info_resp, (
            f"INFO memory에 'used_memory:3' 누락: '{info_resp}'"
        )
        assert "maxmemory:3" in info_resp, (
            f"INFO memory에 'maxmemory:3' 누락: '{info_resp}'"
        )
        assert "evicted_keys:1" in info_resp, (
            f"INFO memory에 'evicted_keys:1' 누락: '{info_resp}'"
        )


# ══════════════════════════════════════════════════════════
# TTLValidator (패턴 D, Popen + time.sleep) — 3개
# ══════════════════════════════════════════════════════════


class TestTTL:
    """TTL 동작 검증 (EXPIRE/TTL 기본, lazy deletion, 미존재/미설정 키)"""

    def test_expire_ttl_basic(self):
        """EXPIRE/TTL 기본 동작 — TTL 설정 + 남은 시간 조회 (8점)"""
        commands = (
            "SET session abc\n"
            "EXPIRE session 100\n"
            "TTL session\n"
            "exit\n"
        )
        responses = _run_repl(commands)
        assert responses is not None and len(responses) >= 3, (
            "REPL 응답이 충분하지 않습니다"
        )

        # responses[0] = SET session abc → "OK"
        # responses[1] = EXPIRE session 100 → "(integer) 1"
        # responses[2] = TTL session → "(integer) 98~100"
        expire_val = _extract_int_value(responses[1].strip())
        assert expire_val == 1, (
            f"EXPIRE session 100 → 1 기대, 실제: '{responses[1].strip()}'"
        )

        ttl_val = _extract_int_value(responses[2].strip())
        assert ttl_val is not None, (
            f"TTL session → 정수 기대, 실제: '{responses[2].strip()}'"
        )
        assert 90 <= ttl_val <= 100, (
            f"TTL session → 90~100 범위 기대, 실제: {ttl_val}"
        )

    def test_ttl_expired_get(self):
        """[AI 트랩] 만료 키 GET → (nil) + DBSIZE 감소 — lazy deletion (6점)"""
        before_cmds = "SET temp val\nEXPIRE temp 1\nDBSIZE\n"
        after_cmds = "GET temp\nDBSIZE\nexit\n"

        responses = _run_popen_session(before_cmds, after_cmds, sleep_sec=2)
        assert responses is not None and len(responses) >= 5, (
            "Popen lazy deletion 테스트 응답이 충분하지 않습니다"
        )

        # responses[0] = SET temp val → "OK"
        # responses[1] = EXPIRE temp 1 → "(integer) 1"
        # responses[2] = DBSIZE → "(integer) 1" (만료 전)
        # --- sleep(2) ---
        # responses[3] = GET temp → "(nil)" (만료!)
        # responses[4] = DBSIZE → "(integer) 0" (lazy deletion)

        get_resp = responses[3].strip()
        dbsize_resp = responses[4].strip()

        assert _is_nil_response(get_resp), (
            f"만료 후 GET temp → nil 기대, 실제: '{get_resp}'"
        )
        assert _extract_int_value(dbsize_resp) == 0, (
            f"만료 후 DBSIZE → 0 기대 (lazy deletion), 실제: '{dbsize_resp}'"
        )

    def test_ttl_nonexistent(self):
        """미존재 키 TTL → -2, TTL 미설정 키 → -1 (6점)"""
        commands = (
            "TTL nonexist\n"
            "SET noexpire val\n"
            "TTL noexpire\n"
            "exit\n"
        )
        responses = _run_repl(commands)
        assert responses is not None and len(responses) >= 3, (
            "REPL 응답이 충분하지 않습니다"
        )

        # responses[0] = TTL nonexist → "(integer) -2"
        # responses[1] = SET noexpire val → "OK"
        # responses[2] = TTL noexpire → "(integer) -1"
        assert _extract_int_value(responses[0].strip()) == -2, (
            f"TTL nonexist → -2 기대, 실제: '{responses[0].strip()}'"
        )
        assert _extract_int_value(responses[2].strip()) == -1, (
            f"TTL noexpire (TTL 미설정) → -1 기대, 실제: '{responses[2].strip()}'"
        )

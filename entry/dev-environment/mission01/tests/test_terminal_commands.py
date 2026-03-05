"""터미널 기초 - 디렉토리 탐색 명령어 검증 (4개 테스트, 각 25점)"""
import importlib.util
import os
import re

import pytest

# ── 허용 정답 목록 ──
ACCEPTED = {
    "q1": ["pwd"],
    "q2": ["mkdir projects", "mkdir -p projects"],
    "q3": ["cd projects", "cd projects/", "cd ./projects"],
    "q4": ["ls -la", "ls -al", "ls -l -a", "ls -a -l"],
}


# ── 헬퍼 ──
def _normalize(s: str) -> str:
    """strip + 연속 공백 단일화"""
    return re.sub(r"\s+", " ", s.strip())


def _load_answers(submission_dir: str) -> dict:
    """학생 answers.py를 동적 import하여 answers dict 반환"""
    path = os.path.join(submission_dir, "answers.py")
    assert os.path.isfile(path), f"answers.py 파일 없음: {path}"
    spec = importlib.util.spec_from_file_location("answers", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "answers"), "answers.py에 answers 변수가 없습니다"
    return mod.answers


def _check(answers: dict, qid: str, accepted: list[str]):
    """정규화 후 허용 목록 매칭"""
    raw = answers.get(qid, "")
    assert isinstance(raw, str) and raw.strip(), f"{qid}에 답이 비어 있습니다"
    normalized = _normalize(raw)
    accepted_normalized = [_normalize(a) for a in accepted]
    assert normalized in accepted_normalized, (
        f"{qid} 오답: '{raw}' (허용: {accepted})"
    )


# ── fixture ──
@pytest.fixture(scope="module")
def answers(submission_dir):
    return _load_answers(submission_dir)


# ── 테스트 ──
class TestTerminalBasic:
    """터미널 기초 - 디렉토리 탐색"""

    def test_q1_pwd(self, answers):
        """현재 작업 디렉토리 경로 출력 (25점)"""
        _check(answers, "q1", ACCEPTED["q1"])

    def test_q2_mkdir(self, answers):
        """'projects' 폴더 생성 (25점)"""
        _check(answers, "q2", ACCEPTED["q2"])

    def test_q3_cd(self, answers):
        """'projects' 폴더로 이동 (25점)"""
        _check(answers, "q3", ACCEPTED["q3"])

    def test_q4_ls(self, answers):
        """숨김 파일 포함 상세 목록 (25점)"""
        _check(answers, "q4", ACCEPTED["q4"])

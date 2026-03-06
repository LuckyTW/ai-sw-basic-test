"""Git 브랜치 워크플로우 검증 (4개 테스트, 각 25점)"""
import importlib.util
import os
import re

import pytest

# ── 허용 정답 목록 ──
ACCEPTED = {
    "q1": ['git commit -m "initial commit"', "git commit -m 'initial commit'"],
    "q2": ["git branch feature"],
    "q3": ["git checkout feature", "git switch feature"],
    "q4": ["git merge feature"],
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
class TestGitBranch:
    """Git 브랜치 워크플로우"""

    def test_q1_commit(self, answers):
        """커밋 생성 (25점)"""
        _check(answers, "q1", ACCEPTED["q1"])

    def test_q2_branch(self, answers):
        """브랜치 생성 (25점)"""
        _check(answers, "q2", ACCEPTED["q2"])

    def test_q3_checkout(self, answers):
        """브랜치 전환 (25점)"""
        _check(answers, "q3", ACCEPTED["q3"])

    def test_q4_merge(self, answers):
        """브랜치 병합 (25점)"""
        _check(answers, "q4", ACCEPTED["q4"])

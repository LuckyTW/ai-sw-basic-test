"""Docker 기본 명령어 검증 (4개 테스트, 각 25점)"""
import importlib.util
import os
import re

import pytest

# ── 허용 정답 목록 ──
ACCEPTED = {
    "q1": ["docker --version", "docker -v", "docker version"],
    "q2": ["docker pull nginx", "docker pull nginx:latest"],
    "q3": ["docker images", "docker image ls"],
    "q4": ["docker ps -a", "docker ps --all"],
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
class TestDockerBasic:
    """Docker 기본 명령어"""

    def test_q1_version(self, answers):
        """Docker 버전 확인 (25점)"""
        _check(answers, "q1", ACCEPTED["q1"])

    def test_q2_pull(self, answers):
        """nginx 이미지 다운로드 (25점)"""
        _check(answers, "q2", ACCEPTED["q2"])

    def test_q3_images(self, answers):
        """로컬 이미지 목록 확인 (25점)"""
        _check(answers, "q3", ACCEPTED["q3"])

    def test_q4_ps(self, answers):
        """모든 컨테이너 목록 (중지 포함) (25점)"""
        _check(answers, "q4", ACCEPTED["q4"])

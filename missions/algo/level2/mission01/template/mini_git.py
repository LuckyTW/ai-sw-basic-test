# mini_git.py
import hashlib
from datetime import datetime


def generate_hash(message: str, seq: int) -> str:
    """커밋 해시 생성 (수정 금지)"""
    return hashlib.sha256(f"{message}:{seq}".encode()).hexdigest()[:7]


class Commit:
    """커밋 노드"""

    def __init__(self, hash_val: str, message: str, author: str,
                 timestamp: str, parents: list | None = None,
                 branch: str = "main"):
        pass  # TODO


class CommitGraph:
    """커밋 DAG + 저장소"""

    def __init__(self):
        pass  # TODO

    def init(self, author: str) -> None:
        """저장소 초기화"""
        pass  # TODO

    def commit(self, message: str):
        """새 커밋 생성"""
        pass  # TODO

    def branch(self, name: str) -> None:
        """새 브랜치 생성"""
        pass  # TODO

    def switch(self, name: str) -> None:
        """브랜치 전환"""
        pass  # TODO


class InvertedIndex:
    """역색인 - 단어/작성자 -> 커밋 해시 매핑"""

    def __init__(self):
        pass  # TODO

    def add_commit(self, commit) -> None:
        """커밋의 메시지 단어와 작성자를 인덱싱"""
        pass  # TODO

    def search_by_keyword(self, keyword: str) -> set:
        """키워드로 커밋 검색"""
        pass  # TODO

    def search_by_author(self, author: str) -> set:
        """작성자로 커밋 검색"""
        pass  # TODO


def merge_sort(arr: list, key=None) -> list:
    """머지 소트 직접 구현"""
    pass  # TODO


def _merge(left: list, right: list, key=None) -> list:
    """두 정렬된 리스트 병합"""
    pass  # TODO


def find_path(graph, hash1: str, hash2: str):
    """BFS로 두 커밋 간 최단 경로"""
    pass  # TODO


def find_ancestors(graph, commit_hash: str) -> list:
    """BFS로 모든 조상 탐색"""
    pass  # TODO

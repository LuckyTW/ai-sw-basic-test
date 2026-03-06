# lru_cache.py
import time


class Node:
    """이중 연결 리스트 노드"""

    def __init__(self, key: str = "", value: str = ""):
        pass  # TODO


class DoublyLinkedList:
    """센티널(head/tail) 기반 이중 연결 리스트"""

    def __init__(self):
        pass  # TODO

    def insert_front(self, node: Node) -> None:
        """노드를 리스트 맨 앞에 삽입"""
        pass  # TODO

    def remove(self, node: Node) -> None:
        """노드를 리스트에서 제거"""
        pass  # TODO

    def remove_back(self) -> Node | None:
        """리스트 맨 뒤 노드를 제거하고 반환"""
        pass  # TODO

    def move_to_front(self, node: Node) -> None:
        """노드를 리스트 맨 앞으로 이동"""
        pass  # TODO


class LRUCache:
    """dict + DoublyLinkedList 조합 LRU 캐시"""

    def __init__(self):
        pass  # TODO

    def set(self, key: str, value: str) -> str:
        """키-값 저장. "OK" 반환"""
        pass  # TODO

    def get(self, key: str) -> str | None:
        """키 조회. 값 또는 None 반환"""
        pass  # TODO

    def delete(self, key: str) -> int:
        """키 삭제. 삭제된 수 반환 (0 또는 1)"""
        pass  # TODO

    def exists(self, key: str) -> int:
        """키 존재 여부. 1 또는 0 반환"""
        pass  # TODO

    def dbsize(self) -> int:
        """현재 저장된 키 수 반환"""
        pass  # TODO

    def expire(self, key: str, seconds: int) -> int:
        """키에 TTL 설정. 성공 1, 미존재 0"""
        pass  # TODO

    def ttl(self, key: str) -> int:
        """남은 TTL 조회. -2: 미존재, -1: TTL 미설정, >=0: 남은 초"""
        pass  # TODO

    def config_set(self, param: str, value: str) -> str:
        """CONFIG SET 명령어 처리"""
        pass  # TODO

    def info_memory(self) -> dict:
        """메모리 통계 반환"""
        pass  # TODO


# -- CLI REPL --

def main():
    """REPL 루프"""
    cache = LRUCache()
    pass  # TODO


if __name__ == "__main__":
    main()

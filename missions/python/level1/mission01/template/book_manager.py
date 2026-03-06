# book_manager.py
import argparse
import json
import sys
from dataclasses import dataclass
from typing import List, Generator


# TODO: Book 데이터클래스를 구현하세요


def search_books(books: List, keyword: str) -> Generator:
    """키워드로 도서 검색"""
    pass  # TODO


# TODO: validate_args 데코레이터를 구현하세요


def save_books(books: List, filepath: str) -> None:
    """도서 목록을 파일로 저장"""
    pass  # TODO


def load_books(filepath: str) -> List:
    """파일에서 도서 목록을 로드"""
    pass  # TODO


def main() -> None:
    """CLI 진입점"""
    pass  # TODO


if __name__ == "__main__":
    main()

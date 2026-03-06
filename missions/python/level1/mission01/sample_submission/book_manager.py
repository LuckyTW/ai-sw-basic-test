import argparse
import functools
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Generator, Callable


# -- 데이터 모델 --

@dataclass
class Book:
    """도서 데이터 모델"""
    isbn: str
    title: str
    author: str
    price: int
    is_available: bool = True

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError(f"가격은 0 이상이어야 합니다: {self.price}")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(**data)


# -- 검색/필터링 --

def validate_args(func: Callable) -> Callable:
    """인자 타입 검증 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise TypeError("None은 허용되지 않습니다")
        return func(*args, **kwargs)
    return wrapper


@validate_args
def search_books(books: List, keyword: str) -> Generator:
    """도서 목록에서 keyword가 제목에 포함된 도서를 yield합니다."""
    for book in books:
        if keyword.lower() in book.title.lower():
            yield book


def filter_by_price(books: List, max_price: int) -> Generator:
    """가격 기준 필터링"""
    for book in books:
        if book.price <= max_price:
            yield book


# -- 저장/로드 --

def save_books(books: List[Book], filepath: str) -> None:
    """도서 목록을 JSONL 형식으로 저장"""
    with open(filepath, "w", encoding="utf-8") as f:
        for book in books:
            f.write(json.dumps(book.to_dict(), ensure_ascii=False) + "\n")


def load_books(filepath: str) -> List[Book]:
    """JSONL 파일에서 도서 목록을 로드"""
    books = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                books.append(Book.from_dict(data))
    return books


# -- CLI --

DATA_FILE = "books.jsonl"


def cmd_add(args: argparse.Namespace) -> None:
    """도서 추가"""
    book = Book(
        isbn=args.isbn,
        title=args.title,
        author=args.author,
        price=int(args.price),
    )

    try:
        books = load_books(DATA_FILE)
    except FileNotFoundError:
        books = []

    books.append(book)
    save_books(books, DATA_FILE)
    print(f"도서 추가 완료: {book.title}")


def cmd_list(args: argparse.Namespace) -> None:
    """도서 목록 출력"""
    try:
        books = load_books(DATA_FILE)
    except FileNotFoundError:
        print("등록된 도서가 없습니다.")
        return

    if not books:
        print("등록된 도서가 없습니다.")
        return

    for book in books:
        status = "대출가능" if book.is_available else "대출중"
        print(f"[{book.isbn}] {book.title} - {book.author} ({book.price}원) [{status}]")


def cmd_search(args: argparse.Namespace) -> None:
    """도서 검색"""
    try:
        books = load_books(DATA_FILE)
    except FileNotFoundError:
        print("등록된 도서가 없습니다.")
        return

    found = False
    for book in search_books(books, args.keyword):
        print(f"[{book.isbn}] {book.title} - {book.author}")
        found = True

    if not found:
        print(f"'{args.keyword}' 검색 결과가 없습니다.")


def main() -> None:
    """메인 CLI 진입점"""
    parser = argparse.ArgumentParser(description="도서 관리 시스템")
    subparsers = parser.add_subparsers(dest="command")

    # add 서브커맨드
    add_parser = subparsers.add_parser("add", help="도서 추가")
    add_parser.add_argument("--isbn", required=True, help="ISBN")
    add_parser.add_argument("--title", required=True, help="도서 제목")
    add_parser.add_argument("--author", required=True, help="저자")
    add_parser.add_argument("--price", required=True, type=int, help="가격")

    # list 서브커맨드
    subparsers.add_parser("list", help="도서 목록")

    # search 서브커맨드
    search_parser = subparsers.add_parser("search", help="도서 검색")
    search_parser.add_argument("--keyword", required=True, help="검색 키워드")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "add":
            cmd_add(args)
        elif args.command == "list":
            cmd_list(args)
        elif args.command == "search":
            cmd_search(args)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

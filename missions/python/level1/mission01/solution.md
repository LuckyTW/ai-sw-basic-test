## 문항 정답지 - Python 도서 관리 시스템

## 프로젝트 구조

```
submission/
└── book_manager.py    # Book 모델 + 검색/필터 + 저장/로드 + CLI
```

---

## 정답 코드

모범 답안은 `sample_submission/book_manager.py`에 위치합니다.

### 1. 데이터 모델 (25점)

- `@dataclass` 데코레이터로 `Book` 클래스 정의
- `isbn`, `title`, `author`, `price`, `is_available` 필드와 타입 힌트
- `__post_init__`으로 `price < 0` 검증
- `to_dict()`, `from_dict()` 직렬화 메서드

### AI 트랩 없음
- 이 문제는 AI 트랩이 없으나, `__post_init__`을 빠뜨리기 쉬움

### 2. 코딩 패턴 (25점)

- `validate_args` 데코레이터 직접 정의 (`functools.wraps` 사용)
- `search_books`는 `yield` 제너레이터로 구현
- 타입 힌트는 `str`, `int`, `List`, `Generator`, `Callable` 등 구체적 타입 사용

### AI 트랩 비교

**❌ AI가 흔히 하는 실수 (yield 미사용)**:
```python
def search_books(books, keyword):
    return [book for book in books if keyword in book.title]
```

**✅ 올바른 구현 (yield 사용)**:
```python
def search_books(books, keyword):
    for book in books:
        if keyword in book.title:
            yield book
```

**❌ AI가 흔히 하는 실수 (Any 남용)**:
```python
from typing import Any
def search_books(books: Any, keyword: Any) -> Any:
```

**✅ 올바른 구현 (구체적 타입)**:
```python
from typing import List, Generator
def search_books(books: List, keyword: str) -> Generator:
```

### 3. 데이터 저장 (20점)

- `save_books()`/`load_books()`로 JSONL 형식 파일 저장/로드
- `json` 모듈 사용 (pickle 금지)

### AI 트랩 비교

**❌ AI가 흔히 하는 실수 (pickle 사용)**:
```python
import pickle
def save_books(books, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(books, f)
```

**✅ 올바른 구현 (json 사용)**:
```python
import json
def save_books(books, filepath):
    with open(filepath, "w") as f:
        for book in books:
            f.write(json.dumps(book.to_dict()) + "\n")
```

### 4. CLI 인터페이스 (30점)

- `argparse`로 `add`/`list`/`search` 서브커맨드 구현
- `--help` 자동 지원
- 에러 핸들링으로 Traceback 방지

### AI 트랩 비교

**❌ AI가 흔히 하는 실수 (--help 미지원)**:
```python
command = sys.argv[1]
if command == "add": ...
```

**✅ 올바른 구현 (argparse 사용)**:
```python
parser = argparse.ArgumentParser(description="도서 관리 시스템")
# argparse가 자동으로 --help 지원
```

---

## 채점 결과 예시 (만점)

```
✅ model_dataclass    - Book 클래스가 @dataclass로 정의됨 (7점)
✅ model_fields       - 필수 필드 존재 (6점)
✅ model_type_hints   - 타입 힌트 적용 (5점)
✅ model_post_init    - price 유효성 검증 동작 (7점)
✅ pattern_yield      - search_books가 yield 제너레이터 (7점) ⚠️
✅ pattern_decorator  - 사용자 정의 데코레이터 존재 (7점)
✅ pattern_type_hints - 3개+ 함수에 타입 힌트 (6점)
✅ pattern_no_any     - Any 비율 30% 미만 (5점) ⚠️
✅ cli_runnable       - book_manager.py 존재 (5점)
✅ cli_help           - --help 동작 (5점) ⚠️
✅ cli_add            - add 서브커맨드 동작 (8점)
✅ cli_list           - list 서브커맨드 동작 (7점)
✅ cli_no_crash       - 크래시 방지 (5점)
✅ persist_roundtrip  - 왕복 무결성 (7점)
✅ persist_format     - JSONL 형식 (3점)
✅ persist_no_pickle  - pickle 미사용 (5점) ⚠️
✅ persist_integrity  - 필수 필드 포함 (5점)

총점: 100/100 ✅ PASS
```

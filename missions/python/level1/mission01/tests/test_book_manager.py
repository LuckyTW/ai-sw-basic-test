"""
Python 도서 관리 시스템 — pytest 검증 (17개 테스트)

4개 Validator(ModelValidator, PatternValidator, CLIValidator, PersistenceValidator)의
CheckItem 17개를 각각 pytest 함수로 변환.

제출물: models.py, filters.py, storage.py, cli.py (4파일)
"""
import ast
import csv
import importlib
import inspect
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import pytest

# ─── 모듈 레벨 변수 (fixture에서 설정) ───

_SUBMISSION_DIR = None


@pytest.fixture(autouse=True, scope="module")
def _configure(submission_dir):
    """submission_dir fixture로 모듈 경로 설정"""
    global _SUBMISSION_DIR
    _SUBMISSION_DIR = submission_dir


# ─── 공통 헬퍼 ───

def _parse_submission() -> List[Tuple[str, ast.Module]]:
    """제출 디렉토리의 모든 .py 파일을 AST로 파싱"""
    results = []
    for filename in sorted(os.listdir(_SUBMISSION_DIR)):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(_SUBMISSION_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=filepath)
            results.append((filepath, tree))
        except (SyntaxError, UnicodeDecodeError):
            pass
    return results


def _import_module(module_name: str):
    """제출 디렉토리에서 특정 모듈을 import (캐시 제거 후)"""
    if _SUBMISSION_DIR not in sys.path:
        sys.path.insert(0, _SUBMISSION_DIR)
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


def _run_cli(args: list, timeout: int = 10, cwd: Optional[str] = None) -> Optional[subprocess.CompletedProcess]:
    """cli.py를 subprocess로 실행"""
    work_dir = cwd or _SUBMISSION_DIR
    cli_path = os.path.join(work_dir, "cli.py")
    try:
        return subprocess.run(
            [sys.executable, cli_path] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=work_dir,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None


def _copy_submission_to(dest_dir: str) -> None:
    """제출물 전체를 대상 디렉토리에 복사"""
    for f in os.listdir(_SUBMISSION_DIR):
        if f.endswith(".py"):
            shutil.copy2(os.path.join(_SUBMISSION_DIR, f), dest_dir)


def _extract_decorator_name(deco: ast.expr) -> str:
    """데코레이터 노드에서 이름 추출"""
    if isinstance(deco, ast.Name):
        return deco.id
    if isinstance(deco, ast.Call):
        return _extract_decorator_name(deco.func)
    if isinstance(deco, ast.Attribute):
        return deco.attr
    return ""


def _has_type_hints(func_node: ast.FunctionDef) -> bool:
    """함수에 하나라도 타입 힌트가 있는지"""
    if func_node.returns:
        return True
    for arg in func_node.args.args + func_node.args.kwonlyargs:
        if arg.annotation:
            return True
    return False


def _is_any_annotation(ann: ast.expr) -> bool:
    """annotation이 Any인지 확인"""
    if isinstance(ann, ast.Name) and ann.id == "Any":
        return True
    if isinstance(ann, ast.Attribute) and ann.attr == "Any":
        return True
    return False


def _parse_jsonl(content: str) -> Optional[List[Dict[str, Any]]]:
    records = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                records.append(obj)
        except json.JSONDecodeError:
            return None
    return records if records else None


def _parse_json(content: str) -> Optional[List[Dict[str, Any]]]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)] or None
    if isinstance(data, dict):
        return [data]
    return None


def _parse_csv(content: str) -> Optional[List[Dict[str, Any]]]:
    try:
        reader = csv.DictReader(io.StringIO(content))
        records = [dict(row) for row in reader]
        return records if records else None
    except csv.Error:
        return None


# ========================================================================
# ModelValidator (AST + import 분석형) — 4개
# ========================================================================

class TestModelValidator:
    """Book 데이터 모델 검증 (dataclass, 필드, 타입 힌트, __post_init__)"""

    def test_model_dataclass(self):
        """Book 클래스가 @dataclass로 정의되어 있는지 확인 (7점)"""
        parsed = _parse_submission()

        # AST 확인: Book 클래스에 @dataclass 데코레이터가 있는지
        has_decorator = False
        for _, tree in parsed:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == "Book":
                    for deco in node.decorator_list:
                        name = _extract_decorator_name(deco)
                        if name == "dataclass":
                            has_decorator = True
                            break
        assert has_decorator, "Book 클래스에 @dataclass 데코레이터가 없습니다"

        # 런타임 확인
        models = _import_module("models")
        book_cls = getattr(models, "Book", None)
        assert book_cls is not None, "models 모듈에서 Book 클래스를 찾을 수 없습니다"
        assert hasattr(book_cls, "__dataclass_fields__"), "Book이 dataclass가 아닙니다"

    def test_model_fields(self):
        """Book에 필수 필드(isbn, title, author, price, is_available)가 있는지 확인 (6점)"""
        models = _import_module("models")
        book_cls = getattr(models, "Book", None)
        assert book_cls is not None, "models 모듈에서 Book 클래스를 찾을 수 없습니다"

        required_fields = {"isbn", "title", "author", "price", "is_available"}

        # is_available에 기본값이 있을 수도 없을 수도 있음
        book = None
        try:
            book = book_cls(
                isbn="978-89-1234-567-8",
                title="파이썬 프로그래밍",
                author="홍길동",
                price=25000,
            )
        except TypeError:
            try:
                book = book_cls(
                    isbn="978-89-1234-567-8",
                    title="파이썬 프로그래밍",
                    author="홍길동",
                    price=25000,
                    is_available=True,
                )
            except Exception:
                pass

        assert book is not None, "Book 인스턴스를 생성할 수 없습니다"

        for field_name in required_fields:
            assert hasattr(book, field_name), f"Book에 '{field_name}' 필드가 없습니다"

    def test_model_type_hints(self):
        """Book 필드에 타입 힌트가 적용되어 있는지 확인 (5점)"""
        parsed = _parse_submission()
        required_fields = {"isbn", "title", "author", "price", "is_available"}

        found = False
        for _, tree in parsed:
            for node in ast.walk(tree):
                if not (isinstance(node, ast.ClassDef) and node.name == "Book"):
                    continue
                annotated_fields = set()
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        annotated_fields.add(item.target.id)
                if required_fields.issubset(annotated_fields):
                    found = True
                    break

        assert found, "Book 필드에 타입 힌트(annotation)가 부족합니다"

    def test_model_post_init(self):
        """price < 0일 때 ValueError가 발생하는지 확인 (7점)"""
        models = _import_module("models")
        book_cls = getattr(models, "Book", None)
        assert book_cls is not None, "models 모듈에서 Book 클래스를 찾을 수 없습니다"

        with pytest.raises(ValueError):
            book_cls(
                isbn="978-89-0000-000-0",
                title="테스트",
                author="테스터",
                price=-1000,
            )


# ========================================================================
# PatternValidator (AST 분석형) — 4개
# ========================================================================

class TestPatternValidator:
    """코딩 패턴 검증 (yield, 데코레이터, 타입 힌트, Any 비율)"""

    def test_pattern_yield(self):
        """[AI 트랩] search_books가 yield 제너레이터로 구현되어 있는지 확인 (7점)"""
        parsed = _parse_submission()

        # 1. AST에서 search_books 함수 내 yield 확인
        has_yield_in_search = False
        for _, tree in parsed:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "search_books":
                    for child in ast.walk(node):
                        if isinstance(child, (ast.Yield, ast.YieldFrom)):
                            has_yield_in_search = True
                            break
        assert has_yield_in_search, "search_books 함수에 yield가 없습니다"

        # 2. 런타임 확인: isgeneratorfunction 또는 __wrapped__ 추적
        filters = _import_module("filters")
        search_fn = getattr(filters, "search_books", None)
        if search_fn is not None:
            # 데코레이터 감싸기 고려: __wrapped__ 추적
            unwrapped = search_fn
            for _ in range(10):
                inner = getattr(unwrapped, "__wrapped__", None)
                if inner is None:
                    break
                unwrapped = inner

            if inspect.isgeneratorfunction(unwrapped):
                return  # 통과

            # 3. 실제 호출하여 generator 반환 확인
            models = _import_module("models")
            book_cls = getattr(models, "Book", None)
            if book_cls is not None:
                try:
                    test_books = [
                        book_cls(isbn="978-test-001", title="파이썬 입문", author="홍길동", price=20000),
                        book_cls(isbn="978-test-002", title="자바 입문", author="김철수", price=25000),
                    ]
                    result = search_fn(test_books, "파이썬")
                    assert hasattr(result, "__next__"), "search_books가 제너레이터를 반환하지 않습니다"
                    return
                except Exception:
                    pass

        # AST에서 yield 확인됐으면 통과 (위에서 assert 통과)

    def test_pattern_decorator(self):
        """사용자 정의 데코레이터가 정의 및 적용되어 있는지 확인 (7점)"""
        parsed = _parse_submission()
        stdlib_decorators = {
            "staticmethod", "classmethod", "property",
            "abstractmethod", "dataclass", "cached_property",
            "overload", "override",
        }

        # 1. AST: 정의된 함수 중 데코레이터로 사용된 것 확인
        defined_funcs = set()
        for _, tree in parsed:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    defined_funcs.add(node.name)

        decorator_found = False
        for _, tree in parsed:
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                for deco in node.decorator_list:
                    name = _extract_decorator_name(deco)
                    if name and name not in stdlib_decorators and name in defined_funcs:
                        decorator_found = True
                        break

        assert decorator_found, "사용자 정의 데코레이터가 정의 및 적용되어 있지 않습니다"

    def test_pattern_type_hints(self):
        """3개 이상의 함수에 타입 힌트가 적용되어 있는지 확인 (6점)"""
        parsed = _parse_submission()
        hinted_count = 0
        for _, tree in parsed:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if _has_type_hints(node):
                        hinted_count += 1
        assert hinted_count >= 3, f"타입 힌트가 있는 함수가 {hinted_count}개뿐입니다 (최소 3개 필요)"

    def test_pattern_no_any(self):
        """[AI 트랩] Any 타입 비율이 30% 미만인지 확인 (5점)"""
        parsed = _parse_submission()
        total_annotations = 0
        any_count = 0

        for _, tree in parsed:
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                # 반환 타입
                if node.returns:
                    total_annotations += 1
                    if _is_any_annotation(node.returns):
                        any_count += 1
                # 매개변수 타입
                for arg in node.args.args + node.args.kwonlyargs:
                    if arg.annotation:
                        total_annotations += 1
                        if _is_any_annotation(arg.annotation):
                            any_count += 1

        # annotation이 없으면 통과
        if total_annotations == 0:
            return

        ratio = any_count / total_annotations
        assert ratio < 0.3, f"Any 타입 비율이 {ratio:.1%}입니다 (30% 미만이어야 함)"


# ========================================================================
# CLIValidator (subprocess 실행형) — 5개
# ========================================================================

class TestCLIValidator:
    """CLI 서브커맨드 동작 검증 (cli.py, --help, add, list, 크래시 방지)"""

    def test_cli_runnable(self):
        """cli.py 파일이 존재하고 실행 가능한지 확인 (5점)"""
        cli_path = os.path.join(_SUBMISSION_DIR, "cli.py")
        assert os.path.isfile(cli_path), "cli.py가 존재하지 않습니다"

    def test_cli_help(self):
        """[AI 트랩] --help 옵션이 정상 동작하는지 확인 (5점)"""
        result = _run_cli(["--help"])
        if result and result.returncode == 0 and len(result.stdout.strip()) > 10:
            return

        # -h 도 시도
        result = _run_cli(["-h"])
        assert result is not None, "--help/-h 실행에 실패했습니다"
        assert result.returncode == 0, f"--help/-h 종료 코드: {result.returncode}"
        assert len(result.stdout.strip()) > 10, "--help/-h 출력이 너무 짧습니다"

    def test_cli_add(self):
        """add 서브커맨드로 도서 추가가 동작하는지 확인 (8점)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            _copy_submission_to(tmpdir)

            result = _run_cli(
                [
                    "add",
                    "--isbn", "978-89-0000-000-0",
                    "--title", "테스트 도서",
                    "--author", "테스터",
                    "--price", "10000",
                ],
                cwd=tmpdir,
            )
            assert result is not None, "add 명령 실행에 실패했습니다"
            assert result.returncode == 0, f"add 종료 코드: {result.returncode}\nstderr: {result.stderr}"

            # 출력이 있거나 데이터 파일이 새로 생겼으면 동작한 것으로 판단
            has_output = len(result.stdout.strip()) > 0
            import glob as gl
            data_files = []
            for pattern in ["*.jsonl", "*.json", "*.csv"]:
                data_files.extend(gl.glob(os.path.join(tmpdir, pattern)))
            has_new_file = len(data_files) > 0

            assert has_output or has_new_file, "add 명령 실행 후 출력도 데이터 파일도 없습니다"

    def test_cli_list(self):
        """list 서브커맨드로 도서 목록 조회가 동작하는지 확인 (7점)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            _copy_submission_to(tmpdir)

            # 먼저 add로 데이터 넣기
            _run_cli(
                [
                    "add",
                    "--isbn", "978-89-9999-999-9",
                    "--title", "목록확인용",
                    "--author", "테스터",
                    "--price", "5000",
                ],
                cwd=tmpdir,
            )

            result = _run_cli(["list"], cwd=tmpdir)
            assert result is not None, "list 명령 실행에 실패했습니다"
            assert result.returncode == 0, f"list 종료 코드: {result.returncode}\nstderr: {result.stderr}"
            assert len(result.stdout.strip()) > 0, "list 결과에 내용이 없습니다"

    def test_cli_no_crash(self):
        """잘못된 입력에 Traceback이 출력되지 않는지 확인 (5점)"""
        result = _run_cli(["invalid_command_xyz"])
        # cli.py 자체가 없으면 별도 감점 (cli_runnable에서 처리)
        if result is None:
            cli_path = os.path.join(_SUBMISSION_DIR, "cli.py")
            assert not os.path.isfile(cli_path), "실행에 실패했지만 파일은 존재합니다"
            return
        assert "Traceback" not in result.stderr, f"잘못된 입력에 Traceback이 발생했습니다:\n{result.stderr}"


# ========================================================================
# PersistenceValidator (import + 파일 I/O형) — 4개
# ========================================================================

class TestPersistenceValidator:
    """데이터 저장 검증 (왕복 무결성, 형식, pickle 미사용, 필수 필드)"""

    @staticmethod
    def _make_test_books():
        """테스트용 Book 인스턴스 리스트 생성"""
        models = _import_module("models")
        book_cls = getattr(models, "Book", None)
        if book_cls is None:
            return None
        try:
            return [
                book_cls(isbn="978-89-1111-111-1", title="파이썬 입문", author="홍길동", price=20000),
                book_cls(isbn="978-89-2222-222-2", title="자바 입문", author="김철수", price=25000),
            ]
        except Exception:
            return None

    @staticmethod
    def _do_save(books, tmpdir):
        """save_books 호출, 생성된 파일 경로 반환"""
        storage = _import_module("storage")
        save_fn = getattr(storage, "save_books", None)
        if save_fn is None:
            return None

        try:
            filepath = os.path.join(tmpdir, "books_test.jsonl")
            save_fn(books, filepath)
            if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                return filepath
        except TypeError:
            pass
        except Exception:
            pass

        # save_books(books) 형태
        try:
            save_fn(books)
            import glob as gl
            for pattern in ["*.jsonl", "*.json", "*.csv"]:
                found = gl.glob(os.path.join(tmpdir, pattern))
                if found:
                    return found[0]
        except Exception:
            pass

        return None

    def test_persist_roundtrip(self):
        """save_books -> load_books 왕복 무결성 확인 (7점)"""
        books = self._make_test_books()
        assert books is not None, "테스트용 Book 인스턴스를 생성할 수 없습니다"

        with tempfile.TemporaryDirectory() as tmpdir:
            saved_file = self._do_save(books, tmpdir)
            assert saved_file is not None, "save_books가 파일을 생성하지 못했습니다"

            storage = _import_module("storage")
            load_fn = getattr(storage, "load_books", None)
            assert load_fn is not None, "load_books 함수를 찾을 수 없습니다"

            loaded = load_fn(saved_file)
            assert loaded is not None, "load_books가 None을 반환했습니다"
            assert len(loaded) == len(books), f"저장한 {len(books)}권 중 {len(loaded)}권만 로드됨"

            # isbn으로 매칭하여 비교
            original_isbns = {getattr(b, "isbn", None) for b in books}
            loaded_isbns = set()
            for item in loaded:
                if hasattr(item, "isbn"):
                    loaded_isbns.add(item.isbn)
                elif isinstance(item, dict):
                    loaded_isbns.add(item.get("isbn"))

            assert original_isbns == loaded_isbns, f"ISBN 불일치: 원본={original_isbns}, 로드={loaded_isbns}"

    def test_persist_format(self):
        """저장 파일이 JSONL/JSON/CSV 형식인지 확인 (3점)"""
        books = self._make_test_books()
        assert books is not None, "테스트용 Book 인스턴스를 생성할 수 없습니다"

        with tempfile.TemporaryDirectory() as tmpdir:
            saved_file = self._do_save(books, tmpdir)
            assert saved_file is not None, "save_books가 파일을 생성하지 못했습니다"
            assert os.path.isfile(saved_file), "저장된 파일이 존재하지 않습니다"

            with open(saved_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            assert content, "저장된 파일이 비어있습니다"

            # 확장자별 파싱 시도
            if saved_file.endswith(".jsonl"):
                assert _parse_jsonl(content) is not None, "JSONL 파싱에 실패했습니다"
            elif saved_file.endswith(".json"):
                assert _parse_json(content) is not None, "JSON 파싱에 실패했습니다"
            elif saved_file.endswith(".csv"):
                assert _parse_csv(content) is not None, "CSV 파싱에 실패했습니다"
            else:
                # 확장자가 없으면 순서대로 시도
                parsed = (_parse_jsonl(content) is not None
                          or _parse_json(content) is not None
                          or _parse_csv(content) is not None)
                assert parsed, "JSONL/JSON/CSV 어떤 형식으로도 파싱할 수 없습니다"

    def test_persist_no_pickle(self):
        """[AI 트랩] pickle 모듈을 사용하지 않는지 확인 (5점)"""
        parsed = _parse_submission()

        # AST에서 pickle import 탐색
        for _, tree in parsed:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not (alias.name == "pickle" or alias.name.startswith("pickle.")), \
                            "pickle 모듈을 import하고 있습니다"
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        assert not (node.module == "pickle" or node.module.startswith("pickle.")), \
                            "pickle 모듈에서 import하고 있습니다"

        # .pkl / .pickle 파일 존재 확인
        import glob as gl
        for pattern in ["*.pkl", "*.pickle"]:
            found = gl.glob(os.path.join(_SUBMISSION_DIR, "**", pattern), recursive=True)
            assert not found, f"pickle 파일이 존재합니다: {found}"

    def test_persist_integrity(self):
        """저장된 데이터에 isbn, title, author, price 필드가 포함되어 있는지 확인 (5점)"""
        books = self._make_test_books()
        assert books is not None, "테스트용 Book 인스턴스를 생성할 수 없습니다"

        with tempfile.TemporaryDirectory() as tmpdir:
            saved_file = self._do_save(books, tmpdir)
            assert saved_file is not None, "save_books가 파일을 생성하지 못했습니다"
            assert os.path.isfile(saved_file), "저장된 파일이 존재하지 않습니다"

            with open(saved_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            assert content, "저장된 파일이 비어있습니다"

            records = (_parse_jsonl(content)
                       or _parse_json(content)
                       or _parse_csv(content))
            assert records, "저장된 파일을 파싱할 수 없습니다"

            required_keys = {"isbn", "title", "author", "price"}
            has_integrity = False
            for record in records:
                keys_lower = {k.lower() for k in record.keys()}
                if required_keys.issubset(keys_lower):
                    has_integrity = True
                    break

            assert has_integrity, f"저장된 레코드에 필수 키({required_keys})가 누락되었습니다"

"""
db_level3_mission01 — 커밋 이력 DB 분석기 pytest

총 19개 CheckItem을 각각 test 함수로 변환.

패턴:
  - SchemaValidator: sqlite3 직접 연결 (패턴 E)
  - AnalysisValidator / ReportValidator: subprocess + 라인 매칭 (패턴 B)
"""
import os
import sqlite3
import subprocess
import sys
from typing import List

import pytest

# ---------------------------------------------------------------------------
# 임베디드 CSV 데이터
# ---------------------------------------------------------------------------
AUTHORS_CSV = """\
author_id,name,email,team
1,김민수,minsoo@dev.com,backend
2,이지혜,jihye@dev.com,frontend
3,박동현,donghyun@dev.com,backend
4,최유나,yuna@dev.com,frontend
5,황서진,seojin@dev.com,backend
6,정태환,taehwan@dev.com,devops
"""

COMMITS_CSV = """\
hash,message,author_id,parent_hash,branch_name,created_at
a1b2c3d,Initial project setup,1,,main,2026-01-10 09:00:00
b2c3d4e,Add README and gitignore,1,a1b2c3d,main,2026-01-10 09:30:00
c3d4e5f,Setup CI/CD pipeline,6,b2c3d4e,main,2026-01-10 10:00:00
d4e5f6a,Add login page,2,c3d4e5f,feature/login,2026-01-11 09:00:00
e5f6a7b,Add auth middleware,2,d4e5f6a,feature/login,2026-01-11 10:00:00
f6a7b8c,Fix build configuration,6,c3d4e5f,main,2026-01-11 11:00:00
a7b8c9d,Add session management,3,e5f6a7b,feature/login,2026-01-12 09:00:00
b8c9d0e,Update dependencies,1,f6a7b8c,main,2026-01-12 10:00:00
c9d0e1f,Add dashboard layout,4,a7b8c9d,feature/dashboard,2026-01-13 09:00:00
d0e1f2a,Refactor API endpoints,3,b8c9d0e,main,2026-01-13 10:00:00
e1f2a3b,Add chart components,4,c9d0e1f,feature/dashboard,2026-01-13 11:00:00
f2a3b4c,Release v1.0,1,d0e1f2a,main,2026-01-14 09:00:00
"""

BRANCHES_CSV = """\
name,head_hash,created_at
main,f2a3b4c,2026-01-10 09:00:00
feature/login,a7b8c9d,2026-01-11 09:00:00
feature/dashboard,e1f2a3b,2026-01-13 09:00:00
hotfix/urgent,c3d4e5f,2026-01-11 14:00:00
"""

COMMIT_FILES_CSV = """\
id,commit_hash,file_path
1,a1b2c3d,src/main.py
2,a1b2c3d,requirements.txt
3,b2c3d4e,README.md
4,b2c3d4e,.gitignore
5,c3d4e5f,.github/workflows/ci.yml
6,c3d4e5f,Dockerfile
7,c3d4e5f,requirements.txt
8,d4e5f6a,src/pages/login.html
9,d4e5f6a,src/auth/login.py
10,e5f6a7b,src/auth/middleware.py
11,e5f6a7b,src/auth/login.py
12,f6a7b8c,Dockerfile
13,f6a7b8c,requirements.txt
14,a7b8c9d,src/auth/session.py
15,a7b8c9d,src/auth/middleware.py
16,b8c9d0e,requirements.txt
17,c9d0e1f,src/pages/dashboard.html
18,c9d0e1f,src/dashboard/layout.py
19,d0e1f2a,src/api/endpoints.py
20,d0e1f2a,src/api/routes.py
21,e1f2a3b,src/dashboard/charts.py
22,e1f2a3b,src/dashboard/layout.py
23,f2a3b4c,CHANGELOG.md
24,f2a3b4c,src/main.py
25,f2a3b4c,requirements.txt
"""

# 기대 정답값
EXPECTED_MAIN_HISTORY = [
    "f2a3b4c", "d0e1f2a", "b8c9d0e",
    "f6a7b8c", "c3d4e5f", "b2c3d4e", "a1b2c3d",
]


# ---------------------------------------------------------------------------
# CSV 쓰기 헬퍼
# ---------------------------------------------------------------------------
def _write_csv_files(data_dir: str) -> None:
    """CSV 4개를 data_dir에 쓰기"""
    files = {
        "authors.csv": AUTHORS_CSV,
        "commits.csv": COMMITS_CSV,
        "branches.csv": BRANCHES_CSV,
        "commit_files.csv": COMMIT_FILES_CSV,
    }
    for filename, content in files.items():
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


# ---------------------------------------------------------------------------
# fixture: 학생 코드 1회 실행 → (db_path, report_text) 반환
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def db_and_report(tmp_path_factory, submission_dir):
    """tmpdir에 CSV 생성 -> subprocess로 학생 코드 실행 -> (db_path, report_text) 반환"""
    tmpdir = tmp_path_factory.mktemp("db")

    data_dir = str(tmpdir / "data")
    os.makedirs(data_dir)
    _write_csv_files(data_dir)

    db_path = str(tmpdir / "analysis.db")
    report_path = str(tmpdir / "report.txt")
    script_path = os.path.join(submission_dir, "commit_analyzer.py")

    result = subprocess.run(
        [sys.executable, script_path,
         "--data-dir", data_dir,
         "--output", report_path,
         "--db", db_path],
        capture_output=True,
        text=True,
        timeout=15,
        cwd=submission_dir,
    )

    # 실행 실패 시 디버깅 정보 제공
    assert result.returncode == 0, (
        f"학생 코드 실행 실패 (returncode={result.returncode})\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    report_text = ""
    if os.path.isfile(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()

    return db_path, report_text


# ---------------------------------------------------------------------------
# 섹션 추출 헬퍼
# ---------------------------------------------------------------------------
def _find_section_lines(report_lines: List[str], section_header: str) -> List[str]:
    """특정 섹션 헤더 이후의 라인들을 반환 (다음 === 까지)"""
    lines: List[str] = []
    in_section = False
    for line in report_lines:
        if section_header in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("===") and section_header not in line:
                break
            lines.append(line)
    return lines


# ===========================================================================
# SchemaValidator 테스트 (5개) — sqlite3 직접 연결
# ===========================================================================

class TestSchema:
    """DB 스키마 구조 검증 (테이블, FK, 인덱스, 데이터 적재)"""

    def test_db_created(self, db_and_report):
        """analysis.db 생성 + 4개 테이블 존재 (4점)"""
        db_path, _ = db_and_report
        assert os.path.isfile(db_path), "analysis.db 파일이 생성되지 않았습니다"

        conn = sqlite3.connect(db_path)
        try:
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()}
            expected = {"authors", "commits", "branches", "commit_files"}
            assert expected.issubset(tables), (
                f"필수 테이블 누락: {expected - tables}"
            )
        finally:
            conn.close()

    def test_foreign_keys(self, db_and_report):
        """commits 테이블에 FK 제약조건 존재 (4점)"""
        db_path, _ = db_and_report
        conn = sqlite3.connect(db_path)
        try:
            fk_list = conn.execute(
                "PRAGMA foreign_key_list(commits)"
            ).fetchall()
            assert len(fk_list) >= 1, (
                "commits 테이블에 FK 제약조건이 없습니다 "
                "(author_id -> authors, parent_hash -> commits FK 필요)"
            )
        finally:
            conn.close()

    def test_root_commit_null(self, db_and_report):
        """parent_hash NULL 허용 + root commit 존재 — AI 트랩 (5점)"""
        db_path, _ = db_and_report
        conn = sqlite3.connect(db_path)
        try:
            count = conn.execute(
                "SELECT COUNT(*) FROM commits WHERE parent_hash IS NULL"
            ).fetchone()[0]
            assert count == 1, (
                f"parent_hash IS NULL인 커밋이 {count}개입니다 (1개여야 함). "
                "root commit의 parent_hash를 NULL로 저장해야 합니다"
            )
        finally:
            conn.close()

    def test_data_loaded(self, db_and_report):
        """테이블별 행 수 정확성: authors=6, commits=12, branches=4, commit_files=25 (4점)"""
        db_path, _ = db_and_report
        conn = sqlite3.connect(db_path)
        try:
            expected = {
                "authors": 6,
                "commits": 12,
                "branches": 4,
                "commit_files": 25,
            }
            for table, expected_count in expected.items():
                actual = conn.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
                assert actual == expected_count, (
                    f"{table} 테이블: {actual}행 (기대값: {expected_count}행)"
                )
        finally:
            conn.close()

    def test_index_exists(self, db_and_report):
        """최소 1개 사용자 정의 인덱스 존재 (3점)"""
        db_path, _ = db_and_report
        conn = sqlite3.connect(db_path)
        try:
            indexes = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' "
                "AND name NOT LIKE 'sqlite_%'"
            ).fetchall()
            assert len(indexes) >= 1, (
                "사용자 정의 인덱스가 없습니다. "
                "자주 조회하는 컬럼(author_id, branch_name 등)에 인덱스를 생성하세요"
            )
        finally:
            conn.close()


# ===========================================================================
# AnalysisValidator 테스트 (8개) — 리포트 라인 매칭
# ===========================================================================

class TestAnalysis:
    """리포트 분석 섹션 검증 (라인 기반 매칭)"""

    def test_author_commit_count(self, db_and_report):
        """김민수 4 commits 확인 (5점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any("김민수" in line and "4 commits" in line for line in lines)
        assert found, (
            "리포트에서 '김민수'와 '4 commits'가 같은 줄에 없습니다. "
            "작성자별 커밋 수를 정확히 집계하세요 (GROUP BY + COUNT)"
        )

    def test_author_left_join(self, db_and_report):
        """황서진(0 commits) 포함 확인 — AI 트랩 (8점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any("황서진" in line and "0 commits" in line for line in lines)
        assert found, (
            "리포트에서 '황서진'과 '0 commits'가 같은 줄에 없습니다. "
            "커밋이 없는 작성자도 리포트에 포함되어야 합니다 (LEFT JOIN 사용)"
        )

    def test_branch_commit_count(self, db_and_report):
        """main 7 commits 확인 (5점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any("main" in line and "7 commits" in line for line in lines)
        assert found, (
            "리포트에서 'main'과 '7 commits'가 같은 줄에 없습니다. "
            "브랜치별 커밋 수를 정확히 집계하세요"
        )

    def test_branch_no_commits(self, db_and_report):
        """hotfix/urgent 0 commits 포함 — AI 트랩 (6점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any(
            "hotfix/urgent" in line and "0 commits" in line
            for line in lines
        )
        assert found, (
            "리포트에서 'hotfix/urgent'와 '0 commits'가 같은 줄에 없습니다. "
            "자체 커밋이 없는 브랜치도 리포트에 포함되어야 합니다 (LEFT JOIN 사용)"
        )

    def test_distinct_file_count(self, db_and_report):
        """김민수 5 files changed 확인 — AI 트랩 (6점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any("김민수" in line and "5 files" in line for line in lines)
        assert found, (
            "리포트에서 '김민수'와 '5 files'가 같은 줄에 없습니다. "
            "같은 파일이 여러 커밋에서 변경되었을 때 고유 파일 수를 세세요 "
            "(COUNT(DISTINCT file_path))"
        )

    def test_most_changed_files(self, db_and_report):
        """requirements.txt 최다 변경 5 commits 확인 (6점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any(
            "requirements.txt" in line and "5 commits" in line
            for line in lines
        )
        assert found, (
            "리포트에서 'requirements.txt'와 '5 commits'가 같은 줄에 없습니다. "
            "파일별 변경 횟수를 커밋 수 기준으로 집계하세요"
        )

    def test_self_join_parent(self, db_and_report):
        """커밋 히스토리에 root(a1b2c3d) 포함 — AI 트랩 (8점)"""
        _, report_text = db_and_report
        report_lines = report_text.splitlines()
        history_lines = _find_section_lines(report_lines, "Commit History")
        found = any("a1b2c3d" in line for line in history_lines)
        assert found, (
            "Commit History 섹션에 root commit(a1b2c3d)이 없습니다. "
            "커밋 히스토리를 parent_hash로 추적할 때 "
            "root commit(parent=NULL)도 포함해야 합니다"
        )

    def test_history_count(self, db_and_report):
        """main 히스토리 7개 커밋 전부 포함 (1점)"""
        _, report_text = db_and_report
        report_lines = report_text.splitlines()
        history_lines = _find_section_lines(report_lines, "Commit History")
        history_text = "\n".join(history_lines)
        missing = [h for h in EXPECTED_MAIN_HISTORY if h not in history_text]
        assert not missing, (
            f"Commit History 섹션에 누락된 커밋 해시: {missing}. "
            "main 브랜치의 head에서 root까지 모든 커밋이 포함되어야 합니다"
        )


# ===========================================================================
# ReportValidator 테스트 (6개) — 리포트 형식/요약 검증
# ===========================================================================

class TestReport:
    """리포트 형식 및 요약 섹션 검증"""

    def test_report_created(self, db_and_report):
        """리포트 파일 생성 확인 (3점)"""
        _, report_text = db_and_report
        assert report_text is not None and len(report_text.strip()) > 0, (
            "리포트가 비어 있거나 생성되지 않았습니다. "
            "--output 경로에 리포트 텍스트 파일을 생성하세요"
        )

    def test_report_sections(self, db_and_report):
        """5개 섹션 헤더 존재 (4점)"""
        _, report_text = db_and_report
        content = report_text.lower()
        sections = [
            "commit statistics",
            "branch analysis",
            "commit history",
            "file change analysis",
            "summary",
        ]
        found = [s for s in sections if s in content]
        missing = [s for s in sections if s not in content]
        assert len(found) >= 5, (
            f"리포트에 누락된 섹션: {missing}. "
            "Commit Statistics, Branch Analysis, Commit History, "
            "File Change Analysis, Summary 섹션을 포함하세요"
        )

    def test_top_author(self, db_and_report):
        """Most Active Author = 김민수 (4 commits) (7점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any(
            "most active author" in line.lower()
            and "김민수" in line
            and "4" in line
            for line in lines
        )
        assert found, (
            "Summary 섹션에 'Most Active Author'로 '김민수'(4 commits)가 표시되지 않았습니다"
        )

    def test_commit_total(self, db_and_report):
        """Total Commits: 12 확인 (6점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        found = any(
            "total commits" in line.lower() and "12" in line
            for line in lines
        )
        assert found, (
            "리포트에서 'Total Commits'와 '12'가 같은 줄에 없습니다. "
            "전체 커밋 수를 정확히 집계하세요"
        )

    def test_summary_stats(self, db_and_report):
        """요약 3항목 (Author/Branch/File) 존재 (8점)"""
        _, report_text = db_and_report
        content = report_text.lower()
        checks = {
            "Most Active Author": "most active author" in content,
            "Largest Branch": "largest branch" in content,
            "Most Changed File": "most changed file" in content,
        }
        missing = [k for k, v in checks.items() if not v]
        assert not missing, (
            f"Summary 섹션에 누락된 항목: {missing}. "
            "Most Active Author, Largest Branch, Most Changed File을 포함하세요"
        )

    def test_file_ranking_order(self, db_and_report):
        """requirements.txt가 파일 변경 순위 1위 (7점)"""
        _, report_text = db_and_report
        lines = report_text.splitlines()
        in_section = False
        for line in lines:
            lower = line.lower()
            if "file change analysis" in lower or "most changed files" in lower:
                in_section = True
                continue
            if in_section:
                if line.startswith("==="):
                    break
                stripped = line.strip()
                if stripped and ("1." in stripped or "1 " in stripped):
                    assert "requirements.txt" in stripped, (
                        f"파일 변경 순위 1위가 requirements.txt가 아닙니다: '{stripped}'. "
                        "파일 변경 횟수를 내림차순 정렬하세요"
                    )
                    return
        # 섹션 내에서 1위 항목을 찾지 못한 경우
        pytest.fail(
            "File Change Analysis 섹션에서 순위 1위 항목을 찾을 수 없습니다"
        )

# commit_analyzer.py
import argparse
import csv
import os
import sqlite3


def create_tables(conn: sqlite3.Connection) -> None:
    """4개 테이블(authors, commits, branches, commit_files) 생성"""
    pass  # TODO


def load_csv(conn: sqlite3.Connection, data_dir: str) -> None:
    """CSV 4개 파일을 읽어 DB에 INSERT"""
    pass  # TODO


def author_contributions(conn: sqlite3.Connection):
    """작성자별 커밋 수 + 변경 파일 수 조회"""
    pass  # TODO


def branch_analysis(conn: sqlite3.Connection):
    """브랜치별 커밋 수 조회"""
    pass  # TODO


def commit_history_main(conn: sqlite3.Connection):
    """main 브랜치 커밋 히스토리 (head -> root)"""
    pass  # TODO


def most_changed_files(conn: sqlite3.Connection):
    """파일별 변경 횟수 조회"""
    pass  # TODO


def generate_report(conn: sqlite3.Connection) -> str:
    """분석 결과를 텍스트 리포트로 생성"""
    pass  # TODO


def main():
    parser = argparse.ArgumentParser(description="커밋 이력 DB 분석기")
    parser.add_argument("--data-dir", required=True, help="CSV 데이터 디렉토리")
    parser.add_argument("--output", required=True, help="리포트 출력 경로")
    parser.add_argument("--db", required=True, help="SQLite DB 파일 경로")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")

    create_tables(conn)
    load_csv(conn, args.data_dir)

    report = generate_report(conn)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    conn.close()


if __name__ == "__main__":
    main()

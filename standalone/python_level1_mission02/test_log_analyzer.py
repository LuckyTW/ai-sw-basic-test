"""
python_level1_mission02 — 서버 접근 로그 분석기 standalone pytest

원본 Validator: plugins/python/validators/log_analyzer_validator.py
7개 CheckItem을 각각 test 함수로 변환.
패턴: subprocess + tmpdir (패턴 B)
"""
import os
import subprocess
import sys

import pytest

# ---------------------------------------------------------------------------
# 함정 포함 CSV 데이터 (24행) — Validator의 TRAP_CSV 그대로 임베드
# ---------------------------------------------------------------------------
TRAP_CSV_HEADER = "timestamp,ip,method,endpoint,status_code,response_time_ms"
TRAP_CSV_ROWS = [
    ("2025-03-15T09:00:00", "192.168.1.1", "GET", "/api/users", "200", "45"),
    ("2025-03-15T09:01:30", "", "GET", "/api/health", "200", "10"),
    ("2025-03-15T09:01:35", "10.0.0.5", "GET", "/api/health", "100", "2"),
    ("2025-03-15T09:02:00", "192.168.1.1", "POST", "/api/users", "201", "38"),
    ("2025-03-15T09:02:10", "10.0.0.5", "GET", "/api/products", "200", "52"),
    ("2025-03-15T09:02:20", "172.16.0.10", "GET", "/api/users", "200", "41"),
    ("2025-03-15T09:02:30", "172.16.0.10", "GET", "/api/products", "200", "33.7"),
    ("2025-03-15T09:03:00", "192.168.1.1", "DELETE", "/api/users", "403", "12"),
    ("2025-03-15T09:03:30", "192.168.2.20", "GET", "/api/orders", "500", "5120"),
    ("2025-03-15T09:04:00", "10.0.0.5", "PUT", "/api/products", "200", "67"),
    ("2025-03-15T09:04:30", "192.168.1.1", "GET", "/api/health", "200", "3"),
    ("2025-03-15T09:05:00", "172.16.0.10", "GET", "/api/orders", "301", "25"),
    ("2025-03-15T09:05:30", "10.0.0.99", "GET", "/api/users", "404", "8"),
    ("2025-03-15T09:06:00", "192.168.1.1", "GET", "/api/products", "200", "55"),
    ("2025-03-15T09:06:30", "10.0.0.5", "POST", "/api/orders", "201", "310"),
    ("2025-03-15T09:07:00", "172.16.0.10", "GET", "/api/health", "200", "4"),
    ("2025-03-15T09:07:30", "192.168.2.20", "GET", "/api/products", "500", "3200"),
    ("2025-03-15T09:08:00", "10.0.0.5", "GET", "/api/users", "200", "29"),
    ("2025-03-15T09:08:30", "192.168.1.1", "GET", "/api/orders", "500", "4500"),
    ("2025-03-15T09:09:00", "10.0.0.99", "POST", "/api/users", "201", "42"),
    ("2025-03-15T09:09:30", "172.16.0.10", "GET", "/api/products", "200", "61"),
    ("2025-03-15T09:10:00", "10.0.0.5", "GET", "/api/health", "200", "5"),
    ("2025-03-15T09:10:30", "192.168.2.20", "GET", "/api/users", "200", "37"),
    ("2025-03-15T09:11:00", "10.0.0.99", "GET", "/api/products", "200", "48"),
]

# 기대 정답값 (Validator에서 추출)
EXPECTED_TOP_IPS = [
    ("192.168.1.1", 6),
    ("10.0.0.5", 6),
    ("172.16.0.10", 5),
    ("192.168.2.20", 3),
    ("10.0.0.99", 3),
]

EXPECTED_STATUS = {
    "1xx": 4.2,
    "2xx": 70.8,
    "3xx": 4.2,
    "4xx": 8.3,
    "5xx": 12.5,
}

EXPECTED_SLOW_ENDPOINTS = [
    ("/api/orders", 2488.8),
    ("/api/products", 502.4),
    ("/api/users", 31.5),
]

# ---------------------------------------------------------------------------
# 제출물 경로 (이 테스트 파일과 같은 디렉토리)
# ---------------------------------------------------------------------------
SUBMISSION_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(SUBMISSION_DIR, "log_analyzer.py")


# ---------------------------------------------------------------------------
# fixture: 학생 코드 1회 실행, report 텍스트 반환
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def report_content(tmp_path_factory):
    """tmpdir에 CSV 생성 → subprocess로 학생 코드 실행 → report.txt 읽기"""
    tmp_path = tmp_path_factory.mktemp("log_analyzer")

    csv_path = str(tmp_path / "access_log.csv")
    report_path = str(tmp_path / "report.txt")

    # 함정 포함 CSV 쓰기
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(TRAP_CSV_HEADER + "\n")
        for row in TRAP_CSV_ROWS:
            f.write(",".join(row) + "\n")

    # subprocess로 학생 코드 실행
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH,
         "--log", csv_path,
         "--output", report_path],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=SUBMISSION_DIR,
    )

    # 실행 실패 시 디버깅 정보 제공
    assert result.returncode == 0, (
        f"학생 코드 실행 실패 (returncode={result.returncode})\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    # report.txt 읽기
    assert os.path.isfile(report_path), "report.txt가 생성되지 않았습니다"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    return content


# ---------------------------------------------------------------------------
# 섹션 추출 헬퍼 (Validator._extract_section 재현)
# ---------------------------------------------------------------------------
def _extract_section(report_content, keywords):
    """리포트에서 특정 키워드를 포함하는 섹션을 추출."""
    lines = report_content.split("\n")
    section_start = -1

    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(kw.lower() in line_lower for kw in keywords):
            section_start = i
            break

    if section_start == -1:
        return None

    section_lines = [lines[section_start]]
    for i in range(section_start + 1, len(lines)):
        line = lines[i]
        if line.startswith("===") or line.startswith("---"):
            break
        section_lines.append(line)

    return "\n".join(section_lines)


# ---------------------------------------------------------------------------
# 7개 테스트 함수
# ---------------------------------------------------------------------------

def test_csv_parse(report_content):
    """CSV 정상 파싱 + report.txt 생성 확인 (15점)"""
    assert report_content is not None
    assert len(report_content.strip()) > 0


def test_top_ips(report_content):
    """IP별 접근 횟수 TOP 5가 정확한지 확인 (15점)

    빈 IP 행은 제외하고 IP별 접근 횟수를 집계.
    각 IP와 count가 같은 라인에 존재해야 함.
    """
    lines = report_content.split("\n")
    for ip, count in EXPECTED_TOP_IPS:
        found = any(ip in line and str(count) in line for line in lines)
        assert found, f"IP={ip}, count={count} 조합이 리포트에 없습니다"


def test_ip_order(report_content):
    """동점 IP 정렬 순서 확인 — AI 트랩 (8점)

    접근 횟수 내림차순, 동점 시 IP 주소도 내림차순.
    192.168.1.1(6)이 10.0.0.5(6)보다 먼저,
    192.168.2.20(3)이 10.0.0.99(3)보다 먼저 나와야 함.
    """
    pos_192_1 = report_content.find("192.168.1.1")
    pos_10_5 = report_content.find("10.0.0.5")
    pos_192_20 = report_content.find("192.168.2.20")
    pos_10_99 = report_content.find("10.0.0.99")

    assert pos_192_1 != -1, "192.168.1.1이 리포트에 없습니다"
    assert pos_10_5 != -1, "10.0.0.5가 리포트에 없습니다"
    assert pos_192_20 != -1, "192.168.2.20이 리포트에 없습니다"
    assert pos_10_99 != -1, "10.0.0.99가 리포트에 없습니다"

    assert pos_192_1 < pos_10_5, (
        "192.168.1.1이 10.0.0.5보다 먼저 나와야 합니다 (동점 IP 내림차순)"
    )
    assert pos_192_20 < pos_10_99, (
        "192.168.2.20이 10.0.0.99보다 먼저 나와야 합니다 (동점 IP 내림차순)"
    )


def test_status_ratio(report_content):
    """HTTP 상태코드 그룹별 비율 확인 — AI 트랩 (10점)

    1xx~5xx 모든 그룹을 출력하고, 전체 행 수(24행) 기준으로 비율 계산.
    AI 트랩: 1xx 상태코드를 무시하여 출력에 포함하지 않는 실수.
    라인 기반 매칭으로 1xx:4.2%와 3xx:4.2%를 구별.
    """
    lines = report_content.split("\n")
    for group, ratio in EXPECTED_STATUS.items():
        ratio_str = f"{ratio:.1f}"
        found = any(group in line and ratio_str in line for line in lines)
        assert found, (
            f"{group}: {ratio_str}% 조합이 리포트에 없습니다"
        )


def test_slow_order(report_content):
    """느린 엔드포인트 TOP 3 순서 확인 (20점)

    엔드포인트별 평균 응답시간 내림차순:
    /api/orders > /api/products > /api/users
    엔드포인트 섹션 내에서만 검색하여 오탐 방지.
    """
    section = _extract_section(
        report_content, ["endpoint", "엔드포인트", "slow", "response"]
    )
    search_text = section if section else report_content

    positions = []
    for endpoint, _ in EXPECTED_SLOW_ENDPOINTS:
        pos = search_text.find(endpoint)
        assert pos != -1, f"엔드포인트 {endpoint}가 섹션에 없습니다"
        positions.append(pos)

    assert positions[0] < positions[1] < positions[2], (
        f"엔드포인트 순서가 올바르지 않습니다: "
        f"/api/orders({positions[0]}) < /api/products({positions[1]}) < /api/users({positions[2]})"
    )


def test_report_sections(report_content):
    """리포트 3개 섹션 존재 확인 (25점)

    IP 접근 횟수, 상태코드 비율, 느린 엔드포인트 섹션이 모두 포함되어야 함.
    """
    report_lower = report_content.lower()

    has_ip_section = "ip" in report_lower and (
        "top" in report_lower or "접근" in report_lower
    )
    has_status_section = (
        "status" in report_lower or "상태" in report_lower
    ) and "%" in report_content
    has_endpoint_section = (
        "endpoint" in report_lower or "엔드포인트" in report_lower
    ) and "ms" in report_lower

    assert has_ip_section, "IP 접근 횟수 섹션이 없습니다"
    assert has_status_section, "상태코드 비율 섹션이 없습니다"
    assert has_endpoint_section, "엔드포인트 섹션이 없습니다"


def test_slow_values(report_content):
    """엔드포인트 평균 응답시간 수치 정확성 확인 — AI 트랩 (7점)

    AI 트랩: 소수점 response_time(33.7)을 int로 변환하여 평균 오차 발생.
    3개 핵심 수치가 모두 리포트에 존재해야 함.
    """
    expected_values = ["2488.8", "502.4", "31.5"]
    for value in expected_values:
        assert value in report_content, (
            f"평균 응답시간 {value}ms가 리포트에 없습니다"
        )

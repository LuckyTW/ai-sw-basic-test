"""
linux_level2_mission01 -- 리눅스 서버 보안 감사 도구 pytest

검증 항목 7개를 각각 pytest test 함수로 변환.
패턴: subprocess + tmpdir (설정 파일 6개 생성 -> 학생 코드 실행 -> 리포트 라인 매칭)
"""

import os
import re
import subprocess
import sys

import pytest

# ── 트랩 입력 파일 6개 ──

TRAP_SSHD_CONFIG = """\
Port 20022
PermitRootLogin prohibit-password
PasswordAuthentication yes
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers agent-admin agent-dev
"""

TRAP_UFW_STATUS = """\
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW IN    Anywhere
15034/tcp                  ALLOW IN    Anywhere
23/tcp                     ALLOW IN    Anywhere
20022/tcp (v6)             ALLOW IN    Anywhere (v6)
15034/tcp (v6)             ALLOW IN    Anywhere (v6)
23/tcp (v6)                ALLOW IN    Anywhere (v6)
"""

TRAP_ACCOUNTS_CSV = """\
username,uid,groups,home,shell
agent-admin,1001,agent-common;agent-core,/home/agent-admin,/bin/bash
agent-dev,1002,agent-common;agent-core,/home/agent-dev,/bin/bash
agent-test,1003,agent-common;agent-core,/home/agent-test,/bin/bash
"""

TRAP_DIRECTORIES_CSV = """\
path,owner,group,octal_permission
/home/agent-admin/agent-app,agent-admin,agent-admin,755
/home/agent-admin/agent-app/upload_files,agent-admin,agent-common,775
/home/agent-admin/agent-app/api_keys,agent-admin,agent-common,775
/var/log/agent-app,agent-admin,agent-core,770
/home/agent-admin/agent-app/bin,agent-admin,agent-admin,755
"""

TRAP_MONITOR_LOG = """\
[2025-12-24 09:56:01] PID:48291 CPU:24.8% MEM:5.1% DISK:45G
[2025-12-24 09:57:01] PID:48291 CPU:25.0% MEM:5.1% DISK:45G
[INVALID] This line has bad format
[2025-12-24 09:58:01] PID:48291 CPU:25.2% MEM:5.2% DISK:45G
[2025-12-24 09:59:01] PID:48291 CPU:25.1% MEM:5.2% DISK:45G
[2025-12-24 10:00:01] PID:48291 CPU:25.3% MEM:5.2% DISK:45G
[2025-12-24 10:01:01] PID:48291 CPU:92.5% MEM:85.3% DISK:12G
"""

TRAP_CRONTAB = """\
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor.log 2>&1
0 2 * * 0 /home/agent-admin/agent-app/bin/backup.sh
0 0 * * * find /var/log/agent-app/archive -name "*.gz" -mtime +30 -delete
"""

# ── 기대 정답값 ──
EXPECTED_CPU_AVG = 36.32
CPU_TOLERANCE = 0.5

# ── 설정 파일 매핑 ──
TRAP_FILES = {
    "sshd_config": TRAP_SSHD_CONFIG,
    "ufw_status.txt": TRAP_UFW_STATUS,
    "accounts.csv": TRAP_ACCOUNTS_CSV,
    "directories.csv": TRAP_DIRECTORIES_CSV,
    "monitor.log": TRAP_MONITOR_LOG,
    "crontab.txt": TRAP_CRONTAB,
}


@pytest.fixture(scope="module")
def report_content(tmp_path_factory, submission_dir):
    """설정 파일 6개를 tmpdir에 쓰고, 학생 코드를 실행하여 리포트 내용을 반환"""
    tmp_path = tmp_path_factory.mktemp("linux_audit")

    # 트랩 파일 6개 쓰기
    for filename, content in TRAP_FILES.items():
        filepath = tmp_path / filename
        filepath.write_text(content, encoding="utf-8")

    report_path = tmp_path / "report.txt"
    script_path = os.path.join(submission_dir, "auditor.py")

    # subprocess로 학생 코드 실행
    result = subprocess.run(
        [
            sys.executable,
            script_path,
            "--config-dir",
            str(tmp_path),
            "--output",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=submission_dir,
    )

    assert result.returncode == 0, f"학생 코드 실행 실패: {result.stderr}"
    assert report_path.is_file(), "report.txt가 생성되지 않음"

    return report_path.read_text(encoding="utf-8")


# ── 7개 테스트 함수 ──


def test_config_parse(report_content):
    """설정 파일 파싱 + report.txt 생성 확인 (10점)"""
    assert report_content is not None
    assert len(report_content.strip()) > 0, "report.txt가 비어있음"


def test_ssh_audit(report_content):
    """SSH 보안 감사: PermitRootLogin 취약점 탐지 (15점, AI 트랩)"""
    topic_keywords = ["permitrootlogin", "prohibit-password", "root login", "루트 로그인"]
    vuln_keywords = ["취약", "위험", "vulnerable", "unsafe", "warning", "주의", "경고"]

    found = False
    for line in report_content.split("\n"):
        line_lower = line.lower()
        if any(kw in line_lower for kw in topic_keywords):
            if any(kw in line_lower for kw in vuln_keywords):
                found = True
                break

    assert found, (
        "PermitRootLogin prohibit-password를 취약으로 판정하지 않음. "
        "'no'만 안전하며, prohibit-password는 키 인증 루트 로그인을 허용하므로 취약합니다."
    )


def test_firewall_audit(report_content):
    """방화벽 감사: 위험 포트(23/tcp Telnet) 탐지 (15점, AI 트랩)"""
    vuln_keywords = [
        "취약", "위험", "차단", "block", "deny", "vulnerable",
        "unsafe", "warning", "주의", "경고", "close",
    ]

    found = False
    for line in report_content.split("\n"):
        line_lower = line.lower()
        if ("23/" in line_lower or "telnet" in line_lower) and (
            "tcp" in line_lower or "telnet" in line_lower
        ):
            if any(kw in line_lower for kw in vuln_keywords):
                found = True
                break

    assert found, (
        "23/tcp(Telnet) 위험 포트를 탐지하지 않음. "
        "Telnet은 암호화 없는 원격 접속 프로토콜로 즉시 차단이 필요합니다."
    )


def test_account_audit(report_content):
    """계정 감사: agent-test의 agent-core 그룹 RBAC 위반 탐지 (15점, AI 트랩)"""
    vuln_keywords = [
        "위반", "취약", "violation", "vulnerable", "unauthorized",
        "unnecessary", "불필요", "위험", "warning", "주의", "경고",
        "제거", "remove",
    ]

    found = False
    for line in report_content.split("\n"):
        line_lower = line.lower()
        if "agent-test" in line_lower:
            if any(kw in line_lower for kw in vuln_keywords):
                found = True
                break

    assert found, (
        "agent-test의 agent-core 그룹 포함 RBAC 위반을 탐지하지 않음. "
        "테스트 계정이 핵심 운영 그룹에 포함되면 최소 권한 원칙 위반입니다."
    )


def test_permission_audit(report_content):
    """권한 감사: api_keys 디렉토리 775+agent-common 탐지 (15점, AI 트랩)"""
    vuln_keywords = [
        "취약", "위험", "vulnerable", "unsafe", "warning",
        "주의", "경고", "과도", "excessive",
    ]

    found = False
    for line in report_content.split("\n"):
        line_lower = line.lower()
        if "api_keys" in line_lower or "api-keys" in line_lower:
            if any(kw in line_lower for kw in vuln_keywords):
                found = True
                break

    assert found, (
        "api_keys 디렉토리의 775+agent-common 권한 위반을 탐지하지 않음. "
        "민감 데이터 디렉토리에 광범위 그룹 쓰기 권한이 있으면 보안 위험입니다."
    )


def test_log_stats(report_content):
    """모니터링 로그 통계: CPU 평균값 정확성 (15점)"""
    cpu_section = ""
    for line in report_content.split("\n"):
        if "cpu" in line.lower() and (
            "평균" in line.lower()
            or "avg" in line.lower()
            or "average" in line.lower()
            or "mean" in line.lower()
        ):
            cpu_section = line
            break

    if not cpu_section:
        cpu_section = report_content

    numbers = re.findall(r"\d+\.\d+", cpu_section)
    found = False
    for num_str in numbers:
        num = float(num_str)
        if abs(num - EXPECTED_CPU_AVG) <= CPU_TOLERANCE:
            found = True
            break

    assert found, (
        f"CPU 평균값이 {EXPECTED_CPU_AVG}% (+-{CPU_TOLERANCE}) 범위 내에 없음. "
        "잘못된 형식의 로그 줄은 건너뛰고 유효한 줄만으로 통계를 계산해야 합니다."
    )


def test_report_sections(report_content):
    """리포트 5개 섹션(SSH, 방화벽, 계정, 권한, 로그) 포함 확인 (15점)"""
    report_lower = report_content.lower()

    section_checks = [
        "ssh" in report_lower,
        any(kw in report_lower for kw in ["방화벽", "firewall", "ufw"]),
        any(kw in report_lower for kw in ["계정", "account", "user"]),
        any(kw in report_lower for kw in ["권한", "permission", "directory"]),
        any(kw in report_lower for kw in ["로그", "log", "monitor"]),
    ]

    count = sum(section_checks)
    assert count >= 4, (
        f"리포트에 {count}/5 섹션만 포함됨. "
        "SSH, 방화벽, 계정, 권한, 로그 관련 섹션을 4개 이상 포함해야 합니다."
    )

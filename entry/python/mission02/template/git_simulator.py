# git_simulator.py — Git 워크플로우 시뮬레이터
# TODO 표시된 3개 메서드만 구현하세요. 나머지 코드는 수정하지 마세요.


class GitSimulator:
    def __init__(self):
        self.staged = []          # 스테이징된 파일 목록
        self.commits = []         # 커밋 이력 (list of dict)
        self.branch = "main"     # 현재 브랜치
        self.branches = ["main"] # 브랜치 목록

    def add(self, filename):
        """파일을 스테이징 영역에 추가 (이미 있으면 무시)"""
        # TODO: 여기를 구현하세요
        pass

    def commit(self, message):
        """staged가 비어있으면 'nothing to commit' 반환
        아니면 commits에 {"message": message, "files": staged 복사본, "branch": self.branch} 추가,
        staged 초기화 후 'committed: {message}' 반환
        """
        # TODO: 여기를 구현하세요
        pass

    def log(self):
        """커밋 이력을 역순(최신 먼저)으로 반환 (원본 불변)"""
        return list(reversed(self.commits))

    def create_branch(self, name):
        """브랜치 생성 — 이미 존재하면 False, 성공하면 True"""
        if name in self.branches:
            return False
        self.branches.append(name)
        return True

    def switch(self, name):
        """브랜치 전환 — 존재하지 않으면 False, 성공하면 True"""
        if name not in self.branches:
            return False
        self.branch = name
        return True

    def status(self):
        """'브랜치: {branch}, 스테이징: {N}개, 커밋: {M}개' 형식 반환"""
        # TODO: 여기를 구현하세요
        pass


def summarize(simulator):
    """전체 현황 요약: '총 {N}개 커밋 | 브랜치: {M}개 | 파일: {K}개'"""
    n = len(simulator.commits)
    m = len(simulator.branches)
    all_files = []
    for c in simulator.commits:
        for f in c["files"]:
            if f not in all_files:
                all_files.append(f)
    k = len(all_files)
    return f"총 {n}개 커밋 | 브랜치: {m}개 | 파일: {k}개"

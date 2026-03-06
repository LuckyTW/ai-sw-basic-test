# git_simulator.py


class GitSimulator:
    def __init__(self):
        self.staged = []
        self.commits = []
        self.branch = "main"
        self.branches = ["main"]

    def add(self, filename):
        """파일을 스테이징 영역에 추가 (이미 있으면 무시)"""
        pass  # TODO

    def commit(self, message):
        """커밋 생성. 'nothing to commit' 또는 'committed: {message}' 반환"""
        pass  # TODO

    def log(self):
        """커밋 이력을 역순(최신 먼저)으로 반환"""
        return list(reversed(self.commits))

    def create_branch(self, name):
        """브랜치 생성 - 이미 존재하면 False, 성공하면 True"""
        if name in self.branches:
            return False
        self.branches.append(name)
        return True

    def switch(self, name):
        """브랜치 전환 - 존재하지 않으면 False, 성공하면 True"""
        if name not in self.branches:
            return False
        self.branch = name
        return True

    def status(self):
        """'브랜치: {branch}, 스테이징: {N}개, 커밋: {M}개' 형식 반환"""
        pass  # TODO


def summarize(simulator):
    """'총 {N}개 커밋 | 브랜치: {M}개 | 파일: {K}개' 형식 반환"""
    n = len(simulator.commits)
    m = len(simulator.branches)
    all_files = []
    for c in simulator.commits:
        for f in c["files"]:
            if f not in all_files:
                all_files.append(f)
    k = len(all_files)
    return f"총 {n}개 커밋 | 브랜치: {m}개 | 파일: {k}개"

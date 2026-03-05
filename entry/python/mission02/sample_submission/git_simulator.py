# git_simulator.py - Git 워크플로우 시뮬레이터 (정답)


class GitSimulator:
    def __init__(self):
        self.staged = []
        self.commits = []
        self.branch = "main"
        self.branches = ["main"]

    def add(self, filename):
        if filename not in self.staged:
            self.staged.append(filename)

    def commit(self, message):
        if not self.staged:
            return "nothing to commit"
        commit_record = {
            "message": message,
            "files": list(self.staged),
            "branch": self.branch,
        }
        self.commits.append(commit_record)
        self.staged = []
        return f"committed: {message}"

    def log(self):
        return list(reversed(self.commits))

    def create_branch(self, name):
        if name in self.branches:
            return False
        self.branches.append(name)
        return True

    def switch(self, name):
        if name not in self.branches:
            return False
        self.branch = name
        return True

    def status(self):
        return f"브랜치: {self.branch}, 스테이징: {len(self.staged)}개, 커밋: {len(self.commits)}개"


def summarize(simulator):
    n = len(simulator.commits)
    m = len(simulator.branches)
    all_files = []
    for c in simulator.commits:
        for f in c["files"]:
            if f not in all_files:
                all_files.append(f)
    k = len(all_files)
    return f"총 {n}개 커밋 | 브랜치: {m}개 | 파일: {k}개"

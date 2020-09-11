import shlex, subprocess, os
from typing import Tuple, List, NewType


Branch = NewType('Branch', str)
Remote = NewType('Remote', str)


class Shell:
    encoding = 'utf-8'

    def __init__(self, working_directory):
        self.working_directory = working_directory

    def run(self, cmd: str) -> Tuple[bool, str]:
        completed_process = subprocess.run(shlex.split(cmd), capture_output=True, cwd=self.working_directory)
        if completed_process.returncode == 0:
            return True, completed_process.stdout.decode(self.encoding)
        else:
            return False, completed_process.stderr.decode(self.encoding)


class Git:

    def __init__(self, repo, shell=None):
        if shell is None:
            self._shell = Shell(working_directory=repo)
        self.repo = os.path.abspath(repo)

    def init(self):
        success, out = self._shell.run('git init')
        return out

    def checkout(self, branch, new_branch=False):
        new_branch_flag = '-b' if new_branch else ''
        success, out = self._shell.run(f'git checkout {new_branch_flag} {branch}')
        return out

    def branch(self) -> List[Branch]:
        '''First branch in list is the current branch.'''
        success, out = self._shell.run('git branch')
        if success:
            branches = out.strip().split('\n')
            branches.sort(key=lambda branch: (not branch.startswith('* '), branch))
            branches[0] = branches[0].replace('* ', '')
            return [branch.strip() for branch in branches]
        raise OSError(out)

    def remote(self) -> List[Remote]:
        success, out = self._shell.run('git remote')
        if success:
            return out.strip().split('\n')
        raise OSError(out)

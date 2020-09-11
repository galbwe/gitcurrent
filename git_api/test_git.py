import unittest
import os
import tempfile

from .git import Git, Shell


class GitApiTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.git_repo = tempfile.TemporaryDirectory()
        self.shell = Shell(working_directory=self.git_repo.name)

    def tearDown(self):
        self.git_repo.cleanup()
        super().tearDown()


class TestShell(GitApiTestCase):

    def setUp(self):
        super().setUp()
        repo_name = os.path.abspath(self.git_repo.name)
        open(os.path.join(repo_name, 'file-01'), 'a').close()
        open(os.path.join(repo_name, 'file-02'), 'a').close()
        open(os.path.join(repo_name, 'file-03'), 'a').close()

    def test_ls(self):
        out = self.shell.run('ls')
        expected = (True, 'file-01\nfile-02\nfile-03\n')
        self.assertEqual(out, expected, msg='Expected %s, found %s' % (expected, out))

    def test_touch(self):
        expected = (True, '')
        out = self.shell.run('touch file-04')
        self.assertEqual(out, expected, msg='Expected %s, found %s' % (expected, out))
        expected = (True, 'file-01\nfile-02\nfile-03\nfile-04\n')
        out = self.shell.run('ls')
        self.assertEqual(out, expected, msg='Expected %s, found %s' % (expected, out))


class TestGit(GitApiTestCase):

    def setUp(self):
        super().setUp()
        repo_name = os.path.abspath(self.git_repo.name)
        open(os.path.join(repo_name, 'file-01'), 'a').close()
        open(os.path.join(repo_name, 'file-02'), 'a').close()
        open(os.path.join(repo_name, 'file-03'), 'a').close()
        self.shell.run('git init')
        self.shell.run('git add *')
        self.shell.run('git commit -m "Initial commit"')
        self.shell.run('git checkout -b branch-01')
        self.shell.run('git checkout -b branch-02')
        self.shell.run('git checkout -b branch-03')
        self.shell.run('git checkout master')

        self.git = Git(self.shell)

    def test_branch(self):
        expected = ['master', 'branch-01', 'branch-02', 'branch-03']
        out = self.git.branch()
        self.assertEqual(expected, out, 'Expected %s, but found %s.' % (expected, out))

    def test_checkout_existing_branch(self):
        self.git.checkout('branch-02')
        expected = ['branch-02', 'branch-01', 'branch-03', 'master']
        out = self.git.branch()
        self.assertEqual(expected, out, 'Expected %s, but found %s.' % (expected, out))

    def test_checkout_new_branch(self):
        self.git.checkout('branch-04')
        expected = ['branch-04', 'branch-01', 'branch-02' 'branch-03', 'master']
        out = self.git.branch()
        self.assertEqual(expected, out, 'Expected %s, but found %s.' % (expected, out))


if __name__ == '__main__':
    unittest.main()
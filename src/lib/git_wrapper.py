import git
from datetime import datetime

class GitWrapper:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

    def get_commits(self, revision_range=None):
        """
        Iterate through commits in the repository.
        :param revision_range: A string representing the revision range (e.g., 'HEAD~5..HEAD', 'main').
                               If None, iterates through all commits on the current branch.
        :return: An iterator of GitPython Commit objects.
        """
        if revision_range:
            return self.repo.iter_commits(revision_range)
        else:
            return self.repo.iter_commits()

    def get_reflog(self):
        """
        Access the reflog of the repository.
        :return: A list of GitPython RefLogEntry objects.
        """
        return self.repo.head.ref.log()

    def get_commit_diff(self, commit):
        """
        Get the diff of a specific commit.
        :param commit: A GitPython Commit object.
        :return: A string representing the diff.
        """
        # For the initial commit, there's no parent to diff against
        if len(commit.parents) == 0:
            # Diff against an empty tree for the very first commit
            return commit.tree.diff(self.repo.tree('4b825dc642cb6eb9a060e54bf8d69288fbee4904'))
        else:
            return commit.diff(commit.parents[0])

    def get_branch_head_commit(self, branch_name):
        """
        Get the head commit of a specific branch.
        :param branch_name: The name of the branch.
        :return: A GitPython Commit object.
        """
        return self.repo.commit(branch_name)

    def get_all_branches(self):
        """
        Get all local branches.
        :return: A list of GitPython Head objects.
        """
        return self.repo.heads

    def get_current_branch(self):
        """
        Get the currently active branch.
        :return: A GitPython Head object.
        """
        return self.repo.active_branch

    def get_commit_by_hexsha(self, hexsha):
        """
        Get a commit object by its hexadecimal SHA.
        :param hexsha: The hexadecimal SHA of the commit.
        :return: A GitPython Commit object.
        """
        return self.repo.commit(hexsha)
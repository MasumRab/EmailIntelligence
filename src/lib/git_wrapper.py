import git

class GitWrapper:
    """
    A wrapper for GitPython to handle basic git operations.
    """

    def __init__(self, repo_path="."):
        """
        Initializes the GitWrapper.

        :param repo_path: The path to the git repository.
        """
        self.repo = git.Repo(repo_path)

    def get_current_branch(self):
        """
        Gets the name of the current branch.

        :return: The name of the current branch.
        """
        return self.repo.active_branch.name

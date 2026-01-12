def clone_or_pull(self, repo_url: str, branch="main") -> str:
        """
        
        
        :param repo_url: 仓库的url
        :param branch: 要操作的分支名称，默认为 "main"
        :return: 仓库在本地存储的完整路径
        """
        repo_path = self.get_repo_path(repo_url)
        
        env = os.environ.copy()
        if self.proxy:
            env["http_proxy"] = self.proxy
            env["https_proxy"] = self.proxy

        try:
            if not os.path.exists(repo_path):
                print("Local repository not found. Cloning...")

                os.makedirs(os.path.dirname(repo_path), exist_ok=True)
                Repo.clone_from(
                    repo_url,
                    repo_path,
                    branch=branch,
                    depth=self.depth,
                    env=env
                )
            else:
                print("Local git repository exists. Updating...")
                repo = Repo(repo_path)
                if repo.active_branch.name != branch:
                    repo.git.checkout(branch)
                repo.git.pull(env=env)

                print("Update Successful!")
        
        except (GitCommandError, InvalidGitRepositoryError) as e:
            raise RepoError(f"Git 仓库获取失败: {e}")

        return repo_path

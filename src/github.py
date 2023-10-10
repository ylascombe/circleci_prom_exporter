import requests
from src.common import ApiCommon, Config

class GitHubOrganization:
    def __init__(self, org) -> None:
        self.org = org
        self.api = ApiCommon()
        self.config = Config()

    def repositories(self):
        """List repositories hosted in org
        """
        repositories = []
        has_more_page = True
        page = 1

        while has_more_page:
            data = self.api.http_get_as_json(
                url=f"https://api.github.com/orgs/{self.org}/repos",
                params={
                    'page': page,
                    'per_page': 100
                },
                headers={
                    'Accept': 'application/vnd.github+json',
                    'Authorization': f'Bearer {self.config.github_token}',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
            )

            for repo in data:
                repositories.append(repo['full_name'])
            page +=1

            has_more_page = len(data) == 100

        print(f'{len(repositories)} have been found on {self.org} organization')
        return repositories

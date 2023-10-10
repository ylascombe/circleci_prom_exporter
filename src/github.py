import requests
from src.common import Common

class GitHubOrganization:
    def repositories(self):
        """List repositories hosted in org
        """
        repositories = []
        has_more_page = True
        page = 1

        while has_more_page:
            data = Common.http_get_as_json(
                url=f"https://api.github.com/orgs{org}/repos",
                params={
                    'page': page,
                    'per_page': 100
                }
            )

            for repo in data:
                repositories.append(repo)
            page +=1

            has_more_page = len(data) == 100
        return repositories

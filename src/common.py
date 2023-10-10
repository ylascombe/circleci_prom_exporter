import requests
import os
from typing import Dict, Any, Tuple

class InvalidConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Config:
    def __init__(self) -> None:
        self.github_user = os.getenv('GITHUB_USER')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.circleci_token = os.getenv('CIRCLECI_TOKEN')
        orgs = os.getenv('GITHUB_ORGANIZATIONS')

        if orgs is None:
            raise InvalidConfigException('missing GITHUB_ORGANIZATIONS env var')

        self.organizations = orgs.split(',')

    def github_auth(self) -> Tuple[str, str]:
        """Return github auth fulfilled with creds
        """
        return (self.github_user, self.github_token)

class ApiCommon:

    def __init__(self) -> None:
        # self.config = config
        pass

    def http_get_as_json(
            self,
            url:str,
            auth: Tuple[str, str] = None,
            headers: Dict[str, str] = None,
            params: Dict[str, Any] = None
    ):
        # print(f'url={url}\nheaders={headers}\nparams={params}')
        try:
            resp = requests.get(
                url=url,
                auth=auth,
                params=params,
                headers=headers,
            )
            data = resp.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise e
        if resp.status_code == 200:
            return data
        else:
            return {}

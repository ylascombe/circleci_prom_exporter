#! /usr/bin/env python3
import http.client
from base64 import b64encode
from typing import Dict, Any
import json
import os

class CircleCI:
    """
    Helper class that abstract calls to CircleCI v2 API
    """

    def __init__(self, token:str) -> None:
        self.token = token
        self.conn_api =  http.client.HTTPSConnection("circleci.com")
        self.conn_runners =  http.client.HTTPSConnection("runner.circleci.com")
        self.headers = { 'authorization': self._basic_auth(f"{self.token}") }

    def _basic_auth(self, token:str) -> str:
        """ helper that create a basic auth token
        """
        token = b64encode(f"{token}:".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    def _execute_api_call(self, url:str, conn:http.client.HTTPSConnection) -> str:
        """ Execute HTTP requests ans return response as JSON
        """
        conn.request("GET",url, headers=self.headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        return data

    def get_project_insights(self,
                             project_slug:str,
                             branch:str ='master',
                             reporting_window:str ='last-7-days'
                             ) -> dict:
        """
        Call insights CircleCI v2 API and return response as dict
        https://circleci.com/docs/api/v2/index.html#tag/Insights
        """
        url = ('/api/v2/insights/pages/gh/'
                + project_slug +
                '/summary?'
                'reporting-window=' + reporting_window + '&'
                'branches=' + branch
        )
        data = self._execute_api_call(url, self.conn_api)
        return data

    def unclaimed_tasks_for(self, resource_class:str) -> int:
        """
        Get the number of unclaimed tasks for a given resource class
        by calling CircleCI runner API
        (https://runner.circleci.com/api/v3/runner/tasks)
        """
        self.conn_runners =  http.client.HTTPSConnection("runner.circleci.com")
        url = f'/api/v3/runner/tasks?resource-class={resource_class}'
        data = self._execute_api_call(url, self.conn_runners)
        return data['unclaimed_task_count']

    def running_tasks_for(self, resource_class:str) -> int:
        """
        Get the number of running tasks for a given resource class
        by calling CircleCI runner API
        (https://runner.circleci.com//api/v3/runner/tasks/running)
        """
        self.conn_runners =  http.client.HTTPSConnection("runner.circleci.com")
        url = f'/api/v3/runner/tasks/running?resource-class={resource_class}'
        data = self._execute_api_call(url, self.conn_runners)
        return data['running_runner_tasks']

    def list_available_runners(self) -> Any:
        """
        Lists the available self-hosted runners based on the specified parameters
        by calling CircleCI runner API
        (https://runner.circleci.com//api/v3/runner/tasks/running)
        """
        self.conn_runners =  http.client.HTTPSConnection("runner.circleci.com")
        url = '/api/v3/runner?namespace=lifen'
        data = self._execute_api_call(url, self.conn_runners)
        return data['items']


if __name__ == '__main__':
    to = os.getenv('CIRCLECI_TOKEN')
    p = CircleCI(to)
    #print(p.unclaimed_tasks_for(rc))
    #print(p.running_tasks_for(rc))
    print(p.list_available_runners())


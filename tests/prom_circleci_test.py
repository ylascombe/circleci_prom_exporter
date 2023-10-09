import unittest
from typing import Dict, Any
from unittest.mock import Mock, patch
from src.prom_circleci import PromCircleCi
from prometheus_client import REGISTRY

# pylint: disable=W0613
def fake_api_response():
   return {
       "project_workflow_branch_data": [
          {
            "workflow_name": "tests",
            "branch": "master",
            "metrics": {
              "total_credits_used": 3231,
              "p95_duration_secs": 315.299,
              "total_runs": 18,
              "success_rate": 0.9444
            },
            "trends": {
              "total_credits_used": 0.668,
              "p95_duration_secs": 1.2261,
              "success_rate": 0.9444,
              "total_runs": 0.6429
            }
          }
        ],
        "all_workflows": [
          "build",
          "tests"
        ],
        "org_id": "xxxxxx-yyy-zzzz-1234-12345678989",
        "all_branches": [],
        "project_workflow_data": [
          {
            "workflow_name": "tests",
            "metrics": {
              "total_credits_used": 11888,
              "p95_duration_secs": 306.0,
              "total_runs": 71,
              "success_rate": 0.7465
            },
            "trends": {
              "total_credits_used": 0.902,
              "p95_duration_secs": 1.0912,
              "success_rate": 0.8096,
              "total_runs": 0.9221
            }
          }
        ],
        "project_id": "ce8e14ea-ec96-4ced-aaad-09af233ee807",
        "project_data": {
          "trends": {
            "success_rate": 0.9444,
            "total_credits_used": 0.668,
            "throughput": 0.642,
            "total_duration_secs": 0.682,
            "total_runs": 0.6429
          },
          "metrics": {
            "success_rate": 0.9444,
            "total_credits_used": 3231,
            "throughput": 2.5714285,
            "total_duration_secs": 4931,
            "total_runs": 18
          }
      }
   }



class TestPromCircleCi(unittest.TestCase):

    def check_gauge(self, key:str, expectedValue:Any, tags:Dict[str, str]):
        a = REGISTRY.get_sample_value(key, tags)
        self.assertEqual(a, expectedValue)

    @patch('src.circleci.CircleCI.get_project_insights')
    def test_parse_insights(self, mock_circleci):
        # arrange
        mock_circleci.return_value = fake_api_response()
        project_slug = 'myorg/myrepo'
        prom_circleci = PromCircleCi()

        # act
        prom_circleci.parse_insights(project_slug)

        # assert
        self.check_gauge('trends_success_rate', 0.9444, {'project_slug': project_slug})
        self.check_gauge('trends_total_credits_used', 0.668, {'project_slug': project_slug})
        self.check_gauge('trends_throughput', 0.642, {'project_slug': project_slug})
        self.check_gauge('trends_total_duration_secs',  0.682, {'project_slug': project_slug})
        self.check_gauge('trends_total_runs',  0.6429, {'project_slug': project_slug})

if __name__ == '__main__':
    unittest.main()
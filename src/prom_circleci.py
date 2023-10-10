#! /usr/bin/env python3
import os
from typing import Dict, List, Any
from src.circleci import CircleCI
from src.common import Config
from prometheus_client import Gauge, REGISTRY
from prometheus_client.metrics import MetricWrapperBase

class PromCircleCi:
    """
    Extract from CircleCI API response data metrics that we want to expose
    by creating labeled Prometheus Gauges
    """

    def __init__(self) -> None:
        token = Config().circleci_token
        self.api = CircleCI(token=token)
        self.gauges: Dict[str, Gauge] = {}

    def set_metric_value(self,
                         name:str,
                         desc:str,
                         labels:Dict[str,str],
                         value: Any
    ) -> None:

        values = list(labels.values())
        keys = list(labels.keys())

        key = name + '_' + '_'.join(keys)
        #key = name

        debug = f'###\nmetric with name {name} and key {key}, \nlabels keys {keys}\nlabelsvalues = {values}"\nname is {name}'
        gauge = None

        #if name == 'workflow_metrics_total_credits_used':
        #    print("------------>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #    gauge = Gauge(key, desc, keys)
        #    gauge.labels(project_slug='honestica/terraform', name='process-module-glue').set(value=value)
        #    return
        if key not in self.gauges:
            print(f"Create gauge {debug}")
            gauge = Gauge(key, desc, labels)
            print(f'values={values}\n keys={keys}')
            #gauge.labels(labels).set(value=value)
            gauge.labels(labels).set(value=value)
            self.gauges[key] = gauge
        else:
            print(f"found gauge {debug}")
            gauge = self.gauges[key]
            print(f'g={gauge}')
            gauge.labels(labels).set(value=value)


    def parse_insights(self, project_slug:str) -> None:
        """
        Create gauges for each metrics returned by CircleCI class/API
        in Prometheus format
        """
        res = self.api.get_project_insights(project_slug)

        for group in res['project_data']:
            project_data = res['project_data'][group]
            for metric in project_data:
                key = f'{group}_{metric}'
                labels = {
                    'project_slug' : project_slug
                }
                self.set_metric_value(
                    name=key,
                    desc=metric,
                    labels=labels,
                    value=project_data[metric]
                )


        for workflow in res['project_workflow_data']:
            self._parse_worflow(workflow, project_slug)

    def parse_container_runners(self, namespace) -> None:
        """
        Create gauges for each resource class returned by CircleCI class/API
        in Prometheus format
        """
        res = self.api.list_available_runners(namespace)

        g_unclaimed = Gauge('runner_unclaimed_tasks', 'runner_unclaimed_tasks', ['resource_class'])
        g_running = Gauge('runner_running_tasks', 'runner_running_tasks', ['resource_class'])

        for resource_class_data in res:
            resource_class = resource_class_data['resource_class']

            unclaimed_tasks_nb = self.api.unclaimed_tasks_for(resource_class)
            running_tasks_nb = self.api.running_tasks_for(resource_class)

            g_unclaimed.labels(resource_class).set(unclaimed_tasks_nb)
            g_running.labels(resource_class).set(running_tasks_nb)


    def _parse_worflow(self, workflow:str, project_slug:str) -> None:
        """
        Parse a list of dict in order to create 8 gauges for each workflow
        Example data:
            "project_workflow_branch_data": [
                {
                "workflow_name": "process-module-iam-teams",
                "branch": "master",
                "metrics": {
                    "total_credits_used": 0,
                    "p95_duration_secs": 0.0,
                    "total_runs": 0,
                    "success_rate": 0.0
                },
                "trends": {
                    "total_credits_used": 1.0,
                    "p95_duration_secs": 0.0,
                    "success_rate": 0.0,
                    "total_runs": 0.0
                }
            },
        """
        workflow_name = workflow['workflow_name']
        for group in ['metrics','trends']:
            group_data = workflow[group]
            for metric in group_data:
                key = f'workflow_{group}_{metric}'

                labels = {
                    'project_slug': project_slug,
                    'name' : workflow_name
                }

                self.set_metric_value(
                    name=key,
                    desc=metric,
                    labels=labels,
                    value=group_data[metric]
                )
                # gauge = Gauge(key, metric,['project_slug', 'name'])
                # gauge.labels(project_slug, workflow_name).set(group_data[metric])

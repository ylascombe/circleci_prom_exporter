#! /usr/bin/env python3
import os
import sys
import random
import time
import src.prom_circleci as prom_circleci
from src.common import Config
from src.github import GitHubOrganization
from prometheus_client import start_http_server, Summary

# FIXME copy pasted from prometheus_client readme

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    promCircleCi = prom_circleci.PromCircleCi()

    config = Config()

    for org in config.organizations:
        github_org = GitHubOrganization(org)
        repos = github_org.repositories()

        for repo in repos:
            print(f'Preparing to parse insights for repo {repo}')
            promCircleCi.parse_insights(repo)

    namespace = os.getenv('CIRCLECI_CONTAINER_NAMESPACE')
    promCircleCi.parse_container_runners(namespace=namespace)

    # Generate some requests.
    while True:
        process_request(random.random())

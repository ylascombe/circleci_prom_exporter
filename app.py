#! /usr/bin/env python3
import os
import sys
import random
import time
import src.circleci as circleci
import src.prom_circleci as prom_circleci
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

    project_slug = os.getenv('PROJECT_SLUG')
    if project_slug is None:
        print("PROJECT_SLUG env var is expected with format myorg/myrepo")
        sys.exit(1)
    promCircleCi.parse_insights(project_slug)

    namespace = os.getenv('CIRCLECI_CONTAINER_NAMESPACE')
    promCircleCi.parse_container_runners(namespace=namespace)
    
    # Generate some requests.
    while True:
        process_request(random.random())

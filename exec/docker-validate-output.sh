#!/bin/bash
# Validate merged outputs inside Docker container

docker-compose run --rm immerculate validate_output.py "$@"

#!/bin/bash
celery -A run_parsing worker -B --loglevel=DEBUG

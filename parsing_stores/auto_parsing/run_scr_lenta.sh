#!/bin/bash
celery -A cherry worker -B --loglevel=DEBUG

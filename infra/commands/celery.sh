#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    uv run celery --app=src.tasks.celery_conf:celery_app worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    uv run celery --app=src.tasks.celery_conf:celery_app flower
elif [[ "${1}" == "beat" ]]; then
    uv run celery --app=src.tasks.celery_conf:celery_app beat -l INFO
fi
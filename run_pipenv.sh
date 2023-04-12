#! /usr/bin/env bash

. ./project.env

# shellcheck disable=SC2034
declare -a run_pipenv_run=(
    "pipenv"
    "run"
)

#! /usr/bin/env bash

. ./project.env

# shellcheck disable=SC2034
declare -a pipenv_run=(
    "pipenv"
    "run"
)

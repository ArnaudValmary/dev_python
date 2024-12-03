#! /usr/bin/env bash

. ./project.env

# shellcheck disable=SC2034
declare -a run_in_env=(
    "poetry"
    "run"
)

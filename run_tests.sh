#! /usr/bin/env bash

. run_pipenv.sh

declare -a run_pytest=(
    "pytest"
    "--verbose"
    "--full-trace"
    "-r" "A"
)

run_test () {
    export_vars
    set -x
    "${run_pipenv_run[@]}" "${run_pytest[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_tests ]]; then
    run_test
fi

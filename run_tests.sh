#! /usr/bin/env bash

. run_pipenv.sh

declare -a pytest_run=(
    "pytest"
    "--verbose"
    "--full-trace"
    "-r" "A"
)

run_test () {
    export_vars
    set -x
    "${pipenv_run[@]}" "${pytest_run[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_tests ]]; then
    run_test
fi

#! /usr/bin/env bash

. run_pipenv.sh

declare -a run_pytest=(
    "pytest"
    "--verbose"
    "--full-trace"
    "-r" "A"
)

declare -a run_pytest_junit=(
    "pytest"
    "--verbose"
    "--full-trace"
    "-r" "A"
    "--junitxml=${test_junit_filename}"
    "-o" "junit_family=xunit1"
)

run_test () {
    export_vars
    set -x
    "${run_pipenv_run[@]}" "${run_pytest[@]}"
    set +x
}

run_test_junit () {
    export_vars
    set -x
    "${run_pipenv_run[@]}" "${run_pytest_junit[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_tests ]]; then
    run_test
    run_test_junit
fi

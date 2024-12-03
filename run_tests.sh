#! /usr/bin/env bash

if [[ -f pyproject.toml ]] && grep -E "tool\.poetry" "pyproject.toml"; then
    source run_poetry.sh
elif [[ -f Pipfile ]]; then
    source run_pipenv.sh
else
    echo "No environment file found. Exit" >&2
fi

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
    "${run_in_env[@]}" "${run_pytest[@]}"
    set +x
}

run_test_junit () {
    export_vars
    set -x
    "${run_in_env[@]}" "${run_pytest_junit[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_tests ]]; then
    run_test
    run_test_junit
fi

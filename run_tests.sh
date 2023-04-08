#! /usr/bin/env bash

. run_pipenv.sh

declare -a pytest_run=(
    "pytest"
    "--verbose"
    "--tb=long"
    "-r" "A"
)

run_test () {
    export_pip_env
    set -x
    "${pipenv_run[@]}" "${pytest_run[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_tests ]]; then
    run_test
fi

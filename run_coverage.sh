#! /usr/bin/env bash

. run_tests.sh

declare -a coverage_run=(
    "coverage"
    "run"
    "-m"
)
coverage_run_pytest=("${coverage_run[@]}" "${pytest_run[@]}")

declare -a coverage_html=(
    "coverage"
    "html"
)

run_coverage_pytest () {
    export_pip_env
    set -x
    "${pipenv_run[@]}" "${coverage_run_pytest[@]}"
    set +x
}
run_coverage_build_html_report () {
    export_pip_env
    set -x
    "${pipenv_run[@]}" "${coverage_html[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_coverage ]]; then
    run_coverage_pytest
    run_coverage_build_html_report
    firefox htmlcov/index.html
fi

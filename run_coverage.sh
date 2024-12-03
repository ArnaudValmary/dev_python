#! /usr/bin/env bash

if [[ -f pyproject.toml ]] && grep -E "tool\.poetry" "pyproject.toml"; then
    source run_poetry.sh
elif [[ -f Pipfile ]]; then
    source run_pipenv.sh
else
    echo "No environment file found. Exit" >&2
fi

declare -a run_coverage_with_pytest_and_build_xml_report=(
    "pytest"
    "--junitxml" "${coverage_junit_filename}"
    "--cov-config=${coverage_config_filename}"
    "--cov-report" "xml:${coverage_xml_report_filename}"
)
for sources_dir in "${sources_dirs[@]}"; do
    run_coverage_with_pytest_and_build_xml_report+=("--cov" "${sources_dir}")
done

declare -a build_coverage_html_report=(
    "coverage"
    "html"
)

run_coverage_and_build_xml_report () {
    export_vars
    set -x
    rm -f "${coverage_report_filename}"
    rm -f "${coverage_xml_report_filename}"
    "${run_in_env[@]}" "${run_coverage_with_pytest_and_build_xml_report[@]}"
    set +x
}

run_build_coverage_html_report () {
    export_vars
    set -x
    rm -rf "${coverage_html_report_dirname}"
    "${run_in_env[@]}" "${build_coverage_html_report[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_coverage ]]; then
    run_coverage_and_build_xml_report
    run_build_coverage_html_report
    firefox htmlcov/index.html
fi

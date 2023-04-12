#! /usr/bin/env bash

. ./run_pipenv.sh

declare -a run_coverage_with_pytest_and_build_xml_report=(
    "pytest"
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
    "${run_pipenv_run[@]}" "${run_coverage_with_pytest_and_build_xml_report[@]}"
    set +x
}
run_build_coverage_html_report () {
    export_vars
    set -x
    rm -rf "${coverage_html_report_dirname}"
    "${run_pipenv_run[@]}" "${build_coverage_html_report[@]}"
    set +x
}

if [[ "$(get_prog_name)" == run_coverage ]]; then
    run_coverage_and_build_xml_report
    run_build_coverage_html_report
    firefox htmlcov/index.html
fi

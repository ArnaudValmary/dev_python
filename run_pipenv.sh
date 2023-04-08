#! /usr/bin/env bash

declare -a pipenv_env=(
    "PYTHONPATH=."
)

# shellcheck disable=SC2034
declare -a pipenv_run=(
    "pipenv"
    "run"
)

print_var () {
    local var_name="$1"
    printf "var %s = '%s'\n" "${var_name}" "${!var_name}"
}

export_pip_env () {
    for var_value in "${pipenv_env[@]}"; do
        # shellcheck disable=SC2163
        export "${var_value}"
        print_var "${var_value%%=*}"
    done
}

get_prog_name () {
    local prog_name="${0##*/}"
    local -r prog_name="${prog_name%.*}"
    printf "%s" "${prog_name}"
}

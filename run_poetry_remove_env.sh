#! /usr/bin/env bash

env_dir=$(poetry env info -p)
if [[ -n "$env_dir" ]] && [[ -d "$env_dir" ]]; then
    env_dir="${env_dir##*/}"
    echo "Removing directory '$env_dir'"
    poetry env remove "$env_dir"
fi

lock_file="poetry.lock"
if [[ "$lock_file" ]]; then
    echo "Removing file '$lock_file'"
    rm -f "$lock_file"
fi

echo "Done"

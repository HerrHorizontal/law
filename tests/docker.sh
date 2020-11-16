#!/usr/bin/env bash

# Script to run all tests in a docker image.
# Arguments:
#   1. The docker image, defaults to "riga/law".
#   2. The test command. When just "i", an interactive bash is started instead of running the tests
#      and exiting. Defaults to "./tests/run.sh".

action() {
    local this_file="$( [ ! -z "$ZSH_VERSION" ] && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "$this_file" )" && pwd )"
    local repo_dir="$( cd "$( dirname "$this_dir" )" && pwd )"

    local image="${1:-riga/law}"
    local cmd="${2:-./tests/run.sh}"

    echo "running docker image $image"

    if [ "$cmd" = "i" ] || [ "$cmd" = "interactive" ]; then
        docker run --rm -ti -v "$repo_dir":/root/law "$image" bash
    else
        docker run --rm -t -v "$repo_dir":/root/law "$image" bash -c "$cmd"
    fi
}
action "$@"

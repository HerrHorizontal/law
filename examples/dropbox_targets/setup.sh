#!/usr/bin/env bash

action() {
    # determine the directory of this file
    local this_file="$( [ ! -z "$ZSH_VERSION" ] && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "$this_file" )" && pwd )"
    local law_base="$( dirname "$( dirname "$this_dir" )" )"

    export LAW_DROPBOX_EXAMPLE="$this_dir"
    export LAW_HOME="$this_dir/.law"
    export LAW_CONFIG_FILE="$this_dir/law.cfg"

    export PATH="$law_base/bin:$PATH"
    export PYTHONPATH="$law_base:$PYTHONPATH"

    source "$( law completion )" ""
}
action

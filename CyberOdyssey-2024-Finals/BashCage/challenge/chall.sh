#!/bin/bash

set -euo pipefail

readonly ALLOWED_CHARS="(){}'\"$\\<#"

echo """
 ____            _      ____
| __ )  __ _ ___| |__  / ___|__ _  __ _  ___
|  _ \ / _' / __| '_ \/ |   / _' |/ _' |/ _ \\
| |_) | (_| \__ \ | | | |__| (_| | (_| |  __/
|____/ \__,_|___/_| |_|\____\__,_|\__, |\___|
                                  |___/
Welcome to BashCage! Break free if you can...
Only these special characters are allowed: ${ALLOWED_CHARS}
Good luck!
"""

read -e -r -p "$ " CMD

if [[ ! "${CMD}" =~ ^[${ALLOWED_CHARS}]*$ ]]; then
    echo >&2 "Invalid command."
    exit 1
fi

if [[ -n "${CMD}" ]]; then
    printf -v cmd '%s ' bash -c "\"${CMD}\""
    eval $cmd
fi

#!/bin/bash

set -euo pipefail

(
    cd "$(dirname "$0")"
    version="${1:-0.1.6}"
    echo "Downloading version $version"

    tools=(wget tar unzip)

    tools_installed="true"
    for tool in "${tools[@]}"; do
        if ! which "$tool" &> /dev/null; then
            echo "please install $tool"
            tools_installed="false"
        fi
    done
    if ! "$tools_installed"; then
        exit 1
    fi

    wget -O "qrscan-linux.tar.gz" "https://github.com/sayanarijit/qrscan/releases/download/v$version/qrscan-$version-x86_64-unknown-linux-gnu.tar.gz"
    tar --overwrite -xf "qrscan-linux.tar.gz"
    rm "qrscan-linux.tar.gz"
    wget -O "qrscan-windows.zip" "https://github.com/sayanarijit/qrscan/releases/download/v$version/qrscan-$version-x86_64-pc-windows-gnu.zip"
    unzip -o "qrscan-windows.zip"
    rm "qrscan-windows.zip"
)

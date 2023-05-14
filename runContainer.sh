#!/bin/bash

if [[ -z "$1" || -z "$2" ]]; then
    echo "Usage: $0 <pdf> <whitelist>"
    exit 1
fi

pdf="$1"
whitelist="$2"

docker run -it --rm -v "$PWD":/app/content index-generator python src/main.py --pdf "/app/content/$pdf" --whitelist "/app/content/$whitelist" --dir content/

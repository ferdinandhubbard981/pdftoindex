#!/bin/bash

if [[ -z "$1" || -z "$2" ]]; then
    echo "Usage: $0 <pdf> <blacklist>"
    exit 1
fi

pdf="$1"
blacklist="$2"

docker run -it --rm -v "$PWD":/app/content index-generator python src/main.py --pdf "/app/content/$pdf" --blacklist "/app/content/$blacklist" --dir content/

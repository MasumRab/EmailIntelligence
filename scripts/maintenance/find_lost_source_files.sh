#!/bin/bash

# This script finds dangling blobs that might contain source code.

# Get the list of dangling blobs
dangling_blobs=$(grep "dangling blob" /home/masum/.gemini/tmp/ecf9a8bc2dfe40868144eda095201fa9bea57f16fec6afc9397615d58ba49520/fsck_lost_found.txt | awk '{print $3}')

if [ -z "$dangling_blobs" ]; then
    echo "No dangling blobs found."
    exit 0
fi

echo "Searching for source code in dangling blobs..."

for blob_sha in $dangling_blobs; do
    if git show "$blob_sha" | grep -qE "class |def |import "; then
        echo "========================================================================"
        echo "Found potential source code in blob: $blob_sha"
        echo "========================================================================"
        git show "$blob_sha"
        echo ""
    fi
done

echo "Search complete."

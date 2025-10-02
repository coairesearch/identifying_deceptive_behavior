#!/bin/bash
# Watch progress of ALL running experiments
# Usage: ./scripts/watch_all_progress.sh

PROGRESS_DIR="experiments"

echo "Watching all experiment progress files..."
echo "Press Ctrl+C to stop"
echo ""

# Check if any progress files exist
if ! ls ${PROGRESS_DIR}/progress_*.txt 1> /dev/null 2>&1; then
    echo "No experiments currently running (no progress files found)"
    echo "Progress files location: ${PROGRESS_DIR}/progress_*.txt"
    exit 1
fi

# Watch all progress files
watch -n 2 "
echo '=== RUNNING EXPERIMENTS ==='
echo ''
for file in ${PROGRESS_DIR}/progress_*.txt; do
    if [ -f \"\$file\" ]; then
        cat \"\$file\"
        echo ''
        echo '---'
        echo ''
    fi
done
echo 'Last updated:' \$(date)
"

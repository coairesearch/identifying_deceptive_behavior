#!/bin/bash
# Watch the progress of parallel experiments
# Usage: ./scripts/watch_progress.sh

STATUS_FILE="experiments/current_run_status.txt"

echo "Watching experiment progress..."
echo "Press Ctrl+C to stop"
echo ""

if [ ! -f "$STATUS_FILE" ]; then
    echo "No experiments currently running (status file not found)"
    echo "Status file: $STATUS_FILE"
    exit 1
fi

# Watch the status file
watch -n 2 "cat $STATUS_FILE 2>/dev/null || echo 'Experiments completed or not running'"

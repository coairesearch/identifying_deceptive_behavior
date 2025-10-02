#!/bin/bash
# Wrapper script to run behavior classifier with environment variables

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment variables
export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)

# Run classifier
python3 "$PROJECT_ROOT/tools/behavior_classifier.py" "$@"

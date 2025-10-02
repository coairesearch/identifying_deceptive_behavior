#!/bin/bash
# Load environment variables and run experiment

# Load .env file
export $(cat .env | xargs)

# Run the experiment
python3 run_experiment.py "$@"

#!/usr/bin/env bash

set -euo pipefail

# Activate virtual environment if available
if [[ -f ".venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

# Run all unit tests and return non-zero exit code if any tests fail
python3 -m unittest discover -s tests -v
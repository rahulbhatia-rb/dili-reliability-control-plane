#!/usr/bin/env bash
set -euo pipefail
python -m src.dili_control_plane.cli examples/production-api.json --evidence evidence.json

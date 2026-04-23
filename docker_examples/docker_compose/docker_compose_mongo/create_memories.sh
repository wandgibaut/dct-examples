#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_DIR="${DCT_COMMON_DIR:-$SCRIPT_DIR/../../common}"

DCT_EXAMPLES_ROOT="$SCRIPT_DIR" python3 "$COMMON_DIR/create_memories.py" "$@"

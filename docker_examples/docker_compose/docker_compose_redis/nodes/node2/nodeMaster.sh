#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_DIR="${DCT_COMMON_DIR:-$SCRIPT_DIR/../../../../common}"

exec "$COMMON_DIR/node_master.sh" "$@"

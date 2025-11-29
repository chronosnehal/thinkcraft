#!/bin/bash
# Generate requirements.txt from requirements.in using pip-compile
# Usage: ./scripts/generate_requirements.sh [--upgrade]
#   --upgrade: Upgrade all packages to their latest versions

set -e

UPGRADE_FLAG=""
if [ "$1" == "--upgrade" ]; then
    UPGRADE_FLAG="--upgrade"
    echo "Generating requirements.txt with --upgrade flag..."
else
    echo "Generating requirements.txt from requirements.in..."
fi
echo ""

# Check if pip-compile is installed
if ! command -v pip-compile &> /dev/null; then
    echo "pip-compile not found. Installing pip-tools..."
    pip install pip-tools
fi

# Generate requirements.txt
cd "$(dirname "$0")/.."
pip-compile $UPGRADE_FLAG requirements.in

echo ""
echo "✓ requirements.txt generated successfully!"
if [ "$UPGRADE_FLAG" != "--upgrade" ]; then
    echo ""
    echo "To upgrade all packages: ./scripts/generate_requirements.sh --upgrade"
fi


#!/bin/bash
# Generate requirements.txt from requirements.in using pip-compile
# Usage: ./scripts/generate_requirements.sh

set -e

echo "Generating requirements.txt from requirements.in..."
echo ""

# Check if pip-compile is installed
if ! command -v pip-compile &> /dev/null; then
    echo "pip-compile not found. Installing pip-tools..."
    pip install pip-tools
fi

# Generate requirements.txt
cd "$(dirname "$0")/.."
pip-compile requirements.in

echo ""
echo "✓ requirements.txt generated successfully!"
echo ""
echo "To update all packages: pip-compile --upgrade requirements.in"


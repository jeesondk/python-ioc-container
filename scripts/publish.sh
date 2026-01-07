#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting publish process...${NC}"

# 1. Run tests and checks
echo -e "${YELLOW}Running tests and checks...${NC}"
make lint
make type-check
make test

# 2. Build the package
echo -e "${YELLOW}Building the package...${NC}"
make build

# 3. Upload to PyPI
echo -e "${YELLOW}Uploading to PyPI...${NC}"
echo "You will be prompted for your PyPI credentials if they are not configured in ~/.pypirc"
make upload

echo -e "${GREEN}Publishing completed successfully!${NC}"

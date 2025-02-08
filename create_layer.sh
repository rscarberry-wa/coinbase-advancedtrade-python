#!/bin/bash

getHeadSha() {
    # Get the HEAD SHA of the current branch
    echo `git rev-parse --short=8 HEAD`
}

# Create the .layers/python directory if it doesn't already exist
mkdir -p .layers/python

# Copy the contents of .venv/Lib/site-packages to .layers/python
cp -r .venv/Lib/site-packages/* .layers/python/

# Copy the coinbase_advanced_trader directory to .layers/python
cp -r coinbase_advanced_trader .layers/python/

# Print a success message
echo "Files have been successfully copied to .layers/python."

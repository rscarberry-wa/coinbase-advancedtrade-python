#!/bin/bash

# Function to get the short hash of the current HEAD commit
getHeadSha() {
    echo "$(git rev-parse --short=8 HEAD)"
}

getTimestamp() {
  echo "$(date +%Y%m%d)"
}

# Define constants
LAYERS_DIR=".layers"
TARGET_DIR="$LAYERS_DIR/python"
VENV_DIR="$LAYERS_DIR/create_layer"
REQUIREMENTS_FILE="requirements.txt"
PROJECT_DIR="coinbase_advanced_trader"

# Ensure Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "Error: Python 3.12 is not installed or not found in PATH."
    exit 1
fi

# Check if the target directory already exists
if [ -d "$TARGET_DIR" ]; then
    echo "Target directory ($TARGET_DIR) already exists. Deleting it..."
    rm -rf "$TARGET_DIR"
    echo "Deleted existing directory."
fi

# Create the layers and virtual environment directories
echo "Creating required directories: $LAYERS_DIR and target $TARGET_DIR"
mkdir -p "$LAYERS_DIR" "$TARGET_DIR"

# Create a new virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment directory ($VENV_DIR) already exists. Deleting it..."
    rm -rf "$VENV_DIR"
    echo "Deleted existing virtual environment."
fi

echo "Creating a new virtual environment ($VENV_DIR) using Python 3.12..."
if ! python3.12 -m venv "$VENV_DIR"; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi
echo "Virtual environment created successfully."

# Activate the virtual environment
echo "Activating the virtual environment..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# Install dependencies from requirements.txt
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
    echo "Dependencies installed successfully."
else
    echo "Error: $REQUIREMENTS_FILE not found in the project root."
    deactivate
    exit 1
fi

# Deactivate the virtual environment
echo "Deactivating the virtual environment..."
deactivate

TARGET_LIB_DIR="$TARGET_DIR/lib"
mkdir -p "$TARGET_LIB_DIR"

# Copy the virtual environment site-packages to the target directory
VENV_LIB_DIR="$VENV_DIR/lib"
if [ -d "$VENV_LIB_DIR" ]; then
    echo "Copying virtual environment dependencies to $TARGET_DIR..."
    cp -r "$VENV_LIB_DIR/"* "$TARGET_LIB_DIR"
else
    echo "Error: Dependencies directory not found in the virtual environment."
    exit 1
fi

# Copy the project directory to the target site-packages
if [ -d "$PROJECT_DIR" ]; then
    echo "Copying project directory ($PROJECT_DIR) to the site-packages directory in $TARGET_DIR..."
    cp -r "$PROJECT_DIR" "$TARGET_LIB_DIR/python3.12/site-packages"
    echo "Project directory copied successfully."
else
    echo "Error: Directory '$PROJECT_DIR' does not exist."
    exit 1
fi

# Create a zip file of the target directory
TIMESTAMP=$(getTimestamp)
GIT_HASH=$(getHeadSha)
ZIP_FILE="$LAYERS_DIR/layer_content_${TIMESTAMP}_${GIT_HASH}.zip"

echo "Creating zip file: $ZIP_FILE"
cd "$LAYERS_DIR" || exit
zip -r "$(basename "$ZIP_FILE")" "$(basename "$TARGET_DIR")" > /dev/null
echo "Zip file created successfully: $ZIP_FILE"

# Print success message
echo "Packaging process complete. Files have been packaged into $ZIP_FILE."

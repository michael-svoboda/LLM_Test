#!/bin/bash

# transfer_pdfs.sh
# Script to copy all PDF files from a Windows directory to the WSL backend data directory

# Define source and destination directories
SOURCE_DIR="/mnt/c/Users/micha/Documents/Programming/CirriculumExtracter/"
DEST_DIR="../data/"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Create destination directory if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
fi

# Copy all PDF files
cp "$SOURCE_DIR"/*.pdf "$DEST_DIR"

# Verify copy
if [ $? -eq 0 ]; then
    echo "Successfully transferred PDFs from $SOURCE_DIR to $DEST_DIR."
else
    echo "Error transferring PDFs."
fi


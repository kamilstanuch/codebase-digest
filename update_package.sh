#!/bin/bash

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not in a git repository. Please run this script from your project's root directory."
    exit 1
fi

# Check if Git credentials are set
if [ -z "$(git config --global user.name)" ] || [ -z "$(git config --global user.email)" ]; then
    echo "Git credentials are not set. Please set them using:"
    echo "git config --global user.name \"Your Name\""
    echo "git config --global user.email \"your.email@example.com\""
    exit 1
fi

# Prompt for change description
echo "Please enter a brief description of the changes:"
read change_description

# Increment version
current_version=$(grep "version=" setup.py | sed "s/.*version='\(.*\)'.*/\1/")
IFS='.' read -ra VERSION_PARTS <<< "$current_version"
VERSION_PARTS[2]=$((VERSION_PARTS[2] + 1))
new_version="${VERSION_PARTS[0]}.${VERSION_PARTS[1]}.${VERSION_PARTS[2]}"
sed -i '' "s/version='$current_version'/version='$new_version'/" setup.py

# Commit and push to GitHub
git add .
git commit -m "Update to version $new_version: $change_description"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

# Build and upload to PyPI
echo "Building distribution..."
python3 setup.py sdist bdist_wheel

echo "Uploading to PyPI..."
python3 -m twine upload dist/*

echo "Package updated to version $new_version and pushed to GitHub and PyPI"
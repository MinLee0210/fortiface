#!/bin/bash

# Function to increment version
increment_version() {
    local version=$1
    local type=$2
    IFS='.' read -r major minor patch <<< "$version"

    case $type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Invalid version type: $type"
            exit 1
            ;;
    esac

    echo "$major.$minor.$patch"
}

# Check if version.txt exists
version_file="version.txt"
if [[ ! -f $version_file ]]; then
    echo "Version file not found: $version_file"
    exit 1
fi

current_version=$(cat "$version_file")
echo "Current version: $current_version"

# Ask user for version type
read -p "Enter version type to increment (0. major/1. minor/2. patch): " version_type_input

if [[ $version_type_input == "0" ]]; then
    version_type="major"
elif [[ $version_type_input == "1" ]]; then
    version_type="minor"
elif [[ $version_type_input == "2" ]]; then
    version_type="patch"
else
    echo "Invalid version type: $version_type_input"
    exit 1
fi
# Increment the version
new_version=$(increment_version "$current_version" "$version_type")

# Update the version file
echo "$new_version" > "$version_file"

# Commit changes to Git
git add "$version_file"
git commit -m "Bump version to $new_version"

# Tag the new version
echo "Enter tag message (press enter for default message)"
echo "For multiple bullet points, enter one per line. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:"
tag_message=""
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]] && [[ -z "$tag_message" ]]; then
        tag_message="Version $new_version"
        break
    elif [[ -n "$line" ]]; then
        if [[ -z "$tag_message" ]]; then
            tag_message="• $line"
        else
            tag_message="$tag_message"$'\n'"• $line"
        fi
    fi
done

git tag -a "$new_version" -m "$tag_message"

read -p "Do you want to push the changes and tags? (Y/n): " push_input
push_input=${push_input:-y}  # Set default to 'y' if no input is given

if [[ $push_input == "y" ]]; then
    git push && git push --tags
fi

echo "Version updated to: $new_version"
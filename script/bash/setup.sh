#!/bin/bash

# Define the target directory
TARGET_DIR="$HOME/Documents/Derivative/Palette/Pixel-Wrangle"

# Define the repository URL
REPO_URL="https://github.com/miu-lab/Pixel-Wrangle.git"

# Check if the target directory exists
if [ -d "$TARGET_DIR" ]; then
    # Get the list of branches from the repository
    branches=($(git ls-remote --heads ${REPO_URL} | cut -d "/" -f 3))

    # Prompt the user to select the branch
    PS3="Select the branch you want to use: "
    select branch in "${branches[@]}"; do
        if [[ -n $branch ]]; then
            git -C $TARGET_DIR pull origin $branch
            break
        else
            echo "Invalid selection"
        fi
    done
else
    # Get the list of branches from the repository
    branches=($(git ls-remote --heads ${REPO_URL} | cut -d "/" -f 3))

    # Prompt the user to select the branch
    PS3="Select the branch you want to use: "
    select branch in "${branches[@]}"; do
        if [[ -n $branch ]]; then
            git clone --progress --recursive -b $branch ${REPO_URL} ${TARGET_DIR}
            break
        else
            echo "Invalid selection"
        fi
    done
fi
echo "

============= SETUP IS COMPLETE =============

Launch Touchdesigner and update your Palette 
with right-click on My Components -> Refresh

"
read -n1 -r -p "Press any key to close this window..."
exit
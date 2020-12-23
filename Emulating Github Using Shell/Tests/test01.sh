#!/bin/dash

touch a b

# Scenario 1: no shrug repo exists
ls -d .shrug
if ! ./shrug-add | grep 'shrug-add: error: no .shrug directory containing shrug repository exists'
then
    echo "failed test: shrug-add: calling function without .shrug directory"
    exit
fi

# Create new .shrug repo
./shrug-init

# Scenario 2: No file names are given.
if ! ./shrug-add | grep 'usage: shrug-add <filenames>'
then
    echo "failed test: shrug-add: calling function without any filenames"
    exit
fi

# Scenario 3: Filename given that doesn't exist in current directory.
sh shrug-add d
# Make sure that d does not exist in index
if [ -f "$(pwd)/.shrug/index/d" ]
then
    echo "failed test: shrug-add: calling function with non-existent file"
    exit
fi

# Scenario 4: Normal
sh shrug-add a b
# Make sure these files exist in index
if [ ! -f "$(pwd)/.shrug/index/a" ] || [ ! -f "$(pwd)/.shrug/index/b" ]
then
    echo "failed test: shrug-add: file missing from index"
    exit
fi

echo "passed: shrug-add"
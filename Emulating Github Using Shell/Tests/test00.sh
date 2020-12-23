#!/bin/dash

# Test for shrug-init

# No .shrug redirectory
ls -d .shrug

# Make .shrug directory
./shrug-init
#Check that the .shrug directory is there
if [ ! -d ".shrug" ]
then
    echo "failed test: shrug directory wasn't created"
    exit
else
    ls -d .shrug
fi

# Check the behaviour when .shrug already exists
if ./shrug-init | grep 'shrug-init: error: .shrug already exists' 
then
    echo "passed test: shrug-init works correctly"
fi

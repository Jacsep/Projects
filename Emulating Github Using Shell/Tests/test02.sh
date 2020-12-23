#!/bin/dash

./shrug-init

touch a

# Scenario 1: Commit when add has never been called.
sh shrug-commit -m firstcommit
if [ -d "$(pwd)/.shrug/index" ]
then
    echo "failed test: shrug-commit: index shouldn't exist"
fi

sh shrug-add a

# Error testing
# Missing operands or message
sh shrug-commit
sh shrug-commit -a -m
sh shrug-commit -m
sh shrug-commit -a

# This should not commit, hence no repo should have been made yet
if [ -d "$(pwd)/.shrug/repository" ]
then
    echo "failed test: shrug-commit: should not have committed successfully"
    exit
fi

# Test -a operand
echo 321321321>a
sh shrug-commit -a -m "first_commit"

# Compare index to working directory file
if ! cmp -s "a" "$(pwd)/.shrug/index/a"
then
    echo "failed test: shrug-commit: -a operand didn't work correctly"
    exit
fi

# Check that if no new files are added to index, then there is nothing to commit
sh shrug-commit -m "second_commit"

# Check that this works using shrug_log
if grep -q "second_commit" "$(pwd)/.shrug/log.txt"
then 
    echo "failed test: shrug-commit: committed when there were no changes to index file"
    exit
fi

echo "shrug-commit passed all tests"
#!/bin/dash

# Test shrug-show

sh shrug-init

echo hello>a
sh shrug-add a
sh shrug-commit -m "first commit"

echo world>>a
sh shrug-add a

# If both these show the same thing, then there is a problem
line1=$(sh shrug-show :a)
line2=$(sh shrug-show 0:a)

if [ line1 = line2 ]
then
    echo "failed test: shrug-show: commit and index files should print something different"
    exit
fi

# show a commit that is too high
error=$(sh shrug-show 2:a)
if ! echo $error | grep 'shrug-show: error: unknown commit'
then
    echo "failed test: shrug-show: printing a commit of a file that doesn't exist"
    exit
fi
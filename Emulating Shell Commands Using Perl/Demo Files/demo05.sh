#!/bin/dash

echo "There are $# number of command line arguments"
echo "They are as follows: "

for arg in $@
do
    if [ -f $arg ]
    then
        echo "$arg is a file"
    elif test -d $arg
    then
        echo "$arg is a directory"
    else
        echo "$arg is not a file"
    fi
done
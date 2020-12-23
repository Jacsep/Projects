#!/bin/dash

# Demoing:
# Nested looped
# Command line argument array
# String comparisons

for arg in $@
do
    if test $arg = success
    then
        echo $arg
    elif test $arg != failure 
    then
        echo $arg
    else   
        echo "neither"
    fi
done
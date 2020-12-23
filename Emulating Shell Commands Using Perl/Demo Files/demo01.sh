#!/bin/dash

# Demoing:
# Numeric operators
# Assigning variables
# Arithmetic


counter=1

while test $counter -lt 10
do
    echo $counter
    counter=$((counter + 1))
done
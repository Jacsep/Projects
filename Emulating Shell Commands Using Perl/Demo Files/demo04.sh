#!/bin/dash

counter=0

for c_file in *.c
do
    echo -n "$c_file is the number $counter file read"
    counter=$((counter + 1))  #Increment counter
done

echo "There are $counter c files in total"
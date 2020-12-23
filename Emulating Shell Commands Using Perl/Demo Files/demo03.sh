#!/bin/dash
# print a contiguous integer sequence
# Adapted from examples/3/sequence_expr.sh
start=$1
finish=$2
increment=$3

number=$start
while [ $number -le $finish ]
do
    echo $number
    start2=$number;
    while test $start2 -gt 0
    do
        echo $start2
        start2=$((start2 - 2)); 
    done
    number=$(expr $number + $increment)  # increment number
done
#!/bin/dash

touch a b
sh shrug-init

if ! ./shrug-rm | grep 'usage: shrug-rm'
then
    echo "failed test: shrug-rm: function called with no filename arguments"
    exit
fi

line=$(sh shrug-rm c)

if ! echo $line | grep 'shrug-rm: error'
then
    echo "failed test: shrug-rm: removing file that doesn't exist"
    exit
fi

sh shrug-add a
sh shrug-rm --cached "a"

if [ -f "$(pwd)/.shrug/index/a" ] || [ ! -f "a"]
then
    echo "failed test: shrug-rm: file either removed from current or not removed from index"
    exit
fi

sh shrug-add b
echo change>>b
# Should not remove, both files should still exist
sh shrug-rm b
if [ ! -f "$(pwd)/.shrug/index/b" ] || [ ! -f "b"]
then
    echo "failed test: shrug-rm: file was removed causing loss of work"
    exit
fi

sh shrug-rm --force b
if [ -f "$(pwd)/.shrug/index/b" ] || [ -f "b"]
then
    echo "failed test: shrug-rm: --force option did not work properly"
    exit
fi

echo 321>c
sh shrug-add c
echo 3212>>c
sh shrug-rm --force --cached c
if [ -f "$(pwd)/.shrug/index/c "]
then
    echo "failed test: shrug-rm: file was not forced removed from index"
    exit
fi

echo "shrug-rm has passed all tests"
#!/bin/dash
# Testing to see if the difference between $* and $@ is correct

echo '#!/bin/dash\necho "$*">ex1.txt\necho "$@">ex2.txt\ndiff ex1.txt ex2.txt\n' >test.sh

chmod 755 "test.sh"

echo "command line arguments" | sh test.sh > output1.txt
(./sheeple.pl "test.sh" | perl - command line arguments) > output2.txt
diff output1.txt output2.txt
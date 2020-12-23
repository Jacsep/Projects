#!/bin/dash

# Multiple arguments in an if statement, combination of square brackets and test

echo '#!/bin/dash\ntest=2\nif [ $test -lt 3 ] && test $test -ne 2\nthen\necho "nice"\nfi\n' >test.sh

chmod 755 "test.sh"
sh test.sh > output1.txt
(./sheeple.pl "test.sh" | perl) > output2.txt

diff output1.txt output2.txt
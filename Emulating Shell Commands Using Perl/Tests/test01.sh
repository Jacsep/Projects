#!/bin/dash

# Using expr in a while statement

echo '#!/bin/dash\nstart=1\nwhile test `expr $number + 1` -lt 5\ndo\necho $number\nnumber=$((number + 1))\ndone\n' >test.sh

chmod 755 "test.sh"
sh test.sh > output1.txt
(./sheeple.pl "test.sh" | perl) > output2.txt

diff output1.txt output2.txt
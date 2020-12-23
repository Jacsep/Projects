#!/bin/dash

# Testing to see if local variables are local

echo '#!/bin/dash\nsep() {\nlocal value="1"\necho $value\n}\nsep\nif [ -z "$value" ]\nthen\necho "var empty"\nfi\n' >test.sh

chmod 755 "test.sh"

sh test.sh > output1.txt
(./sheeple.pl "test.sh" | perl) > output2.txt

diff output1.txt output2.txt
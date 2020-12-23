#!/bin/dash

# Test function not inside if statement

echo '#!/bin/dash\nstring="cool"\ntest $string = great\n' >test.sh

chmod 755 "test.sh"
sh test.sh > output1.txt
(./sheeple.pl "test.sh" | perl) > output2.txt

diff output1.txt output2.txt
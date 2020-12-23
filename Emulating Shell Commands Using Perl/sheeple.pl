#!/usr/bin/perl -w

# No command line arguments, read from STDIN
@shell = ();

if ($#ARGV == -1) {
    # Store all inputted lines into an array
    while ($line = <STDIN>) {
        push (@shell, $line);
    }
    # Call translation fn
} else {
    foreach $file (@ARGV) {
        # Store all lines from file into an array\
        open my $text, '<', $file or die "Cannot open $file: $!";
        while ($line = <$text>) {
            chomp $line;
            push (@shell, $line);
        }
        close $text;
    }
}
# Translate shell to perl
translation(@shell);

sub translation {
    # Loop keeps track of the proper identing
    $loop = 0;
    my (@lines) = @_;
    foreach $command (@lines) {
        # Initalise the comment to an empty string. This is used to track any inline comments that contain other code
        $comment = "";
        # Empty line
        if ($command eq "") {
            print ("\n");
            next;
        }
        # If the entire line is just a comment, print it and go next
        if ($command =~ /^# /) {
            print "$command\n";
            next;
        }
        # PreEdit the string into perl syntax
        $command = preEditString($command); 
        # Removes any whitespace       
        $command =~ s/^\s+//;
        # Hash bang line
        if ($command eq "#!/bin/dash") {
            print "#!/usr/bin/perl -w";
        } else {
            # Find any inline comments and extract it from the overall string
            if ($command =~ / #/) {
                $comment = $command;
                $comment =~ /(#.*)/;
                $comment = $1;
                $command =~ s/ #.*//;
                $command =~ s/\s*$//;
            }
            # Split the line into individual words.
            @words = split(' ', $command);
            # Setting variables
            if ($command =~ /\S=\S/) {
                indent($loop);
                variables($command);  
            # Echo
            } elsif ($words[0] eq "echo") {
                indent($loop);
                echo($command);
            # Cd
            } elsif ($words[0] eq "cd") {
                indent($loop);
                print "chdir \'$words[1]\'\;";
            # Exit
            } elsif ($words[0] eq "exit") {
                indent($loop);
                print "exit $words[1]\;";
            # Read
            } elsif ($words[0] eq "read") {
                indent($loop);
                print "\$$words[1] = <STDIN>\;\n";
                indent($loop);
                print "chomp \$$words[1]\;";
            # For loop
            } elsif ($words[0] eq "for") {
                indent($loop);
                # Use glob if we find *
                perlfor($command, @words);
                next;
            # Do
            } elsif ($words[0] eq "do") {
                $loop++;
                print " {";
            # Done
            } elsif ($words[0] eq "done") {
                $loop--;
                indent($loop);
                print "}";
            # While
            } elsif ($words[0] eq "while") {
                print "while ";
                test($command, @words);
                next;
            # If
            } elsif ($words[0] eq "if") {
                $loop++;
                print "if ";
                test($command, @words);
                next;
            # Elif
            } elsif ($words[0] eq "elif") {
                print "} elsif ";
                test($command, @words);
                next;
            # Else
            } elsif ($words[0] eq "else") {
                print "} else {";
            # Fi
            } elsif ($words[0] eq "fi") {
                $loop--;
                print "}";
            # Then
            } elsif ($words[0] eq "then") {
                print " {";
            } else {
                # System commands
                print "system \"$command\"\;";
            }
        }
        # Print comment, if there are no comments this will just print a newline
        print "  $comment\n";
    }
}
# Function to print the required indentation based on the value of loop
sub indent {
    my ($loop) = @_;
    $counter = 0;
    while ($counter < $loop) {
        print "    ";
        $counter++;
    }
}
# Deal with all the test operators
sub test {
    my ($command, @words) = @_;
    # Check whether it is a file or numeric/string operator used
    # Determine operator used
    # File: -r, -d, -e -> Same as operators in Perl
    if ($command =~ /-\w /) {
        if ($words[3] =~ /\$/) {
            print "($words[2] $words[3])";
        } else {
            print "($words[2] \'$words[3]\')";
        }
        
    # Numeric: -eq -ge -gt -le -lt -ne
    } elsif ($command =~ /-/) {
        if ($words[3] eq "-eq") {
            print "($words[2] == $words[4])";
        } elsif ($words[3] eq "-ge") {
            print "($words[2] >= $words[4])";
        } elsif ($words[3] eq "-gt") {
            print "($words[2] > $words[4])";
        } elsif ($words[3] eq "-le") {
            print "($words[2] <= $words[4])";
        } elsif ($words[3] eq "-lt") {
            print "($words[2] < $words[4])";
        } elsif ($words[43] eq "-ne") {
            print "($words[2] != $words[4])";
        } 
    # String: = != 
    } else {
        if ($words[2] =~ /\$/) {
            print "($words[2] "; 
        } else {
            print "(\'$words[2]\' ";
        }
        if ($words[3] eq "=") {
            print "eq";
        } elsif ($words[3] eq "!=") {
            print "ne";
        } elsif ($words[3] eq ">") {
            print "gt";
        }elsif ($words[3] eq "<") {
            print "lt";
        }
        if ($words[4] =~ /\$/) {
            print " $words[4])";
        } else {
            print " \'$words[4]\')";
        }
    } 
}
sub preEditString {
    my ($command) = @_;
    # Change any '" to '\"
    if ($command =~ /\'\"/) {
        $command =~ s/\"/\\\"/g;
    }
    # Remove any '
    if ($command =~ /'/) {
        $command =~ s/'//g;
    }
    # Remove the expr function as for most, perl has an inbuilt for it
    if ($command =~ /expr/) {
        $command =~ s/expr //g;
    }
    # Number of arguments
    if ($command =~ /\$#/) {
        $command =~ s/\$#/\$#ARGV/g;
    }
    # Command line argument array
    if ($command =~ /\$@/) {
        if ($command =~ /"\$@"/) {
            $command =~ s/"\$@"/\@ARGV/g;
        }
        $command =~ s/\$@/\@ARGV/g;
    }
    
    # Remove any backticks are perl can deal with this normally for most cases
    if ($command =~ /\`/) {
        $command =~ s/\`//g;
    }
    # Change [ ] to test, so that I can reuse my test function.
    if ($command =~ /\[.*\]/) {
        $command =~ s/\[/test/;
        $command =~ s/ \]//;
    }
    # Remove $() as perl can deal with this normally for most cases
    if ($command =~ /\$\([^\(]/) {
        $command =~ s/\$\(//;
        $command =~ s/\)//;
    }
    # Dealing with $(())
    if ($command =~ /\$\(\(/) {
        $arithmetic = $command;
        $arithmetic =~ m/(\(.*\))/;
        $arithmetic = $1;
        $old = $arithmetic;
        $arithmetic =~ s/\(//g;
        $arithmetic =~ s/\)//g;
        @equation = split(' ', $arithmetic);
        # Need to determine whether there are any variables inside the brackets
        foreach $term (@equation) {
            # Word character
            if ($term =~ /\w+/) {
                # Non number character
                if ($term =~ /\D+/) {
                    # Add $ to found variable
                    $arithmetic =~ s/$term/\$$term/;
                }
            }
        }
        # Replace old (( )) with new perl expression
        $command =~ s/\Q$old\E/$arithmetic/;
        $command =~ s/\$//;
    }
    # Convert command line arguments
    # Changing from $NUMBER to ARGV[NUMBER-1]
    if ($command =~ /\$\d+/) {
        $num = $command;
        $num =~ /(\$\d+)/;
        $arg = $1;
        $num = $1;
        $num =~ /([^\$]+)/;
        $num = $1;
        $num--;
        $command =~ s/\Q$arg/\$ARGV\[$num\]/g;
    }
    return ($command);
}

sub variables {
    my ($command) = @_;
    $variablename = $command;
    $variablevalue = $command;
    # Extract both variable name and the value
    $variablename =~ s/=.*//;
    $variablevalue =~ s/^.*=//;
    # If the variable is equal to a variable, we don't use single quotes
    if ($variablevalue =~ /\$/){
        print "\$$variablename = $variablevalue\;"
    # Otherwise, use single quotes
    } else {
        print "\$$variablename = \'$variablevalue\'\;"
    }
}

sub echo {
    my ($command) = @_;
    # If -n operator is found, do not print new line
    if ($words[1] eq "-n") {
        $command =~ s/^echo -n //;
        # This is used to prevent printing double quotes
        # Use for arguments that already have double quotes
        if ($command =~ /^\"/ && $command =~ /\"$/) {
            $command =~ s/^\"//;
            $command =~ s/\"$//;
        }
        print "print \"$command\"\;";  
    } else {
        $command =~ s/^echo //;
        if ($command =~ /^\"/ && $command =~ /\"$/) {
            $command =~ s/^\"//;
            $command =~ s/\"$//;
        }
        print "print \"$command\\n\"\;";
    }   
}

sub perlfor {
    my ($command, @words) = @_;
    # Finding all the arguments for the glob function
    if ($command =~ /\*/) {
        print "foreach \$$words[1] (glob(\"$words[3]\")) ";
    } elsif ($command =~ /@/) {
        print "foreach \$$words[1] ($words[3])";
    } else {
        print "foreach \$$words[1] (";
        # Remove the first three words from array so we can focus on arguments solely
        splice @words, 0, 3;
        foreach $key (@words) {
            # If the key is the last one
            if ($key eq $words[-1]) {
                print "\'$key\')";
            } else {
                print "\'$key\', "
            }
        }
    }
}
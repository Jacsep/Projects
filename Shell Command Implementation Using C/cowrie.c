// cowrie.c a simple shell


// PUT YOUR HEADER COMMENT HERE


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <limits.h>
#include <spawn.h>
#include <ctype.h>
#include <glob.h>


// PUT EXTRA `#include'S HERE


#define MAX_LINE_CHARS 1024
#define INTERACTIVE_PROMPT "cowrie> "
#define DEFAULT_PATH "/bin:/usr/bin"
#define WORD_SEPARATORS " \t\r\n"
#define DEFAULT_HISTORY_SHOWN 10

// These characters are always returned as single words
#define SPECIAL_CHARS "!><|"


// PUT EXTRA `#define'S HERE


static void execute_command(char **words, char **path, char **environment, int history, int glob);
static void do_exit(char **words);
static int is_executable(char *pathname);
static char **tokenize(char *s, char *separators, char *special_chars);
static void free_tokens(char **tokens);



// PUT EXTRA FUNCTION PROTOTYPES HERE
char* concat(char *str1, char *str2);
void run_exe(char *command, char **words);
void add_history(char **words);
int count_num_lines(void);
void print_history(int limit);
void print_and_execute(int number, char **path, char **environment);
int array_length(char **words);
int check_num_of_arrows(char **words);
int check_builtin(char *words);
char *pathname_string(int start, char **path, char **words);
char *new_commandline(int start, int difference, char **words, int length);
char **command_words2(char **words);
void exit_status(pid_t pid, char *pathname);

int main(void) {
	//ensure stdout is line-buffered during autotesting
    setlinebuf(stdout);

    // Environment variables are pointed to by `environ', an array of
    // strings terminated by a NULL value -- something like:
    //     { "VAR1=value", "VAR2=value", NULL }
    extern char **environ;

    // grab the `PATH' environment variable;
    // if it isn't set, use the default path defined above
    char *pathp;
    if ((pathp = getenv("PATH")) == NULL) {
        pathp = DEFAULT_PATH;
    }
    char **path = tokenize(pathp, ":", "");

    char *prompt = NULL;
    // if stdout is a terminal, print a prompt before reading a line of input
    if (isatty(1)) {
        prompt = INTERACTIVE_PROMPT;
    }

    // main loop: print prompt, read line, execute command
    while (1) {
        if (prompt) {
            fputs(prompt, stdout);
        }

        char line[MAX_LINE_CHARS];
        if (fgets(line, MAX_LINE_CHARS, stdin) == NULL) {
            break;
        }

        char **command_words = tokenize(line, WORD_SEPARATORS, SPECIAL_CHARS);
        execute_command(command_words, path, environ, 1, 1);
        free_tokens(command_words);
    }

    free_tokens(path);
    return 0;
}


//
// Execute a command, and wait until it finishes.
//
//  * `words': a NULL-terminated array of words from the input command line
//  * `path': a NULL-terminated array of directories to search in;
//  * `environment': a NULL-terminated array of environment variables.
//
static void execute_command(char **words, char **path, char **environment, int history, int glob) {
    assert(words != NULL);
    assert(path != NULL);
    assert(environment != NULL);


    char *program = words[0];

    if (program == NULL) {
        // nothing to do
        return;
    }

    // Add the command to history immediately only if the command is not '!n' or 'history'
    if (words[0][0] != '!' && strcmp(program, "history") != 0 && history != 0) {
    	add_history(words);
    }

    
    if (strcmp(program, "exit") == 0) {
        do_exit(words);
        // do_exit will only return if there is an error
        return;
    }


    // If the value of glob for execute_command is 1, then we will glob the words array
    // Glob will only be 0 in execute_command when we have already globbed the word
    if (glob == 1) {
        char **command_words = command_words2(words);
        execute_command(command_words, path, environment, 0, 0);
        return;  
    } 

    // Check for redirection here
    // Find the length of the words array
    int length = array_length(words);
    // Find the total number of '<' and '>' in the words array
    int num_arrows = check_num_of_arrows(words);
    if (num_arrows > 0) {
    	if (num_arrows == 1) {
    		// Standard input connected to a specific file
    		if (strcmp(words[0], "<") == 0) {
    			// Check whether the command to be executed is a builtin command
    			if (check_builtin(words[2])) {
    				fprintf(stderr, "%s: I/O redirection not permitted for builtin commands\n", words[2]);
    				return;
    			}
    			char *pathname = pathname_string(2, path, words);

    			char *new_string = new_commandline(2, 0, words, length);

			    pid_t pid;
			    posix_spawn_file_actions_t actions;

			    if (posix_spawn_file_actions_init(&actions) != 0) {
			    	perror("posix_spawn_file_actions_init");
			    	return;
			    }
			    // Open the specific file in read mode
			    int read = open(words[1], O_RDONLY, 0);
			    posix_spawn_file_actions_adddup2(&actions, read, 0);
			    posix_spawn_file_actions_addclose(&actions, read);

			    extern char **environ;
			    // Create a new string after removing '<' and the filename
    			char **new_command = tokenize(new_string, WORD_SEPARATORS, SPECIAL_CHARS);
    			// Running posix_spawn on the command
			    if (posix_spawn(&pid, pathname, &actions, NULL, &new_command[0], environ) != 0) {
        				fprintf(stderr, "command not found\n");
        				return;
    			}

			    exit_status(pid, pathname);

    			return;
    		// Standard output connected to a specific file
    		} else if (length > 1 && strcmp(words[length - 2], ">") == 0) {

    			if (check_builtin(words[0])) {
    				fprintf(stderr, "%s: I/O redirection not permitted for builtin commands\n", words[0]);
    				return;
    			}

			    char *pathname = pathname_string(0, path, words);

    			char *new_string = new_commandline(0, 2, words, length);

			    pid_t pid;
			    posix_spawn_file_actions_t actions;

			    if (posix_spawn_file_actions_init(&actions) != 0) {
			    	perror("posix_spawn_file_actions_init");
			    	return;
			    }
			    // Open the specific file in write mode, copying standard output to it
			    if (posix_spawn_file_actions_addopen(&actions, 1, words[length - 1], O_WRONLY | O_CREAT | O_TRUNC, 0644) != 0) {
			    	perror("posix_spawn_file_actions_addopen");
			    	return;
			    }

			    extern char **environ;

    			char **new_command = tokenize(new_string, WORD_SEPARATORS, SPECIAL_CHARS);
			    if (posix_spawn(&pid, pathname, &actions, NULL, &new_command[0], environ) != 0) {
        				fprintf(stderr, "command not found\n");
        				return;
    			}

			    exit_status(pid, pathname);

    			return;
    		} else {
    			fprintf(stderr, "invalid output direction\n");
    			return;
    		}
    	} else if(num_arrows == 2) {
    		// Standard output appended to a specific file
    		if (length > 2 && strcmp(words[length - 3], ">") == 0 && strcmp(words[length - 2], ">") == 0) {
    			
    			if (check_builtin(words[0])) {
    				fprintf(stderr, "%s: I/O redirection not permitted for builtin commands\n", words[0]);
    				return;
    			}

    			char *pathname = pathname_string(0, path, words);

    			char *new_string = new_commandline(0, 3, words, length);

			    pid_t pid;
			    posix_spawn_file_actions_t actions;

			    if (posix_spawn_file_actions_init(&actions) != 0) {
			    	perror("posix_spawn_file_actions_init");
			    	return;
			    }
			    // Open the specified file in append more, before copying standard output to it
			    if (posix_spawn_file_actions_addopen(&actions, 1, words[length - 1], O_RDWR |O_APPEND | O_CREAT , S_IWUSR) != 0) {
			    	perror("posix_spawn_file_actions_addopen");
			    	return;
			    }

			    extern char **environ;

    			char **new_command = tokenize(new_string, WORD_SEPARATORS, SPECIAL_CHARS);
			    if (posix_spawn(&pid, pathname, &actions, NULL, &new_command[0], environ) != 0) {
    				fprintf(stderr, "command not found\n");
    				return;
    			}

			    exit_status(pid, pathname);

    			return;
    		// Standard input connected to a specific file combined with standard output written to another file
    		} else if(length > 4 && strcmp(words[0], "<") == 0 && strcmp(words[length-2], ">") == 0) {
    			if (check_builtin(words[2])) {
    				fprintf(stderr, "%s: I/O redirection not permitted for builtin commands\n", words[0]);
    				return;
    			}

    			char *pathname = pathname_string(2, path, words);
    			char *new_string = new_commandline(2, 2, words, length);
    			pid_t pid;
    			posix_spawn_file_actions_t actions;

    			if (posix_spawn_file_actions_init(&actions) != 0) {
    				perror("posix_spawn_file_actions_init");
    				return;
    			}
    			// First set up standard input given as the commands to the program
    			int read = open(words[1], O_RDONLY, 0);
			    posix_spawn_file_actions_adddup2(&actions, read, 0);
			    posix_spawn_file_actions_addclose(&actions, read);
			    // Copy the resulting standard output to the designated file
			    if (posix_spawn_file_actions_addopen(&actions, 1, words[length - 1], O_WRONLY | O_CREAT | O_TRUNC, 0644) != 0) {
			    	perror("posix_spawn_file_actions_addopen");
			    	return;
			    }

    			extern char **environ;

    			char **new_command = tokenize(new_string, WORD_SEPARATORS, SPECIAL_CHARS);
			    if (posix_spawn(&pid, pathname, &actions, NULL, &new_command[0], environ) != 0) {
    				fprintf(stderr, "command not found\n");
    				return;
    			}

			    exit_status(pid, pathname);

    			return;
    		} else {
    			fprintf(stderr, "invalid output direction\n");
    			return;
    		}
    	} else if (num_arrows == 3) {
    		// Standard input read from a specific file and the resulting standard output appended to a file
    		if (length > 5 && strcmp(words[0], "<") == 0 && strcmp(words[length-2], ">") == 0 && strcmp(words[length-3], ">") == 0) {
    			if (check_builtin(words[2])) {
    				fprintf(stderr, "%s: I/O redirection not permitted for builtin commands\n", words[0]);
    				return;
    			}

    			char *pathname = pathname_string(2, path, words);
    			char *new_string = new_commandline(2, 3, words, length);
    			pid_t pid;
    			posix_spawn_file_actions_t actions;

    			if (posix_spawn_file_actions_init(&actions) != 0) {
    				perror("posix_spawn_file_actions_init");
    				return;
    			}

    			int read = open(words[1], O_RDONLY, 0);
			    posix_spawn_file_actions_adddup2(&actions, read, 0);
			    posix_spawn_file_actions_addclose(&actions, read);

			    if (posix_spawn_file_actions_addopen(&actions, 1, words[length - 1], O_RDWR |O_APPEND | O_CREAT , S_IWUSR) != 0) {
			    	perror("posix_spawn_file_actions_addopen");
			    	return;
			    }

    			extern char **environ;

    			char **new_command = tokenize(new_string, WORD_SEPARATORS, SPECIAL_CHARS);
			    if (posix_spawn(&pid, pathname, &actions, NULL, &new_command[0], environ) != 0) {
    				fprintf(stderr, "command not found\n");
    				return;
    			}

			    exit_status(pid, pathname);

    			return;
    		} else {
    			fprintf(stderr, "invalid output direction\n");
    			return;
    		}
    	} else {
    		fprintf(stderr, "invalid output direction\n");
    		return;
    	}
    }

  

    // Change directory command
    if (strcmp(program, "cd") == 0) {
    	// Change Directory
    	if (words[1] ==  NULL) {
    		// Change to HOME directory
    		char *value = getenv("HOME");
    		if (chdir(value) != 0) {
    		}
    	} else {
    		if (chdir(words[1]) != 0) {
    			fprintf(stderr, "cd: %s: No such file or directory\n", words[1]);
    		}
    	}
  	// Print current directory command
    } else if (strcmp(program, "pwd") == 0) {
    	char pathname[MAX_LINE_CHARS];
    	if(getcwd(pathname, sizeof pathname) == NULL) {
    		perror("getcwd");
    	}
    	printf("current directory is '%s'\n", pathname);
    // Print the contents of the history file
    } else if(strcmp(program, "history") == 0) {
        int counter = 0;
        while (words[counter] != NULL) {
            counter++;
        }
        if (counter > 2) {
            fprintf(stderr, "history: too many arguments\n");
            return;
    	} else if (words[1] == NULL) {
    		print_history(10);
    	} else {
            // Check whether the arguments given to the history command are numbers
            if (isdigit(words[1][0]) == 0) {
                fprintf(stderr, "history: %s: numeric argument required\n", words[1]);
            }
    		print_history(atoi(words[1]));
    	}
    	add_history(words);
    // Print the nth command in history and execute it as well
    } else if (words[0][0] == '!') {
    	// No argument is given, print and execute the last command
        if (words[1] == NULL) {
    		int num_lines = count_num_lines();
    		print_and_execute(num_lines - 2, path, environment);
    	} else {
    		print_and_execute(atoi(words[1]), path, environment);
    	}
    // If the program string doesn't have a backslash, then we need to find the appropriate
    // executable file by string concatenation with the path arrays
    } else if (strrchr(program, '/') == NULL) {
        char *pathname = pathname_string(0, path, words);
        run_exe(pathname, words);
   	// The executable file pathname is already given
    } else if (is_executable(program)) {
    	// Find the appropriate executable file
        run_exe(program, words);
    } else {
    	
        fprintf(stderr, "%s: command not found\n", program);
    }
    
}


// PUT EXTRA FUNCTIONS HERE
// This function combines to strings
char* concat(char *str1, char *str2) {
    char *pathname = malloc(strlen(str2)+strlen(str1)+1);
    strcpy(pathname, str1);
    strcat(pathname, str2);
    return pathname;

}

// Given the command and the arguments, this program runs posix_spawn to execute the executable file
void run_exe(char *command, char **words) {

    pid_t pid;
    extern char **environ;
    if (posix_spawn(&pid, command, NULL, NULL, &words[0], environ) != 0) {
        fprintf(stderr, "%s: command not found\n", words[0]);
        return;
    }

    exit_status(pid, command);
    
    return;

}

// Opens the history file in append mode and prints the entered command to it
void add_history(char **words) {
	char *environment = getenv("HOME");
	char *filename = concat(environment, "/.cowrie_history");
	FILE *history = fopen(filename, "a");

	int counter = 0;
	while (words[counter] != NULL) {
		fprintf(history, "%s ", words[counter]);
		counter++;
	}
	fprintf(history, "\n");
	fclose(history);
}

// Counts the number of lines within the history file
int count_num_lines(void) {
	char *environment = getenv("HOME");
	char *filename = concat(environment, "/.cowrie_history");
	FILE *history = fopen(filename, "r");
	int counter = 1;

	char line[MAX_LINE_CHARS];

	while(fgets(line, MAX_LINE_CHARS, history) != NULL) {
		counter++;
	}
	return counter;
}

// Prints the last 10 or limit number of lines from the end
void print_history(int limit) {
	char *environment = getenv("HOME");
	char *filename = concat(environment, "/.cowrie_history");
	FILE *history = fopen(filename, "r");
	int num_lines = count_num_lines();
	char line[MAX_LINE_CHARS];
	// If the number of lines is less than the limit set, then print them all
	if (num_lines <= limit) {
		int counter = 0;
		while(fgets(line, MAX_LINE_CHARS, history) != NULL) {
			printf("%d: %s", counter, line);
			counter++;
		}
	// Print the last n number of lines in the history file
	} else {
		int counter = 0;
		while (fgets(line, MAX_LINE_CHARS, history) != NULL) {
			if (counter >= num_lines - limit - 1) {
				printf("%d: %s", counter, line);
			}
			counter++;
		}
	}
	fclose(history);
}

// This function is used for the command '!n'
// This finds the appropriate command in the history file
// It then prints that command and executes it
void print_and_execute(int number, char **path, char **environment) {
	int counter = 0;
	FILE *history = fopen(concat(getenv("HOME"), "/.cowrie_history"), "r");
    char line[MAX_LINE_CHARS];

    while (fgets(line, MAX_LINE_CHARS, history) != NULL && number >= counter) {
    	if (counter == number) {
    		printf("%s", line);
    		char **command_words = tokenize(line, WORD_SEPARATORS, SPECIAL_CHARS);
        	execute_command(command_words, path, environment, 1, 1);
    	}
    	//printf("%d", counter);
    	counter++;
    }
    fclose(history);
}

// Find the number of words in an array
int array_length(char **words) {
	int counter = 0;
	while (words[counter] != NULL) {
		counter++;
	}
	return counter;
}

// Check the number of '<' and '>' in the words array
int check_num_of_arrows(char **words) {
	int counter = 0;
	int num = 0;
	while (words[counter] != NULL) {
		if (strcmp(words[counter], ">") == 0 || strcmp(words[counter], "<") == 0) {
			num++;
		}
		counter++;
	}
	return num;
}

// Check whether the command is builtin and hence we do not need to run posix_spawn
int check_builtin(char *words) {
	if (strcmp(words, "history") == 0 || strcmp(words, "cd") == 0 || strcmp(words, "pwd") == 0) {
		return 1;
	}
	return 0;
}

// Finds the path for the appropriate executable file
char *pathname_string(int start, char **path, char **words) {
	char *add_slash = concat("/", words[start]);
	char *pathname = concat(path[0], add_slash);
	if (strrchr(words[start], '/') == NULL) {
		int counter = 0;

		while (is_executable(pathname) != 1 && path[counter+1] != NULL) {
        	counter++;
        	pathname = concat(path[counter], add_slash);
 			}
	}
	return pathname;
}

// Removes the arrows and file names from the words array, leaving only the execute command and
// its arguments
char *new_commandline(int start, int difference, char **words, int length) {
	char *new_string = concat(words[start], " ");
	int increment = start + 1;
	while (words[increment] != NULL && increment < length - difference) {
		new_string = concat(new_string, words[increment]);
		new_string = concat(new_string, " ");
		increment++;
	}
	return new_string;
}

// This function essentially globs the words array before tokenising it and then returning the tokens
char **command_words2(char **words) {
	glob_t matches;

	int counter = 1;
	
	char *new_program = concat(words[0], " ");

	while (words[counter] != NULL) {
		int result = glob(words[counter], GLOB_NOCHECK|GLOB_TILDE, NULL, &matches);

		if (result == GLOB_NOMATCH) {
			char *add_space = concat(words[counter], " ");
			new_program = concat(new_program, add_space);
		} else {
			for (int counter1 = 0; counter1 < matches.gl_pathc; counter1++) {
				char *add_space = concat(matches.gl_pathv[counter1], " ");
				new_program = concat(new_program, add_space);
			}
		}
		counter++;
	}
	char **new_command = tokenize(new_program, WORD_SEPARATORS, SPECIAL_CHARS);
	return new_command;
}

void exit_status(pid_t pid, char *pathname) {
	int exit_status;
    if(waitpid(pid, &exit_status, 0) == -1) {
    	perror("waitpid");
    	return;
    }
    printf("%s exit status = %d\n", pathname, WEXITSTATUS(exit_status));
}

//
// Implement the `exit' shell built-in, which exits the shell.
//
// Synopsis: exit [exit-status]
// Examples:
//     % exit
//     % exit 1
//
static void do_exit(char **words) {
    int exit_status = 0;

    if (words[1] != NULL) {
        if (words[2] != NULL) {
            fprintf(stderr, "exit: too many arguments\n");
        } else {
            char *endptr;
            exit_status = (int)strtol(words[1], &endptr, 10);
            if (*endptr != '\0') {
                fprintf(stderr, "exit: %s: numeric argument required\n",
                        words[1]);
            }
        }
    }

    exit(exit_status);
}


//
// Check whether this process can execute a file.
// Use this function when searching through the directories
// in the path for an executable file
//
static int is_executable(char *pathname) {
    struct stat s;
    return
        // does the file exist?
        stat(pathname, &s) == 0 &&
        // is the file a regular file?
        S_ISREG(s.st_mode) &&
        // can we execute it?
        faccessat(AT_FDCWD, pathname, X_OK, AT_EACCESS) == 0;
}


//
// Split a string 's' into pieces by any one of a set of separators.
//
// Returns an array of strings, with the last element being `NULL';
// The array itself, and the strings, are allocated with `malloc(3)';
// the provided `free_token' function can deallocate this.
//
static char **tokenize(char *s, char *separators, char *special_chars) {
    size_t n_tokens = 0;
    // malloc array guaranteed to be big enough
    char **tokens = malloc((strlen(s) + 1) * sizeof *tokens);


    while (*s != '\0') {
        // We are pointing at zero or more of any of the separators.
        // Skip leading instances of the separators.
        s += strspn(s, separators);

        // Now, `s' points at one or more characters we want to keep.
        // The number of non-separator characters is the token length.
        //
        // Trailing separators after the last token mean that, at this
        // point, we are looking at the end of the string, so:
        if (*s == '\0') {
            break;
        }

        size_t token_length = strcspn(s, separators);
        size_t token_length_without_special_chars = strcspn(s, special_chars);
        if (token_length_without_special_chars == 0) {
            token_length_without_special_chars = 1;
        }
        if (token_length_without_special_chars < token_length) {
            token_length = token_length_without_special_chars;
        }
        char *token = strndup(s, token_length);
        assert(token != NULL);
        s += token_length;

        // Add this token.
        tokens[n_tokens] = token;
        n_tokens++;
    }

    tokens[n_tokens] = NULL;
    // shrink array to correct size
    tokens = realloc(tokens, (n_tokens + 1) * sizeof *tokens);

    return tokens;
}



//
// Free an array of strings as returned by `tokenize'.
//
static void free_tokens(char **tokens) {
    for (int i = 0; tokens[i] != NULL; i++) {
        free(tokens[i]);
    }
    free(tokens);
}

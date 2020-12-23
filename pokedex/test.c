#include <stdio.h>
#include <stdlib.h>

int name_length(char pokemon_name);

int main(void) {
	int counter = 0;
	char* help = 'Balbasaur';
    counter = name_length(help);
    printf("%d, counter");
    
	return 0;
}

int name_length(char pokemon_name) {
    int counter = 0;
    int i = 0;
    char* name = &pokemon_name;
    while (name[i] != '\0') {
        if (name[i] == ' ' || name[i] == '-' || (name[i] >= 'a' && name[i] <= 'z') || (name[i] >= 'A' && name[i] <= 'Z')) {
            counter++;
        }
        i++;
    }
    return counter;
}
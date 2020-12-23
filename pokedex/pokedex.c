// Assignment 2 19T1 COMP1511: Pokedex
// pokedex.c
//
// This program was written by WILLIAM SU (z5264299)
// on INSERT-DATE-HERE
//
// Version 1.0.0: Assignment released.
// Version 1.0.1: Minor clarifications about `struct pokenode`.
// Version 1.1.0: Moved destroy_pokedex function to correct location.
// Version 1.1.1: Renamed "pokemon_id" to "id" in change_current_pokemon.

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// Add any extra #includes your code needs here.
//
// But note you are not permitted to use functions from string.h
// so do not #include <string.h>

#include "pokedex.h"

// Add your own #defines here.
#define TRUE 1
#define FALSE 0
#define NONE -1

// Note you are not permitted to use arrays in struct pokedex,
// you must use a linked list.
//
// You are also not permitted to use arrays in any of the functions
// below.
//
// The only exception is that char arrays are permitted for
// search_pokemon and functions it may call, as well as the string
// returned by pokemon_name (from pokemon.h).
//
// You will need to add fields to struct pokedex.
// You may change or delete the head field.

struct pokedex {
    struct pokenode *head; // LINK TO START TO LINKED LIST (NODES )
};


// You don't have to use the provided struct pokenode, you are free to
// make your own struct instead.
// If you use the provided struct pokenode, you will need to add fields
// to it to store other information.

struct pokenode {
    struct pokenode *next;
    Pokemon         pokemon;
    // Determine whether the pokemon has been found yet
    int found;
    // Determine which pokemon is currently selected
    int current_selected;
    // The id of the evolution of the pokemon
    int evolution_id;
};

// Add any other structs you define here.


// Add prototypes for any extra functions you create here.
void add_to_end(Pokedex pokedex, struct pokenode *node);
struct pokenode *new_pokenode(Pokemon pokemon);
int name_length(Pokedex pokedex, char *pokemon_name);
void print_found_pokemon_details (struct pokenode *node);
void print_not_found_pokemon_details(struct pokenode *node, Pokedex pokedex);
void print_pokemon_list (struct pokenode *node, Pokedex pokedex);
void print_evolution_first (struct pokenode *node);
void print_evolution_subsequent (struct pokenode *node);
// void clone_pokenode_type (Pokedex pokedex, pokemon_type type); NOT WORKING

// You need to implement the following 20 functions.
// In other words, replace the lines calling fprintf & exit with your code.
// You can find descriptions of what each function should do in pokedex.h


Pokedex new_pokedex(void) {
    Pokedex new_pokedex = malloc(sizeof (struct pokedex)); // MAKES US A NEW VARIABLE BASED ON THE STRUCT POKEDEX
    assert(new_pokedex != NULL); // CHECKS IF WE HAVE GIVEN SOME MEMORY
    new_pokedex->head = NULL;
    // clone_pokenode_type (pokedex, type);
    return new_pokedex;
}

////////////////////////////////////////////////////////////////////////
//                         Stage 1 Functions                          //
////////////////////////////////////////////////////////////////////////

void add_pokemon(Pokedex pokedex, Pokemon pokemon) {
    // CREATE NEW NODE FOR NEW POKEMON
    // New_pokenode(pokemon) calls functions that creates a new pokenode
    // Add_to_end function adds the pokenode to the pokedex in the order in which they are added
    struct pokenode *node = new_pokenode(pokemon);
    struct pokenode *loopingNode = pokedex->head;
    while (loopingNode != NULL) {
        if (pokemon_id(loopingNode->pokemon) == pokemon_id(node->pokemon)) {
            printf("Error, pokemon already inside pokedex\n");
            exit(1);
        }
        loopingNode = loopingNode->next;
    }
    add_to_end(pokedex, node);
}

void detail_pokemon(Pokedex pokedex) {
    // Set loopingNode to head of pokedex
    struct pokenode *loopingNode = pokedex->head;
    // Check every pokenode within the pokedex
    while (loopingNode != NULL) {
        // Check for the pokenode that is currently selected
        if (loopingNode->current_selected == TRUE) {
            // Check if the pokemon has been found so that it will print appropriate information about it
            if (loopingNode->found == TRUE) {
                print_found_pokemon_details (loopingNode);
            // Check if the pokemon has not been found
            } else if (loopingNode->found == FALSE) {
                print_not_found_pokemon_details(loopingNode, pokedex);
            }
        }
        // Go to the next pokenode
        loopingNode = loopingNode->next;
    }
}

Pokemon get_current_pokemon(Pokedex pokedex) {
    // Set loopingNode to first pokenode inside the pokedex
    struct pokenode *loopingNode = pokedex->head;
    struct pokenode *returnNode = pokedex->head;
    // Variable to terminate the while loop once the currently selected pokenode has been found
    int limiter = 0;
    if (loopingNode != NULL) {
        while (loopingNode != NULL && limiter < 1) {
            if (loopingNode->current_selected == TRUE) {
                returnNode = loopingNode; 
                limiter++;
            }
            loopingNode = loopingNode->next;
        }
        return returnNode->pokemon; 
    // If there are no currently selected pokemon (pokedex is empty), print an error message and return NULL
    } else {
        printf("Error! Exiting because there are no Pokemon in the Pokedex\n");
        return NULL;
    }
}

void find_current_pokemon(Pokedex pokedex) {
    // Set loopingNode to first pokenode inside the pokedex
    struct pokenode *loopingNode = pokedex->head;
    while (loopingNode != NULL) {
        // Find the pokenode that is currently selected
        if (loopingNode->current_selected == TRUE) {
            // Change the found variable inside the pokenode to TRUE
            loopingNode->found = TRUE;
        }
        loopingNode = loopingNode->next;
    }
}

void print_pokemon(Pokedex pokedex) {
    // Set curr to first pokenode inside the pokedex
    struct pokenode *curr = pokedex->head;
    
    if (curr!= NULL) {
        while (curr != NULL) {
            print_pokemon_list (curr, pokedex);
            curr = curr->next;
        }
    }
}

////////////////////////////////////////////////////////////////////////
//                         Stage 2 Functions                          //
////////////////////////////////////////////////////////////////////////

void next_pokemon(Pokedex pokedex) {
    // Set loopingNode to first pokenode inside the pokedex
    struct pokenode *loopingNode = pokedex->head;
    // Set limiter to void the while loop once the currently selected pokemon has changed
    int limiter = 0;
    while (loopingNode != NULL && limiter < 1) {
        // Find the pokemon that is currently selected
        if (loopingNode->current_selected == TRUE) {
            // If the currently selected pokemon is not the last pokenode
            if (loopingNode->next != NULL) {
                // Change the currently selected pokenode to FALSE
                loopingNode->current_selected = FALSE;
                // Set the next pokenode as the currently selected one
                loopingNode->next->current_selected = TRUE;
                limiter++;
            // If the currently selected pokemon is the last pokenode, make no change
            } else {
                limiter++;
            }   
        }
        loopingNode = loopingNode->next;
    }
}

void prev_pokemon(Pokedex pokedex) {
    // Set loopingNode to first pokenode inside the pokedex
    struct pokenode *loopingNode = pokedex->head;
    // Set previousNode to be the pokenode one before loopingNode
    struct pokenode *previousNode = NULL;
    // Set limiter to void while loop once the currently selected pokemon has changed
    int limiter = 0;

    while (loopingNode != NULL && limiter < 1) {
        // Find the pokenode that is currently selected
        if (loopingNode->current_selected == TRUE) {
            // If the pokenode is the head of the pokedex, make no change
            if (previousNode == NULL) {
                limiter++;
            // If the pokenode is not the head of the pokedex
            } else {
                // Change the currently selected pokenode to the previous one
                loopingNode->current_selected = FALSE;
                previousNode->current_selected = TRUE;
                limiter++;
            }
        }
        // Increment both nodes forward one
        previousNode = loopingNode;
        loopingNode = loopingNode->next;
    }
}

void change_current_pokemon(Pokedex pokedex, int id) {
    // Set loopingNode to first pokenode inside the pokedex
    struct pokenode *loopingNode = pokedex->head;
    // Set checkNode to first pokenode inside the pokedex
    struct pokenode *checkNode = pokedex->head;
    int counter = 0;

    // Use this while loop to check whether the id inputed matches any of the ids within the pokedex
    // counter = 1 if the id matches one in the pokedex
    while (checkNode != NULL) {
        if (pokemon_id(checkNode->pokemon) == id) {
            counter++;
        }
        checkNode = checkNode->next;
    }
    // COMPARE THE IDS AND MAKE THE CORRECT CHANGE TO CURRENTLY SELECTED
    while (loopingNode != NULL && counter == 1) {
        // Change the pokemon matching the input id to become the currently selected one
        if (pokemon_id(loopingNode->pokemon) == id) {
            loopingNode->current_selected = TRUE;
        }
        // Find the pokemon that was originally selected and deselect it
        // I.e. the pokemon whose id does not match the one inputed but the value of the current_selected variable within the pokenode is TRUE
        if (pokemon_id(loopingNode->pokemon) != id && loopingNode->current_selected == TRUE) {
            loopingNode->current_selected = FALSE;
        }
        loopingNode = loopingNode->next;
    }
    // GO BACK THROUGH THE POKEDEX AND DESELECT THE ONE THAT WASN'T CHANGED.


}

void remove_pokemon(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    struct pokenode *previousNode = NULL;
    int limiter = 0;
    
    // Delete first node of the pokedex
    if (previousNode == NULL) {
        if (loopingNode->current_selected == TRUE) {
            if (loopingNode->next != NULL) {
                // Let previousNode equal to pokenode that is to be deleted
                previousNode = loopingNode;
                // Increment loopingNode to the pokenode that is to be the new head
                loopingNode = loopingNode->next;
                // Set the new head of the linked list
                pokedex->head = loopingNode;
                // Free the memory stored in the pokemon struct 
                destroy_pokemon(previousNode->pokemon);
                loopingNode->current_selected = TRUE;
                // Free the memory stores in the pokenode struct
                free(previousNode);
                limiter++;
            } else {
                destroy_pokemon(loopingNode->pokemon);
                free(loopingNode);
                pokedex->head = NULL;
                limiter++;
            }
        }
    } 
    while (loopingNode != NULL && limiter < 1) {
        // Delete last node
        if (loopingNode->next == NULL && loopingNode->current_selected == TRUE) {
            // Set the last pokenode to NULL
            previousNode->next = NULL;
            // previousNode now becomes the new last pokenode within the linked list
            previousNode->current_selected = TRUE;
            // Free memory allocated to both the pokemon and pokenode struct
            destroy_pokemon(loopingNode->pokemon);
            free(loopingNode);
            limiter++;
        } else {
            // Delete a node inbetween
            if (loopingNode->current_selected == TRUE) {
                // Link the pokenode before the one deleted to the pokenode after the one deleted
                previousNode->next = loopingNode->next;
                previousNode->next->current_selected = TRUE;
                // Free memory allocated to both the pokemon and pokenode struct
                destroy_pokemon(loopingNode->pokemon);
                free(loopingNode);
                limiter++;
            }
        }
        if (limiter < 1) {
            previousNode = loopingNode;
            loopingNode = loopingNode->next;
        }
    }
}

void destroy_pokedex(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    while (loopingNode != NULL) {
        struct pokenode *currNode = loopingNode;
        // Increment loopingNode to the next one
        loopingNode = loopingNode->next;
        // Remove memory allocate to the previous node
        destroy_pokemon(currNode->pokemon);
        free(currNode);
    }
    free(pokedex);
}

////////////////////////////////////////////////////////////////////////
//                         Stage 3 Functions                          //
////////////////////////////////////////////////////////////////////////

void go_exploring(Pokedex pokedex, int seed, int factor, int how_many) {
    // Generate random numbers
    srand(seed);
    int counter = 0;
    int counter1 = 0;
    
    // No Pokemon in Pokedex with an id that is inbetween the two parameters.
    struct pokenode *checkNode = pokedex->head;
    while (checkNode != NULL) {
        // Check if there are any pokemon in the pokedex with an id between the two parameters
        if (pokemon_id(checkNode->pokemon) >= 0 && pokemon_id(checkNode->pokemon) <= factor - 1) {
            // Increase counter1 is there are. I.e. if there aren't any, counter1 will be equal to 0
            counter1++;
        }
        checkNode = checkNode->next;
    }
    // If there are no pokemon in the pokedex with an id between parameters, print an error message.
    if (counter1 == 0) {
        printf("Exiting, no Pokemon in Pokedex with an ID between the parameters\n");
        exit(1);
    }
    // While loop continues until it reaches the value of how_many
    while (counter < how_many) {
        struct pokenode *loopingNode = pokedex->head;
        // Generate a random number and divided it by the factor so that all generated numbers are between 0 and factor-1
        int random_number = rand() % factor;
        while (loopingNode != NULL) {
            // If pokemon id matches the number randomly generated, record the pokemon as found in the pokedex.
            if (pokemon_id(loopingNode->pokemon) == random_number) {
                loopingNode->found = TRUE;
                counter++;
            }
            loopingNode = loopingNode->next;
        }
    }
}

int count_found_pokemon(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    // Set counter to record the amount of found pokemon
    int counter = 0;

    // No pokemon inside the pokedex
    if (loopingNode == NULL) {
        return 0;
    } else {
        // While loopingNode is not the last pokenode
        while (loopingNode->next != NULL) {
            // If the pokemon is found, increase the counter by 1
            if (loopingNode->found == TRUE) {
                counter++;
            }
            loopingNode = loopingNode->next;
        }
        // Since the above while loops stops once it reaches the last pokenode, we must consider whether the last one is found or not.
        if (loopingNode->found == TRUE) {
            counter++;
        }
        return counter;
    }
}

int count_total_pokemon(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    // Counter to measure value of pokemon in pokedex. This has been set to the value one as our while loop stops once it reaches the last pokenode and hence this accounts for it.
    int counter = 1;

    // No pokemon inside the pokedex
    if (loopingNode == NULL) {
        return 0;
    } else {
        // While loopingNode is not the last pokenode
        while (loopingNode->next != NULL) {
            counter++;
            loopingNode = loopingNode->next;
        }
        return counter;
    }
}

////////////////////////////////////////////////////////////////////////
//                         Stage 4 Functions                          //
////////////////////////////////////////////////////////////////////////

void add_pokemon_evolution(Pokedex pokedex, int from_id, int to_id) {
    struct pokenode *loopingNode = pokedex->head;
    // Set up checkNode to check that both the inputed ids match ids within the pokedex
    struct pokenode *checkNode = pokedex->head;
    // Counter to measure the amount of times the id of the pokemon matches the inputed ids.
    int counter = 0;

    // Check if the inputed ids are the same
    // If they are, exit the program
    if (from_id == to_id) {
        printf("Error, both the ids entered are the same\n");
        exit(1);
    }

    // If the id of a pokemon is equal to one of the inputed ids, increase the counter by 1
    while (checkNode != NULL) {
        if (pokemon_id(checkNode->pokemon) == from_id || pokemon_id(checkNode->pokemon) == to_id) {
            counter++;
        }
        checkNode = checkNode->next;
    }

    // If both the inputed ids match pokemon inside the pokedex, counter should have the value of 2
    // If the value of counter is not 0, exit the program
    if (counter != 2) {
        printf("Error, one or both of the inputed ids does not match any Pokemon within the pokedex\n");
        exit(1);
    }

    // If both the inputed ids match pokemon inside the pokedex, set the evolution_id component of the pokenode to equal the value of to_id
    while (loopingNode != NULL) {
        if (pokemon_id(loopingNode->pokemon) == from_id) {
            loopingNode->evolution_id = to_id;
        }
        loopingNode = loopingNode->next;
    }
}

void show_evolutions(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    int counter = 0;

    // Find the currently selected pokemon and print approriate output
    while (loopingNode != NULL && counter == 0) {
        if (loopingNode->current_selected == TRUE) {
            print_evolution_first (loopingNode);
            counter++;
        }
        // Stop the program from further incrementing when the currently selected pokemon has been found
        // loopingNode stays on the pokenode that is currently selected
        if (counter == 0) {
            loopingNode = loopingNode->next;
        }

    }
    // Find the pokemon that matches the evolution id
    // If the pokenode evolution_id does not equal -1, it means that it has a valid evolution next
    if (loopingNode->evolution_id != NONE) { 
        while (loopingNode->evolution_id != NONE) {
            struct pokenode *evolutionNode = pokedex->head;
            counter = 0;
            while (evolutionNode != NULL && counter == 0) {
                // Loop until the pokenode that contains the id of the pokemon evolution is found
                if (pokemon_id(evolutionNode->pokemon) == loopingNode->evolution_id) {
                    print_evolution_subsequent (evolutionNode);
                    counter++;
                }
                // Stop further incrementations so evolutionNode stays on the correct pokenode (the evolution of the currently selected one)
                if (counter == 0) {
                    evolutionNode = evolutionNode->next;
                }
            }
            // Let loopingNode be the pokenode of the evolution so that this while loop can continue and determine whether there are further evolutions and so on
            loopingNode = evolutionNode;
        }
    }
    printf("\n");
}

int get_next_evolution(Pokedex pokedex) {
    struct pokenode *loopingNode = pokedex->head;
    // Set return_value to the default evolution_id value
    int return_value = NONE;

    if (loopingNode == NULL) {
        printf("Error, not pokemon currently stored in pokedex\n");
        exit(1);
    }

    while (loopingNode != NULL) {
        // Find the currently selected pokenode
        if (loopingNode->current_selected == TRUE) {
            // If there are valid evolutions for the currently selected pokemon, set return_value to be the evolution_id of the pokemon
            if (loopingNode->evolution_id != NONE) {
                return_value = loopingNode->evolution_id;
            } 
        }
        loopingNode = loopingNode->next;
    }
    // If return_value does not remain as NONE, print the id of the evolution
    // If reutrn_value retains the value of NONE, it indicates that the currently selected pokemon has no evolution and hence return DOES_NOT_EVOLVE
    if (return_value != NONE) {
        return return_value;
    } else {
        return DOES_NOT_EVOLVE;
    }
}

////////////////////////////////////////////////////////////////////////
//                         Stage 5 Functions                          //
////////////////////////////////////////////////////////////////////////

Pokedex get_pokemon_of_type(Pokedex pokedex, pokemon_type type) {
    fprintf(stderr, "exiting because you have not implemented the get_pokemon_of_type function in pokedex.c\n");
    exit(1);
    //new_pokedex();
    
}

Pokedex get_found_pokemon(Pokedex pokedex) {
    fprintf(stderr, "exiting because you have not implemented the get_found_pokemon function in pokedex.c\n");
    exit(1);
}

Pokedex search_pokemon(Pokedex pokedex, char *text) {
    fprintf(stderr, "exiting because you have not implemented the search_pokemon function in pokedex.c\n");
    exit(1);
}

// Add definitions for your own functions below.
// Make them static to limit their scope to this file.
struct pokenode *new_pokenode(Pokemon pokemon) {
    struct pokenode *node;
    node = malloc(sizeof(struct pokenode));
    node->pokemon = pokemon;
    node->found = FALSE;
    node->next = NULL;
    node->current_selected = FALSE;
    node->evolution_id = NONE;
    return node;
};
void add_to_end(Pokedex pokedex, struct pokenode *node) {
    // POKEDEX IS EMPTY, PUT FIRST POKEMON IN
    struct pokenode *loopingNode = pokedex->head;
    struct pokenode *previousNode = NULL;

    while (loopingNode != NULL) {
        previousNode = loopingNode;
        loopingNode = loopingNode->next;
    }
    struct pokenode *new_pokenode = node;
    if (pokedex->head == NULL) {
        pokedex->head = new_pokenode;
        pokedex->head->current_selected = TRUE;
    } else {
        previousNode->next = new_pokenode;
    }
        
    
}
int name_length(Pokedex pokedex, char *pokemon_name) {
    int counter = 0;
    int i = 0;
    char* name = pokemon_name;
    while (name[i] != '\0') {
        if (name[i] == ' ' || name[i] == '-' || (name[i] >= 'a' && name[i] <= 'z') || (name[i] >= 'A' && name[i] <= 'Z')) {
            counter++;
        }
        i++;
    }
    return counter;
}

// NOT WORKING
/*void clone_pokenode_type (Pokedex pokedex, pokemon_type type) {
    struct pokenode *loopingNode = NULL;
    struct pokenode *loopingNode1 = pokedex->head;
    struct pokenode *clone_node;

    while (loopingNode1 != NULL) {
        if ((pokemon_first_type(loopingNode1->pokemon) == type && loopingNode1->found == TRUE) || (pokemon_second_type(loopingNode->pokemon) == type && loopingNode1->found == TRUE)) {
            clone_node = malloc(sizeof(struct pokenode));
            clone_node = loopingNode1;
            clone_node->evolution_id = NONE;
            clone_node->current_selected = FALSE;
            if (loopingNode == NULL) {
                loopingNode = clone_node;
                loopingNode->current_selected = TRUE;
            } else {
                loopingNode->next = clone_node;
                loopingNode = loopingNode->next;
            }
        }
        loopingNode1 = loopingNode1->next;
    }
} */

void print_found_pokemon_details (struct pokenode *node) {
    // %03d to make sure that the id contains 3 digits
    printf("Id: %03d\n", pokemon_id(node->pokemon));
    printf("Name: %s\n", pokemon_name(node->pokemon));
    // %.1lf to make sure that the height and weight are to one decimal point and there is no trail of 0s
    printf("Height: %.1lfm\n", pokemon_height(node->pokemon));
    printf("Weight: %.1lfkg\n", pokemon_weight(node->pokemon));
    if (pokemon_first_type(node->pokemon) == 0) {
        printf("Type: %s\n", pokemon_type_to_string(pokemon_second_type(node->pokemon)));
    } else if (pokemon_second_type(node->pokemon) == 0) {
        printf("Type: %s\n", pokemon_type_to_string(pokemon_first_type(node->pokemon)));
    } else {
        printf("Type: %s %s\n", pokemon_type_to_string(pokemon_first_type(node->pokemon)), pokemon_type_to_string(pokemon_second_type(node->pokemon)));
    }
}

void print_not_found_pokemon_details(struct pokenode *node, Pokedex pokedex) {
    printf("Id: %03d\n", pokemon_id(node->pokemon));
    // Call name_length function to check the number of digits in the pokemon's name so that the approriate amount of * are printed
    int limit = name_length(pokedex, pokemon_name(node->pokemon));
    int counter = 0;
    printf("Name: ");
    // Counter to print the amount of * that is equivalent to the number of letters in the pokemon's name
    while (counter < limit) {
        printf("*");
        counter++;
    }
    printf("\n");
    printf("Height: --\n");
    printf("Weight: --\n");
    printf("Type: --\n");
}

void print_pokemon_list (struct pokenode *node, Pokedex pokedex) {
    // Find the pokenode that is currently selected
    if (node->current_selected == TRUE) {
        // Check if pokemon is found so that if it is, the pokemon name is printed
        if (node->found == TRUE) {
            printf("--> #%03d: %s\n", pokemon_id(node->pokemon), pokemon_name(node->pokemon));
        } else {
            // Find number of digits within the pokemon's name
            int limit = name_length(pokedex, pokemon_name(node->pokemon));
            int counter = 0;
            printf("--> #%03d: ", pokemon_id(node->pokemon));
            // Print appropriate amount of *
            while (counter < limit) {
                printf("*");
                counter++;
            }
            printf("\n");
        }
    // If the pokenode is not the one currently selected   
    } else if (node->current_selected == FALSE) {
        if (node->found == TRUE) {
            printf("    #%03d: %s\n", pokemon_id(node->pokemon), pokemon_name(node->pokemon));
        } else {
            int limit = name_length(pokedex, pokemon_name(node->pokemon));
            int counter = 0;
            printf("    #%03d: ", pokemon_id(node->pokemon));
            while (counter < limit) {
                printf("*");
                counter++;
            }
            printf("\n");
        }
    }
}

void print_evolution_first (struct pokenode *node) {
     // Check whether the currently selected pokemon has been found
    if(node->found == TRUE) {
        // Check if any of the pokemons have a type 'NONE' so that only one type is printed
        if (pokemon_first_type(node->pokemon) == 0) {
            printf("#%03d %s [%s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_second_type(node->pokemon)));
        } else if (pokemon_second_type(node->pokemon) == 0) {
            printf("#%03d %s [%s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_first_type(node->pokemon)));
        } else {
            printf("#%03d %s [%s, %s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_first_type(node->pokemon)), pokemon_type_to_string(pokemon_second_type(node->pokemon)));
        }
        // If the pokemon has not been found
    } else {
        printf("#%03d ???? [????] ", pokemon_id(node->pokemon));
    }
}

void print_evolution_subsequent (struct pokenode *node) {
    if(node->found == TRUE) {
        // Determine whether the pokemon has only one or two types
        if (pokemon_first_type(node->pokemon) == 0) {
            printf("--> #%03d %s [%s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_second_type(node->pokemon)));
        } else if (pokemon_second_type(node->pokemon) == 0) {
            printf("--> #%03d %s [%s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_first_type(node->pokemon)));
        } else {
            printf("--> #%03d %s [%s, %s] ", pokemon_id(node->pokemon), pokemon_name(node->pokemon), pokemon_type_to_string(pokemon_first_type(node->pokemon)), pokemon_type_to_string(pokemon_second_type(node->pokemon)));
        }
    } else {
        printf("--> #%03d ???? [????] ", pokemon_id(node->pokemon));
    }
}
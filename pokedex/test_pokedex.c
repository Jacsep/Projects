// Assignment 2 19T1 COMP1511: Pokedex
// test_pokedex.c
//
// This file allows you to automatically test the functions you
// implement in pokedex.c.
//
// This program was written by WILLIAM SU (z5264299)
// on INSERT-DATE-HERE
//
// Version 1.0.0: Assignment released.
// Version 1.0.1: Added pointer check for the provided tests.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "pokedex.h"

// Add your own #defines here.


// Sample data on Bulbasaur, the Pokemon with pokemon_id 1.
#define BULBASAUR_ID 1
#define BULBASAUR_NAME "Bulbasaur"
#define BULBASAUR_HEIGHT 0.7
#define BULBASAUR_WEIGHT 6.9
#define BULBASAUR_FIRST_TYPE GRASS_TYPE
#define BULBASAUR_SECOND_TYPE POISON_TYPE

// Sample data on Ivysaur, the Pokemon with pokemon_id 2.
#define IVYSAUR_ID 2
#define IVYSAUR_NAME "Ivysaur"
#define IVYSAUR_HEIGHT 1.0
#define IVYSAUR_WEIGHT 13.0
#define IVYSAUR_FIRST_TYPE GRASS_TYPE
#define IVYSAUR_SECOND_TYPE POISON_TYPE

// Data on Venusaur, the Pokemon with pokemon_id 3.
#define VENUSAUR_ID 3
#define VENUSAUR_NAME "Venusaur"
#define VENUSAUR_HEIGHT 1.3
#define VENUSAUR_WEIGHT 18.2
#define VENUSAUR_FIRST_TYPE GRASS_TYPE
#define VENUSAUR_SECOND_TYPE POISON_TYPE

// Data on Charmander, the Pokemon with pokemon_id 4.
#define CHARMANDER_ID 4
#define CHARMANDER_NAME "Charmander"
#define CHARMANDER_HEIGHT 0.8
#define CHARMANDER_WEIGHT 12.6
#define CHARMANDER_FIRST_TYPE FIRE_TYPE
#define CHARMANDER_SECOND_TYPE NONE_TYPE

// Data on Charmeleon, the Pokemon with pokemon_id 5.
#define CHARMELEON_ID 5
#define CHARMELEON_NAME "Charmeleon"
#define CHARMELEON_HEIGHT 1.5
#define CHARMELEON_WEIGHT 17.6
#define CHARMELEON_FIRST_TYPE FIRE_TYPE
#define CHARMELEON_SECOND_TYPE NONE_TYPE

// Data on Charizard, the Pokemon with pokemon_id 6.
#define CHARIZARD_ID 6
#define CHARIZARD_NAME "Charizard"
#define CHARIZARD_HEIGHT 2.4
#define CHARIZARD_WEIGHT 20.5
#define CHARIZARD_FIRST_TYPE FIRE_TYPE
#define CHARIZARD_SECOND_TYPE FLYING_TYPE



// Add your own prototypes here.


// Tests for Pokedex functions from pokedex.c.
static void test_new_pokedex(void);
static void test_add_pokemon(void);
// static void test_get_found_pokemon(void);
static void test_next_pokemon(void);
static void test_prev_pokemon(void);
static void test_detail_pokemon(void);
static void test_count_pokemon(void);
static void test_evolutions_pokemon(void);
static void test_go_exploring(void);

// Helper functions for creating/comparing Pokemon.
static Pokemon create_bulbasaur(void);
static Pokemon create_ivysaur(void);
static Pokemon create_venusaur(void);
static Pokemon create_charmeleon(void);
static Pokemon create_charizard(void);
static Pokemon create_charmander(void);
static int is_same_pokemon(Pokemon first, Pokemon second);
static int is_copied_pokemon(Pokemon first, Pokemon second);



int main(int argc, char *argv[]) {
    printf("Welcome to the COMP1511 Pokedex Tests!\n");

    printf("\n==================== Pokedex Tests ====================\n");

    test_new_pokedex();
    test_add_pokemon();
    test_next_pokemon();
    test_prev_pokemon();
    test_detail_pokemon();
    test_count_pokemon();
    test_evolutions_pokemon();
    test_go_exploring();
    // test_get_found_pokemon();

    printf("\nAll Pokedex tests passed, you are Awesome!\n");
}


////////////////////////////////////////////////////////////////////////
//                     Pokedex Test Functions                         //
////////////////////////////////////////////////////////////////////////

// `test_new_pokedex` checks whether the new_pokedex and destroy_pokedex
// functions work correctly, to the extent that it can.
//
// It does this by creating a new Pokedex, checking that it's not NULL,
// then calling destroy_pokedex.
//
// Note that it isn't possible to check whether destroy_pokedex has
// successfully destroyed/freed the Pokedex, so the best we can do is to
// call the function and make sure that it doesn't crash..
static void test_new_pokedex(void) {
    printf("\n>> Testing new_pokedex\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("       --> Checking that the returned Pokedex is not NULL\n");
    assert(pokedex != NULL);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed new_pokedex tests!\n");
}

// `test_add_pokemon` checks whether the add_pokemon function works
// correctly.
//
// It does this by creating the Pokemon Bulbasaur (using the helper
// functions in this file and the provided code in pokemon.c), and
// calling add_pokemon to add it to the Pokedex.
//
// Some of the ways that you could extend these test would include:
//   - adding additional Pokemon other than just Bulbasaur,
//   - checking whether the currently selected Pokemon is correctly set,
//   - checking that functions such as `count_total_pokemon` return the
//     correct result after more Pokemon are added,
//   - ... and more!
static void test_add_pokemon(void) {
    printf("\n>> Testing add_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);

    // Count amount of pokemon once the first one has been added
    printf("    ... Counting total number of Pokemon inside the Pokedex\n");
    assert(count_total_pokemon(pokedex) == 1);

    // Adding additional Pokemon
    printf("    ... Creating Ivysaur\n");
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, ivysaur);

    // Checking whether currently selected Pokemon is correctly set to the first one added (Bulbasaur).
    printf("    ... Printing Pokemon List\n");
    print_pokemon(pokedex);

    // Checking if count_total_pokemon returns correct number of pokemons after adding one more
    printf("    ... Printing Total Number of Pokemons\n");
    assert(count_total_pokemon(pokedex) == 2);

    // Remove a pokemon and check that the currently selected one is the one removed
    printf("    ... Deleting Bulbasaur from the Pokedex\n");
    remove_pokemon(pokedex);

    // Print the list of Pokemon to make sure Bulbasaur (currently selected one) is removed and Ivysaur is now the new head and is currently selected
    printf("    ... Printing Pokemon List\n");
    print_pokemon(pokedex);
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    // Check whether the count_total_pokemon returns the correct number once a pokemon has been removed
    printf("    ... Printing Total Number of Pokemons\n");
    assert(count_total_pokemon(pokedex) == 1);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed add_pokemon tests!\n");
}

// `test_next_pokemon` checks whether the next_pokemon function works
// correctly.
//
// It does this by creating two Pokemon: Bulbasaur and Ivysaur (using
// the helper functions in this file and the provided code in pokemon.c).
//
// It then adds these to the Pokedex, then checks that calling the
// next_pokemon function changes the currently selected Pokemon from
// Bulbasaur to Ivysaur.
//
// Some of the ways that you could extend these tests would include:
//   - adding even more Pokemon to the Pokedex,
//   - calling the next_pokemon function when there is no "next" Pokemon,
//   - calling the next_pokemon function when there are no Pokemon in
//     the Pokedex,
//   - ... and more!
static void test_next_pokemon(void) {
    printf("\n>> Testing next_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    // Calling next_pokemon function when no Pokemon have been added. This function should do nothing and check to make sure the Pokedex still exists
    printf("    ... Moving to the next pokemon\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the returned Pokedex is not NULL\n");
    assert(pokedex != NULL);

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next pokemon\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    // Calling next_pokemon function when there are no pokemon after ivysaur
    printf("    ... Moving to the next pokemon\n");
    next_pokemon(pokedex);
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");
}


// `test_get_found_pokemon` checks whether the get_found_pokemon
// function works correctly.
//
// It does this by creating two Pokemon: Bulbasaur and Ivysaur (using
// the helper functions in this file and the provided code in pokemon.c).
//
// It then adds these to the Pokedex, sets Bulbasaur to be found, and
// then calls the get_found_pokemon function to get all of the Pokemon
// which have been found (which should be just the one, Bulbasaur).
//
// Some of the ways that you could extend these tests would include:
//   - calling the get_found_pokemon function on an empty Pokedex,
//   - calling the get_found_pokemon function on a Pokedex where none of
//     the Pokemon have been found,
//   - checking that the Pokemon in the new Pokedex are in ascending
//     order of pokemon_id (regardless of the order that they appeared
//     in the original Pokedex),
//   - checking that the currently selected Pokemon in the returned
//     Pokedex has been set correctly,
//   - checking that the original Pokedex has not been modified,
//   - ... and more!
/*static void test_get_found_pokemon(void) {
    printf("\n>> Testing get_found_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    // Testing get_found_pokemon function when Pokedex is empty
    printf("    ... Getting all found Pokemon\n");
    assert(count_found_pokemon(pokedex) ==  0);

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    // Testing get_found_pokemon function when no Pokemon in the pokedex is found
    printf("    ... Getting all found Pokemon\n");
    assert(count_found_pokemon(pokedex) ==  0);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(get_current_pokemon(pokedex) == bulbasaur);
    
    printf("    ... Setting Bulbasaur to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Getting all found Pokemon\n");
    Pokedex found_pokedex = get_found_pokemon(pokedex);

    printf("       --> Checking the correct Pokemon were copied and returned\n");
    assert(count_total_pokemon(found_pokedex) == 1);
    assert(count_found_pokemon(found_pokedex) == 1);
    assert(is_copied_pokemon(get_current_pokemon(found_pokedex), bulbasaur));

    printf("    ... Destroying both Pokedexes\n");
    destroy_pokedex(pokedex);
    destroy_pokedex(found_pokedex);

    printf(">> Passed get_found_pokemon tests!\n");
}*/


// Write your own Pokedex tests here!

// test whether the function 'prev_pokemon' works correctly.
// A new Pokedex is createed and then both Bulbasaur and Ivysaur are added to the Pokedex.
// Check that the currently selected Pokemon is the first one added (Bulbasaur)
// Testing the prev_pokemon function when the currently_selected Pokemon is the head of the linked list
// The next Pokemon is then set to currently selected and that is checked using assert
// Prev_function is then called to verify that it works when the currently selected Pokemon is not the head
static void test_prev_pokemon(void) {
    printf("\n>> Testing prev_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    // Calling prev_pokemon function when no Pokemon have been added. This function should do nothing and check to make sure the Pokedex still exists
    printf("    ... Moving to the next pokemon\n");
    prev_pokemon(pokedex);

    printf("       --> Checking that the returned Pokedex is not NULL\n");
    assert(pokedex != NULL);

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    // Check that when the function prev_pokemon is called on the first pokemon, no changes are made to the currently selected pokemon
    printf("       --> Moving on the previous Pokemon\n");
    prev_pokemon(pokedex);

    printf("       --> Checking the currently selected Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    // Making sure that the new pokemon becomes the currently selected pokemon
    printf("       --> Moving on the next Pokemon\n");
    next_pokemon(pokedex);

    printf("       --> Checking the currently selected Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    // Calling prev_pokemon to make sure it works when there is more than one Pokemon and the first Pokemon is not the one selected.
    printf("       --> Moving on the previous Pokemon\n");
    prev_pokemon(pokedex);

    printf("       --> Checking the currently selected Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");
}
    
// Checking that the details of found pokemon are correct and that pokemon not found are asterisks
// A new Pokedex is create and both Bulbasaur and Ivysaur are added.
// The details of the currently selected to ensure that is it by default set to not found
// The currently selected Pokemon is then moved to the next one and the details are printed before it has been found
// Ivysaur is then set to found and its details are printed which should include all its data.
static void test_detail_pokemon(void) {
    printf("\n>> Testing detail_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("    ... Printing details of Bulbasaur before it has been found\n");
    detail_pokemon(pokedex);

    // Checking that the details of the next Pokemon before it has been found is also asterisks
    printf("       --> Moving on the next Pokemon\n");
    next_pokemon(pokedex);
    assert(get_current_pokemon(pokedex) == ivysaur);

    printf("    ... Printing details of Ivysaur before it has been found\n");
    detail_pokemon(pokedex);

    // Find current Pokemon and print out the details after it has been found to see if find_current_pokemon works
    printf("    ... Setting Ivysaur to be found\n");\
    find_current_pokemon(pokedex);

    printf("    ... Printing details of Ivysaur after it has been found\n");
    detail_pokemon(pokedex);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");
}

// Testing count_found_pokemon and count_total_pokemon function
// Pokedex is create and both Bulbasaur and Ivysaur are added
// Count the total amount of Pokemon and total amount found
// Set Bulbasaur to be found and recount the total amount of Pokemon and total amount found
// Add another Pokemon (Venusaur) and recount the total amount of Pokemon and total amount found
static void test_count_pokemon(void) {
    printf("\n>> Testing both count_pokemon functions\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("    ... Counting total Pokemons and total found Pokemons\n");
    assert(count_found_pokemon(pokedex) == 0);
    assert(count_total_pokemon(pokedex) == 2);

    // Finding one Pokemon
    printf("    ... Setting Bulbasaur to be found\n");
    find_current_pokemon(pokedex);

    // Counting total and found Pokemon after one Pokemon has been found
    printf("    ... Counting total Pokemons and total found Pokemons\n");
    assert(count_found_pokemon(pokedex) == 1);
    assert(count_total_pokemon(pokedex) == 2);

    // Adding another Pokemon after
    printf("    ... Creating Venusaur\n");
    Pokemon venusaur = create_venusaur();

    printf("    ... Adding Venusaur to the Pokedex\n");
    add_pokemon(pokedex, venusaur);

    // Counting total and found Pokemon once Venusaur has been added
    printf("    ... Counting total Pokemons and total found Pokemons\n");
    assert(count_found_pokemon(pokedex) == 1);
    assert(count_total_pokemon(pokedex) == 3);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");
}

// Testing whether the evolution functions work
// Pokedex is created and Bulbasaur, Ivysaur and Venusaur are added to it
// Checking that by default all Pokemon has no evolution until the appropriate function has been called
// Check that the return on the initial get_next_evolution of Bulbasaur to be 'DOES_NOT_EVOLVE'
// Add an evolution to Bulbasaur to check that it is Ivysaur
// Reset the evolution to Bulbasaur and check that is it Venusaur
// Add Ivysaur as an evolution of Venusaur
// Print out the entire evolution line starting from Bulbasaur
static void test_evolutions_pokemon(void) {
    printf("\n>> Testing evolution functions\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Venusaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon venusaur = create_venusaur();

    printf("    ... Adding Bulbasaur, Ivysaur and Venusaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, venusaur);

    // Testing get_next_evolution when no evolutions have been added
    printf("    ... Getting the evolution of Bulbasaur\n");
    assert(get_next_evolution(pokedex) == DOES_NOT_EVOLVE);

    // Adding an evolution to Bulbasaur and checking that it is Ivysaur
    printf("    ... Adding Ivysaur as an evolution of Bulbasaur\n");
    add_pokemon_evolution(pokedex, 1, 2);
    assert(get_next_evolution(pokedex) == IVYSAUR_ID);

    // Adding Venusaur as an evolution of Bulbasaur to check whether this will correctly override the previous evolution added to Bulbasaur
    printf("    ... Adding Venusaur as an evolution of Bulbasaur\n");
    add_pokemon_evolution(pokedex, 1, 3);
    assert(get_next_evolution(pokedex) == VENUSAUR_ID);

    // Add Ivysaur as an evolution of Venusaur and check if the change_current_pokemon to a certain id works
    printf("    ... Adding Ivysaur as an evolution of Venusaur\n");
    add_pokemon_evolution(pokedex, 3, 2);
    change_current_pokemon(pokedex, 3);
    assert(get_next_evolution(pokedex) == IVYSAUR_ID);

    // Printing entire evolution line
    printf("    ... Printing the entire evolution line of Bulbasaur\n");
    show_evolutions(pokedex);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");

}
// Checking go_exploring function
// Pokedex is createa and Charmander, Ivysayr and Venusaur are added
// Go exploring is called with a large how_many value. This will most likely lead to all the Pokemon within the Pokedex to be found.
// Bulbasaur which has an extremely low Pokemon ID is added
// Go exploring is called with a large factor. This makes it unlikely that Bulbasaur will be found.
// Charmeleon and Charizard are then added which are two Pokemon with a relatively higher Pokemon ID.
// Go eporing is called with a small factor. This make it unlikely that Charmeleon or Charizard are found.
static void test_go_exploring(void) {
    printf("\n>> Testing go_exploring function\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Charmander, Ivysaur and Venusaur\n");
    Pokemon charmander = create_charmander();
    Pokemon ivysaur = create_ivysaur();
    Pokemon venusaur = create_venusaur();

    printf("    ... Adding Charmander, Ivysaur and Venusaur to the Pokedex\n");
    add_pokemon(pokedex, charmander);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, venusaur);

    // Testing when how_many is much larger than the number of Pokemon inside the Pokedex
    // Lower id number pokemon should be found more easily (e.g. ID 1)
    printf("    ... Going exploring with a large how_many value\n");
    go_exploring(pokedex, 123, 4, 100);

    printf("    ... Printing list of all Pokemons\n");
    print_pokemon(pokedex);

    // Testing when factor is really small
    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);

    printf("    ... Going exploring with a small factor value\n");
    go_exploring(pokedex, 123, 2, 5);

    printf("    ... Printing list of all Pokemons\n");
    print_pokemon(pokedex);

    // Testing when factor is really large
    // Unlikely to find any lower numbered ID pokemon
    printf("    ... Creating Charmeleon and Charizard\n");
    Pokemon charmeleon = create_charmeleon();
    Pokemon charizard = create_charizard();

    printf("    ... Adding Charmeleon and Charizard to the Pokedex\n");
    add_pokemon(pokedex, charmeleon);
    add_pokemon(pokedex, charizard);

    printf("    ... Going exploring with a small factor value\n");
    go_exploring(pokedex, 123, 50, 5);

    printf("    ... Printing list of all Pokemons\n");
    print_pokemon(pokedex);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);


    printf(">> Passed next_pokemon tests!\n");
}


////////////////////////////////////////////////////////////////////////
//                     Helper Functions                               //
////////////////////////////////////////////////////////////////////////

// Helper function to create Bulbasaur for testing purposes.
static Pokemon create_bulbasaur(void) {
    Pokemon pokemon = new_pokemon(
            BULBASAUR_ID, BULBASAUR_NAME,
            BULBASAUR_HEIGHT, BULBASAUR_WEIGHT,
            BULBASAUR_FIRST_TYPE,
            BULBASAUR_SECOND_TYPE
    );
    return pokemon;
}

// Helper function to create Ivysaur for testing purposes.
static Pokemon create_ivysaur(void) {
    Pokemon pokemon = new_pokemon(
            IVYSAUR_ID, IVYSAUR_NAME,
            IVYSAUR_HEIGHT, IVYSAUR_WEIGHT,
            IVYSAUR_FIRST_TYPE,
            IVYSAUR_SECOND_TYPE
    );
    return pokemon;
}

// Help function to create Venusaur for testing purposes.
static Pokemon create_venusaur(void) {
    Pokemon pokemon = new_pokemon(
            VENUSAUR_ID, VENUSAUR_NAME,
            VENUSAUR_HEIGHT, VENUSAUR_WEIGHT,
            VENUSAUR_FIRST_TYPE,
            VENUSAUR_SECOND_TYPE
    );
    return pokemon;
}

// Help function to create Charmander for testing purposes.
static Pokemon create_charmander(void) {
    Pokemon pokemon = new_pokemon(
            CHARMANDER_ID, CHARMANDER_NAME,
            CHARMANDER_HEIGHT, CHARMANDER_WEIGHT,
            CHARMANDER_FIRST_TYPE,
            CHARMANDER_SECOND_TYPE
    );
    return pokemon;
}

// Help function to create Charmeleon for testing purposes.
static Pokemon create_charmeleon(void) {
    Pokemon pokemon = new_pokemon(
            CHARMELEON_ID, CHARMELEON_NAME,
            CHARMELEON_HEIGHT, CHARMELEON_WEIGHT,
            CHARMELEON_FIRST_TYPE,
            CHARMELEON_SECOND_TYPE
    );
    return pokemon;
}

// Help function to create Charizard for testing purposes.
static Pokemon create_charizard(void) {
    Pokemon pokemon = new_pokemon(
            CHARIZARD_ID, CHARIZARD_NAME,
            CHARIZARD_HEIGHT, CHARIZARD_WEIGHT,
            CHARIZARD_FIRST_TYPE,
            CHARIZARD_SECOND_TYPE
    );
    return pokemon;
}


// Helper function to compare whether two Pokemon are the same.
// This checks that the two pointers contain the same address, i.e.
// they are both pointing to the same pokemon struct in memory.
//
// Pokemon ivysaur = new_pokemon(0, 'ivysaur', 1.0, 13.0, GRASS_TYPE, POISON_TYPE)
// Pokemon also_ivysaur = ivysaur
// is_same_pokemon(ivysaur, also_ivysaur) == TRUE
static int is_same_pokemon(Pokemon first, Pokemon second) {
    return first == second;
}

// Helper function to compare whether one Pokemon is a *copy* of
// another, based on whether their attributes match (e.g. pokemon_id,
// height, weight, etc).
// 
// It also checks that the pointers do *not* match -- i.e. that the
// pointers aren't both pointing to the same pokemon struct in memory.
// If the pointers both contain the same address, then the second
// Pokemon is not a *copy* of the first Pokemon.
// 
// This function doesn't (yet) check that the Pokemon's names match
// (but perhaps you could add that check yourself...).
static int is_copied_pokemon(Pokemon first, Pokemon second) {
    return (pokemon_id(first) == pokemon_id(second))
    &&  (first != second)
    &&  (pokemon_name(first) == pokemon_name(second))
    &&  (pokemon_height(first) == pokemon_height(second))
    &&  (pokemon_weight(first) == pokemon_weight(second))
    &&  (pokemon_first_type(first) == pokemon_first_type(second))
    &&  (pokemon_second_type(first) == pokemon_second_type(second));
}

// Write your own helper functions here!


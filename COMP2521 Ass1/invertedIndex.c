// COMP2521 Ass1
// z5264299 

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#include "invertedIndex.h"

#define MAX 100

// Struct for temporary Linked List
typedef struct tempFile {
	char *filename;
	struct tempFile *next;
} tempFile;


// Function Prototypes
InvertedIndexBST newBST(void);
TfIdfList newTfIdfList(void);
tempFile *scanFile(char *collectionFilename);
static InvertedIndexBST newBSTNode(char *str, char *str2, int totalNumber);
static FileList newFileListNode(char *str, int totalNumber);
static TfIdfList newTfIdfNode(char *str, double tf, double idf);
InvertedIndexBST BSTInsert(InvertedIndexBST t, char *str, char *str2, int totalNumber);
void BSTreeInfix (InvertedIndexBST tree, FILE *fp);
InvertedIndexBST BSTreeSearch(InvertedIndexBST tree, char *searchWord);
int countNumberWords (char *str);


// Normalise the word
// fscanf already removes all the white space, so we don't need to worry about that

char * normaliseWord(char *str) {
	int counter = 0;
	int stringLength = strlen(str);

	// Changing all characters to lowercase
	while (str[counter] != '\0') {
		if (str[counter] >= 'A' && str[counter] <= 'Z') {
			str[counter] = tolower(str[counter]);
		}
		counter++;
	}
	// If there last character is a puncutation mark
	if (str[stringLength-1] == '.' || str[stringLength-1] == ',' ||
		str[stringLength-1] == ';' || str[stringLength-1] == '?') {
		str[stringLength-1] = '\0';
	}
	return str;
}

InvertedIndexBST generateInvertedIndex(char *collectionFilename) {
	// Create a new BST using a helper function
	InvertedIndexBST invertedIndex = newBST();
	int totalNumber = 0;
	// Go into the collectFilename and store all the file names in a temp linked list
	tempFile *tempCollection = scanFile(collectionFilename);
	// Go into each individual text file and store the words within a BST
	while (tempCollection != NULL) {
		// Count the total number of words within a file
		totalNumber = countNumberWords(tempCollection->filename);
		// Open the individual word file
		FILE *individualFile = fopen(tempCollection->filename, "r");
		assert (individualFile != NULL); 
		char word[MAX];
		char *word2;
		while (fscanf(individualFile, "%s", word) != EOF) {
			// Substitute for strdup
		    word2 = malloc(sizeof(word)+1);
		    strcpy(word2, word);
		    // Insert the node into the BST
			invertedIndex = BSTInsert (invertedIndex, normaliseWord(word2), 
			tempCollection->filename, totalNumber);
		}
		fclose(individualFile);
		// Increment it so that it moves onto the next individual word file
		tempCollection = tempCollection->next;
	}
	return invertedIndex;
}

void printInvertedIndex(InvertedIndexBST tree) {
	// We essentially want to print out the words in infix order
	FILE *output = fopen("invertedIndex.txt", "w");
	BSTreeInfix(tree, output);
	fclose(output);
}

// Stage 2 Functions
// Descending order of tfidf values
// If same, ascending order of filename (must add this case)
// What if there are a bunch of with same tfidf
// Must go through all the ones with the same one and find appropriate place
TfIdfList calculateTfIdf(InvertedIndexBST tree, char *searchWord , int D) {
    // Create a new TfIdfList
    TfIdfList newList = newTfIdfList();
    // Find the node that matches the word
    InvertedIndexBST matchingNode = BSTreeSearch(tree, searchWord);
    FileList currentNode = matchingNode->fileList;
    double totalNumber = 0;
    int countEquality = 0;
    int countStop = 0;
    while (currentNode != NULL) {
        totalNumber++;
        currentNode = currentNode->next;
    }
    double idf = log10(D/totalNumber);
    currentNode = matchingNode->fileList;
    TfIdfList tail = NULL;
   	while (currentNode != NULL) {
   		// Make a new node
    	TfIdfList newNode = newTfIdfNode(currentNode->filename, idf, currentNode->tf);
    	countStop = 0;
    	// Insert in appropriate place
    	// We should deal with empty linked list
    	if (newList == NULL) {
    		newList = newNode;
    		tail = newNode;
    	} else {
    		// Check if there is equality first
    		countEquality = 0;
    		TfIdfList traversingNode = newList;
    		while (traversingNode != NULL) {
    			if (newNode->tfidf_sum == traversingNode->tfidf_sum) {
    				countEquality++;
    			}
    			traversingNode = traversingNode->next;
    		}
    		if (countEquality != 0) {
    			// If 0, skip this
    			TfIdfList previousNode3 = NULL;
    			TfIdfList currentNode3 = newList;
    			TfIdfList firstEqual = NULL;
    			TfIdfList lastEqual = NULL;
    			int countCheck = 0;
    			// Go through the list and find the first one that is the same and let firstEqual be that
    			while (currentNode3 != NULL && countCheck == 0) {
    				if (newNode->tfidf_sum == currentNode3->tfidf_sum) {
    					firstEqual = currentNode3;
    					countCheck++;
    				}
    				if (countCheck == 0) {
    					previousNode3 = currentNode3;
    					currentNode3 = currentNode3->next;
    				}
    			}
    			// Need to find last equal
    			currentNode3 = firstEqual;
    			while (currentNode3->tfidf_sum == newNode->tfidf_sum && currentNode3 != NULL) {
    				previousNode3 = currentNode3;
    				currentNode3 = currentNode3->next;
    			}
    			lastEqual = previousNode3;
    			// We have found the first node that is equal in tfidf value to the newNode
    			// Name is smaller than first one of the group that is same
    			previousNode3 = NULL;
    			currentNode3 = newList;
    			while (currentNode3 != NULL && countStop == 0) {
    			    // Smaller than the first node with the same ifidf value
    				if (strcmp(newNode->filename, currentNode3->filename) < 0 
    				&& currentNode3 == firstEqual) {
    				    // Check if it will become the new head
    					if (previousNode3 == NULL) {
    						newNode->next = newList;
    						newList = newNode;
    					} else {
    						previousNode3->next = newNode;
    						newNode->next = currentNode3;
    					}
    					countStop++;
    				// Greater than the last node that has an equal ifidf value
    				} else if (strcmp(newNode->filename, currentNode3->filename) > 0 
    				&& currentNode3 == lastEqual) {
    				    // Check if it will become the new tail
    					if (lastEqual == tail) {
    						tail->next = newNode;
    						tail = newNode;
    					} else {
    						newNode->next = currentNode3->next;
    						currentNode3->next = newNode;
    					}
    					countStop++;
    				// Go through and find the two nodes that it should be inbetween
    				} else if (previousNode3 != NULL) {
        			    if ((newNode->tfidf_sum == previousNode3->tfidf_sum && 
        			    strcmp(newNode->filename, previousNode3->filename) > 0) &&
        			    newNode->tfidf_sum == currentNode3->tfidf_sum && 
        			    strcmp(newNode->filename, currentNode3->filename) < 0 ) {
        		            previousNode3->next = newNode;
        				    newNode->next = currentNode3;
        				    countStop++;
        			    }
    				}
    				previousNode3 = currentNode3;
    				currentNode3 = currentNode3->next;
    			}
    			
    			
    		} else {
    			// Than the other cases 
    			// Greater than the first node
    			if (newNode->tfidf_sum > newList->tfidf_sum) {
    				newNode->next = newList;
    				newList = newNode;
    			// Less than the last node
    			} else if (newNode->tfidf_sum < tail->tfidf_sum) {
    				tail->next = newNode;
    				tail = newNode;
    			// In between two nodes
    			} else {
    				TfIdfList previousNode = newList;
    				TfIdfList currentNode2 = newList->next;
    				while (currentNode2 != NULL) {
    					if (newNode->tfidf_sum < previousNode->tfidf_sum && 
    					newNode->tfidf_sum > currentNode2->tfidf_sum) {
    						previousNode->next = newNode;
    						newNode->next = currentNode2;
    					}
    					previousNode = currentNode2;
    					currentNode2 = currentNode2->next;
    				}
    			}
    		}
    	}
    	currentNode = currentNode->next;
    }		
   	return newList;
    
}

// This doesn't work completely
TfIdfList retrieve(InvertedIndexBST tree, char* searchWords[] , int D) {
	int counter = 1;
	// Run the 4th function on the first word to get a linked list
	TfIdfList newList = calculateTfIdf(tree, searchWords[0], D);
	TfIdfList tail = NULL;
    TfIdfList check = newList;
	while (check != NULL) {
		tail = check;
		check = check->next;
	}
	newList = calculateTfIdf(tree, searchWords[0], D);
	// Run the 4th function on subsequent words (in a while loop)
	while (searchWords[counter] != NULL) {
		TfIdfList checkList = calculateTfIdf(tree, searchWords[counter], D);
		// For each node in the subsequent nodes, check the existing list for the same filename
		while (checkList != NULL) {
			int countSame = 0;
			TfIdfList insertNode = newTfIdfNode("placeholder", 1.0, 1.0);
			TfIdfList previousNode = NULL;
			TfIdfList traversingNode = newList;
			// Check whether there is an existing node with the same filename
			while (traversingNode != NULL && countSame == 0) {
				if (strcmp(traversingNode->filename, checkList->filename) == 0) {
					countSame++;
				}
				if (countSame == 0) {
					previousNode = traversingNode;
					traversingNode = traversingNode->next;
				}
			}
			// If there was an existing node with the same filename, take out that node and change its tfidf value
			if (countSame != 0 ) {
			    if (previousNode == NULL) {
			        newList = traversingNode->next;
			        traversingNode->next = NULL;
			        traversingNode->tfidf_sum = traversingNode->tfidf_sum + checkList->tfidf_sum;
				    insertNode = traversingNode;
			    } else if (traversingNode->next == NULL) {
			        previousNode->next = NULL;
			        tail = previousNode;
			        traversingNode->tfidf_sum = traversingNode->tfidf_sum + checkList->tfidf_sum;
				    insertNode = traversingNode;
			    } else {  
				    previousNode->next = traversingNode->next;
				    traversingNode->next = NULL;
				    traversingNode->tfidf_sum = traversingNode->tfidf_sum + checkList->tfidf_sum;
				    insertNode = traversingNode;
				}
				// Insert traversingNode back into it based on its new value
			// No existing node with the same filename, insert in correct place based on criteria
			} else {
				// Duplicate checkList
				insertNode->filename = checkList->filename;
				insertNode->tfidf_sum = checkList->tfidf_sum;
				insertNode->next = NULL;
			}
			// Insert in the appropriate place
			// Same as the code in function 4
			
		// Check if there is equality first
			int countEquality = 0;
			TfIdfList traversingNode2 = newList;
			while (traversingNode2 != NULL) {
				if (insertNode->tfidf_sum == traversingNode2->tfidf_sum) {
					countEquality++;
				}
				traversingNode2 = traversingNode2->next;
			}
			if (countEquality != 0) {
			// If 0, skip this
				TfIdfList previousNode3 = NULL;
				TfIdfList currentNode3 = newList;
				TfIdfList firstEqual = NULL;
				TfIdfList lastEqual = NULL;
				int countCheck = 0;
				// Go through the list and find the first one that is the same and let firstEqual be that
				while (currentNode3 != NULL && countCheck == 0) {
					if (insertNode->tfidf_sum == currentNode3->tfidf_sum) {
						firstEqual = currentNode3;
						countCheck++;
					}
					if (countCheck == 0) {
						previousNode3 = currentNode3;
						currentNode3 = currentNode3->next;
					}	
				}
				// Need to find last equal
				currentNode3 = firstEqual;
				while (currentNode3->tfidf_sum == insertNode->tfidf_sum && currentNode3 != NULL) {
					previousNode3 = currentNode3;
					currentNode3 = currentNode3->next;
				}
				lastEqual = previousNode3;
				// We have found the first node that is equal in tfidf value to the newNode
				// Name is smaller than first one of the group that is same
				previousNode3 = NULL;
				currentNode3 = newList;
				int countStop = 0;
				while (currentNode3 != NULL && countStop == 0) {
			    	// Smaller than the first node with the same ifidf value
					if (strcmp(insertNode->filename, currentNode3->filename) < 0 
					&& currentNode3 == firstEqual) {
				    	// Check if it will become the new head
						if (previousNode3 == NULL) {
							insertNode->next = newList;
							newList = insertNode;
						} else {
							previousNode3->next = insertNode;
							insertNode->next = currentNode3;
						}
						countStop++;
				// Greater than the last node that has an equal ifidf value
					} else if (strcmp(insertNode->filename, currentNode3->filename) > 0 
					&& currentNode3 == lastEqual) {
				    // Check if it will become the new tail
						if (lastEqual == tail) {
							tail->next = insertNode;
							tail = insertNode;
						} else {
							insertNode->next = currentNode3->next;
							currentNode3->next = insertNode;
						}
						countStop++;
				// Go through and find the two nodes that it should be inbetween
					} else if (previousNode3 != NULL) {
    			    	if ((insertNode->tfidf_sum == previousNode3->tfidf_sum && 
    			    	strcmp(insertNode->filename, previousNode3->filename) > 0) &&
    			    	insertNode->tfidf_sum == currentNode3->tfidf_sum && 
    			    	strcmp(insertNode->filename, currentNode3->filename) < 0 ) {
    		            	previousNode3->next = insertNode;
    				    	insertNode->next = currentNode3;
    				    	countStop++;
    			   	 	}
					}
					previousNode3 = currentNode3;
					currentNode3 = currentNode3->next;
				}
			
			
			} else {
			// Than the other cases 
			// Greater than the first node
				if (insertNode->tfidf_sum > newList->tfidf_sum) {
					insertNode->next = newList;
					newList = insertNode;
			// Less than the last node
				} else if (insertNode->tfidf_sum < tail->tfidf_sum) {
					tail->next = insertNode;
					tail = insertNode;
			// In between two nodes
				} else {
					TfIdfList previousNode = newList;
					TfIdfList currentNode2 = newList->next;
					while (currentNode2 != NULL) {
						if (insertNode->tfidf_sum < previousNode->tfidf_sum && 
						insertNode->tfidf_sum > currentNode2->tfidf_sum) {
							previousNode->next = insertNode;
							insertNode->next = currentNode2;
						}
						previousNode = currentNode2;
						currentNode2 = currentNode2->next;
					}
				}	
			}
			checkList = checkList->next;
		}
		counter++;
	}
	return newList;
}



// Function adapted from Wk3 Lab (BSTree.c)
// Create an empty BST
InvertedIndexBST newBST(void) {
	return NULL;
}

// Function adapted from Wk3 Lab (BSTree.c)
// Create an empty BST
TfIdfList newTfIdfList(void) {
    return NULL;
}

// Function adapted from Wk3 Lab (BSTree.c)
// Function to make new TfIdfNode
TfIdfList newTfIdfNode(char *fileName, double idf, double tf) {
    TfIdfList newNode = malloc (sizeof(*newNode));
    newNode->filename = fileName;
    newNode->tfidf_sum = idf*tf;
    newNode->next = NULL;
    return newNode;
}

// Function adapted from Wk3 Lab (BSTree.c)
// Function to search through the BST and find a word
InvertedIndexBST BSTreeSearch(InvertedIndexBST tree, char *searchWord)
{
	if (tree == NULL)
		return tree;
	else if (strcmp(searchWord, tree->word) < 0)
		return BSTreeSearch (tree->left, searchWord);
	else if (strcmp(searchWord, tree->word) > 0)
		return BSTreeSearch (tree->right, searchWord);
	else // (v == t->value)
		return tree;
}

// Function to scan the name of the individual text files in the collection.txt into a temp linked list
tempFile *scanFile(char *collectionFilename) {
	char tempFileName[MAX];
	tempFile *head = NULL;
	tempFile *tail = NULL;
	FILE *collection = fopen(collectionFilename, "r");

	while (fscanf(collection, "%s", tempFileName) != EOF) {
		tempFile *newNode = malloc(sizeof(*newNode));
		// Substitute for strdup
		newNode->filename = malloc(sizeof(tempFileName)+1);
		strcpy(newNode->filename, tempFileName);
		newNode->next = NULL;
		// If linked list is empty
		if (head == NULL) {
			head = newNode;
			tail = newNode;
		} else {
			tail->next = newNode;
			tail = newNode;
		}
	}
	fclose(collection);
	return head;
}

// Function that returns the total number of words within a single text file
int countNumberWords (char *str) {
	int counterWord = 0;
	char word[MAX] = {};
	FILE *file = fopen(str, "r");
	assert(file != NULL);
	// While fscanf returns a word/works, increment counterWord
	while (fscanf(file, "%s", word) == 1) {
		counterWord++;
	}
	fclose(file);
	return counterWord;
}

// Function adapt from Wk3 Lab (BSTree.c)
// Insert the node into the BST in alphabetical order (use strcmp)
InvertedIndexBST BSTInsert(InvertedIndexBST t, char *str, char *str2, int totalNumber) {
	// BST is empty
	if (t == NULL) {
		return newBSTNode(str, str2, totalNumber);
	} else if (strcmp(str, t->word) < 0) {
		t->left = BSTInsert(t->left, str, str2, totalNumber);
	} else if (strcmp(str, t->word) > 0) {
		t->right = BSTInsert(t->right,str, str2, totalNumber);
	} else {
		// This ensures that there are no duplicates
		// If the word is same and also from same file
		// Go through the word's linked list, and if it finds the same filename, add 1/totalNumber
		FileList currentNode = t->fileList;
		int counter = 0;
		while (currentNode != NULL) {
			// Find node that contains the same filename if there is one
			if (strcmp(currentNode->filename, str2) == 0) {
				currentNode->tf = currentNode->tf + 1.0/totalNumber;
				counter++;
			}
			currentNode = currentNode->next;
		// If the word is same but from a different file, create another node
		} 
		if (counter == 0) {
			currentNode = t->fileList;
			// Go to the last node
			while (currentNode->next != NULL) {
				currentNode = currentNode->next;
			}
			FileList newNode = newFileListNode(str2, totalNumber);
			// Must make sure that they are in order
			FileList tail = currentNode;
			FileList head = t->fileList;
			// Node should be inserted as the first one
			if (strcmp(newNode->filename, head->filename) < 0) {
			    newNode->next = head;
			    t->fileList = newNode;
			// Node should be inserted as the last one
			} else if (strcmp(newNode->filename, tail->filename) > 0) {
			    tail->next = newNode;
			    tail = newNode;
		    // In between two nodes
			} else {
			    FileList previousNode = t->fileList;
			    currentNode = t->fileList->next;
			    while (currentNode != NULL) {
			        if (strcmp(newNode->filename, previousNode->filename) > 0 &&
			        strcmp(newNode->filename, currentNode->filename) < 0) {
			            previousNode->next = newNode;
			            newNode->next = currentNode;
			        }
			        previousNode = currentNode;
			        currentNode = currentNode->next;
			    }
			}
		}
	}
	return t;
}

// Function adapted from Wk3 Lab (BSTree.c)
// Create a new node containing a word
static InvertedIndexBST newBSTNode(char *str, char *str2, int totalNumber) {
	InvertedIndexBST newNode = malloc(sizeof *newNode);
	assert (newNode != NULL);
	newNode->word = str;
	newNode->left = newNode->right = NULL;
	newNode->fileList = newFileListNode(str2, totalNumber);
	return newNode;
}

// Create a new FileList Node 
// Use to make a new InvertedIndexBST or when the word has already been found
static FileList newFileListNode(char *str, int totalNumber) {
	FileList newNode = malloc(sizeof *newNode);
	assert (newNode != NULL);
	newNode->filename = str;
	newNode->tf = 1.0/totalNumber;
	newNode->next = NULL;
	return newNode;
}

// Function adapted from Wk3 Lab (BSTree.c)
// Print out the words in alphabetical/infix order
void BSTreeInfix (InvertedIndexBST tree, FILE *fp) {
	if (tree == NULL)
		return;
	BSTreeInfix (tree->left, fp);
	fprintf(fp,"%s ", tree->word);
	FileList currentNode = tree->fileList;
	// Go through the linked list of each word's node to print all the files that contain the word
	while (currentNode != NULL) {
		fprintf(fp, "%s ", currentNode->filename);
		currentNode = currentNode->next;
	}
	fprintf(fp, "\n");
	BSTreeInfix(tree->right, fp);
}

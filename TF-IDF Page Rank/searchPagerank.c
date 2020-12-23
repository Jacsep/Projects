#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 1000

// Create a struct 
typedef struct URLNode {
    char *urlname;
    double pageRank;
    int numOfWords;
    struct URLNode *next;
}URLNode;

URLNode *newNode (void);
URLNode *pageRankNode (void);
URLNode *duplicateNode (char *urlname, double pageRank, int numOfWords);

int main(int argc, char* argv[]) {
    // Go through pagerankList and add the url name and corresponding pagerank
   URLNode *leadingNode = pageRankNode();

    // Go through invertedIndex.txt and find the matching words to those inserted.
   // Then go through and compare the urls and if matching, increment NumOfWords
   // Do this until all the words are done
    int counter = 1;
    char line[MAX];
    while (counter < argc) {
    	FILE *invertedIndex = fopen("invertedIndex.txt", "r");
    	while (fgets(line, MAX, invertedIndex) != NULL) {
    		char *word4 = strtok(line, " ");
    		if (strcmp(word4, argv[counter]) == 0) {
    		    word4 = strtok(NULL, " ");
    			while (word4 != NULL) {
    				URLNode *currentNode = leadingNode;
    				while (currentNode != NULL) { 
    					if (strcmp(currentNode->urlname, word4) == 0) {
    						currentNode->numOfWords++;
    					}
    					currentNode = currentNode->next;
    				}
    				word4 = strtok(NULL, " ");
    			}
    		}
    	}
    	fclose(invertedIndex);
    	counter++;
    }
    URLNode *biggie = leadingNode;
    
    URLNode *head = NULL;
    URLNode *tail = NULL;
    while (biggie != NULL) {
        if (biggie->numOfWords != 0) {
            URLNode *copyNode = duplicateNode(biggie->urlname, biggie->pageRank, biggie->numOfWords);
            // Insert node into appropriate place
            if (head == NULL) {
                head = copyNode;
                tail = copyNode;
            // Insert at the front
            } else if ((copyNode->numOfWords > head->numOfWords) || (copyNode->numOfWords == head->numOfWords && 
                copyNode->pageRank > head->pageRank)) {
                copyNode->next = head;
                head = copyNode;
            // Insert at the back
            } else if ((copyNode->numOfWords < tail->numOfWords) || (copyNode->numOfWords == tail->numOfWords && 
                copyNode->pageRank < tail->pageRank)) {
                tail->next = copyNode;
                tail = copyNode;
            } else {
                URLNode *currentNode = head->next;
                URLNode *previousNode = head;
                while (currentNode != NULL) {
                    // Not any of the same numOfWords
                    if (previousNode->numOfWords > copyNode->numOfWords && currentNode->numOfWords < copyNode->numOfWords) {
                        previousNode->next = copyNode;
                        copyNode->next = currentNode;
                        break;
                    // Insert inbetween nodes with the same numOfWords
                    } else if ((previousNode->numOfWords == copyNode->numOfWords && currentNode->numOfWords == 
                        copyNode->numOfWords) && (previousNode->pageRank > 
                    copyNode->pageRank && currentNode->pageRank < copyNode->pageRank)) {
                        previousNode->next = copyNode;
                        copyNode->next = currentNode;
                        break;
                        // Insert between a previousnode wtih the same amount of nodes and currentnode wtih less numOfWOrds
                    } else if ((previousNode->numOfWords == copyNode->numOfWords && copyNode->numOfWords > 
                        currentNode->numOfWords) && copyNode->pageRank < 
                    previousNode->pageRank) {
                        previousNode->next = copyNode;
                        copyNode->next = currentNode;
                        break;
                        // Insert between a previousNode wtih more numOfWords and currentNode wtih same
                    } else if ((previousNode->numOfWords > copyNode->numOfWords && copyNode->numOfWords == 
                        currentNode->numOfWords) && copyNode->pageRank > 
                    currentNode->pageRank) {
                        previousNode->next = copyNode;
                        copyNode->next = currentNode;
                        break;
                    } 
                    previousNode = currentNode;
                    currentNode = currentNode->next;
                }
            }
        }
        biggie = biggie->next;
    }
    // Increment number to make sure only the top 30 are printed to stdout
    int number = 0;
    while (head != NULL && counter < 30) {
        printf("%s\n", head->urlname);
        number++;
        head = head->next;
    }
   
   
    return 0;
}


URLNode *newNode (void) {
    URLNode *newNode = malloc (sizeof(*newNode));
    newNode->urlname = "NA";
    newNode->pageRank = 1.0;
    newNode->numOfWords = 0;
    newNode->next = NULL;
    return newNode;
}

// Read pagerankList and create a linked list with nodes containing the urlname and pageRank
URLNode *pageRankNode (void) {
    URLNode *head = NULL;
    URLNode *tail = NULL;
    FILE *pagerankList = fopen("pagerankList.txt", "r");
    char line[MAX];
    while (fgets(line, MAX, pagerankList) != NULL) {
        char *word;
        URLNode *currentNode = newNode();
        word = strtok(line, ",");
        int counter = 0;
        while (word != NULL) {
            double rank = atof(word);
            // If the word is the first one on the line, it is the urlname
            if (counter == 0) {
                currentNode->urlname = malloc(sizeof(word)+1);
                strcpy(currentNode->urlname, word);
            // If the word is the third one  on the line, it is the pageRank
            } else if (counter == 2) {
                currentNode->pageRank = rank;
            }
            counter++;
            word = strtok (NULL, ",");
        }
        if (head == NULL) {
            head = currentNode;
            tail = currentNode;
        } else {
            tail->next = currentNode;
            tail = currentNode;
        }
    }
    fclose(pagerankList);
    return head;
}

URLNode *duplicateNode (char *urlname, double pageRank, int numOfWords) {
    URLNode *node = malloc(sizeof(*node));
    node->urlname = urlname;
    node->pageRank = pageRank;
    node->numOfWords = numOfWords;
    node->next = NULL;
    return node;
}
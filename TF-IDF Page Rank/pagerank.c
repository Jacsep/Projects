#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "pagerank.h"
#include "graph.h"

#define MAX 1000

typedef struct StringToId {
	char *urlname;
	int numberID;
	double newPageRank;
	int outLinks;
	double previousPageRank;
	struct StringToId *next;
}StringToId;

// Scan in the command line arguments and then run PageRankW function using these values
int main(int argc, char* argv[]) {
    double d, diffRP;
    sscanf(argv[1], "%lf", &d);
    sscanf(argv[2], "%lf", &diffRP);
    int maxIt = atoi(argv[3]);
    PageRankW(d, diffRP, maxIt);
    return 0;
}


// Scan the urls from collection.txt
Graph getGraph (char *filename) {
	int totalURLs = 0;
	char URLs[MAX][MAX];
	int counter = 0;
	FILE *collection = fopen("collection.txt", "r");

	while (fscanf(collection, "%s", URLs[counter]) != EOF) {
		totalURLs++;
		counter++;
	}
	fclose(collection);

	Graph URLGraph = newGraph(totalURLs);
	counter = 0;
	char editedURL[MAX][MAX];
	while (counter < totalURLs) {
		strcpy(editedURL[counter], URLs[counter]);
		int counter2 = 0;
		while (editedURL[counter][counter2] != '\0') {
			counter2++;
		}
		editedURL[counter][counter2] = '.';
		editedURL[counter][counter2+1] = 't';
		editedURL[counter][counter2+2] = 'x';
		editedURL[counter][counter2+3] = 't';
		editedURL[counter][counter2+4] = '\0';
		counter++;
	}

	counter = 0;
	// Go into each url file and create edges between urls
	while (counter < totalURLs) {
		FILE *URLFile = fopen(editedURL[counter], "r");
		char line[MAX];
		if (strcmp(fgets(line, 17, URLFile), "#start Section-1") == 0) {
			char linkedURL[100];
			fscanf(URLFile, "%s", linkedURL);
			while (strcmp(linkedURL, "#end") != 0) {
				int counter3 = 0;
				while (counter3 < totalURLs) {
					if (strcmp(URLs[counter3], linkedURL) == 0 && counter != counter3) {
						insertEdge(URLGraph, counter, counter3);
					}
					counter3++;
				}
				fscanf(URLFile, "%s", linkedURL);
			}
		}
		fclose(URLFile);
		counter++;
	}
	return URLGraph;
}

// Creates a new URL node
// Used to copy a node
URLNode newNode(char *urlname, int numberID, double newPageRank, int outLinks, double previousPageRank) {
    URLNode newNode = malloc (sizeof(*newNode));
    newNode->urlname = urlname;
    newNode->numberID = numberID;
    newNode->newPageRank = newPageRank;
    newNode->outLinks = outLinks;
    newNode->previousPageRank = previousPageRank;
    newNode->next = NULL;
    return newNode;
}


void calculateOutLinks(URLNode head, Graph g) {
	URLNode traversingNode = head;
	while (traversingNode != NULL) {
		int counter = 0;
		int numOutLinks = 0;
		while (counter < numOfVertices(g)) {
			if (checkEdges(g, traversingNode->numberID, counter) == 1) {
				numOutLinks++;
			}
			counter++;
		}
		traversingNode->outLinks = numOutLinks;
		traversingNode = traversingNode->next;
	}
}

double calculateWIn (Graph dataGraph, Vertex src, Vertex dest) {
	double inSrc = 0;
	double inDest = 0;
	int counter = 0;

	while (counter < numOfVertices(dataGraph)) {
		if (checkEdges(dataGraph, counter, dest) == 1) {
			inDest++;
		}
		if (checkEdges(dataGraph, src, counter) == 1) {
			int counter2 = 0;
			int checker = 0;
			while (counter2 < numOfVertices(dataGraph)) {
				if (checkEdges(dataGraph, counter2, counter) == 1) {
					inSrc++;
					checker++;
				}
				counter2++;
			}
			// Prevent an error of division by 0 by setting it to 0.5
			if (checker == 0){
				inSrc = inSrc + 0.5;
			}
		}
		counter++;
	}
	if (inDest == 0) {
		inDest = 0.5;
	}
	double wIn = inDest/inSrc;
	return wIn;
}

double calculateWOut (Graph dataGraph, Vertex src, Vertex dest) {
	double outSrc = 0;
	double outDest = 0;
	int counter = 0;
	while (counter < numOfVertices(dataGraph)) {
		if (checkEdges(dataGraph, dest, counter) == 1) {
			outDest++;
		}
		if (checkEdges(dataGraph, src, counter) == 1) {
			int counter2 = 0;
			int checker = 0;
			while (counter2 < numOfVertices(dataGraph)) {
				if (checkEdges(dataGraph, counter, counter2) == 1) {
					outSrc++;
					checker++;
				}
				counter2++;
			}
			if (checker == 0) {
				outSrc = outSrc + 0.5;
			}
		}
		counter++;
	}
	if (outDest == 0) {
	    outDest = 0.5;
	}
	double wOut = outDest/outSrc;
	return wOut;
}

// Create a linked list containing all the urls information
URLNode collectionId(char *fileName) {
	char tempFileName[MAX];
	URLNode head = NULL;
	URLNode tail = NULL;
	int counter = 0;
	FILE *collection = fopen(fileName, "r");

	while (fscanf(collection, "%s", tempFileName) != EOF) {
		URLNode newNode = malloc(sizeof(*newNode));
		// Substitute for strdup
		newNode->urlname = malloc(sizeof(tempFileName)+1);
		strcpy(newNode->urlname, tempFileName);
		newNode->numberID = counter;
		newNode->newPageRank = 0;
		newNode->outLinks = 0;
		newNode->previousPageRank = 0;
		newNode->next = NULL;
		// If linked list is empty
		if (head == NULL) {
			head = newNode;
			tail = newNode;
		} else {
			tail->next = newNode;
			tail = newNode;
		}
		counter++;
	}
	fclose(collection);
	return head;
}

void PageRankW(double d, double diffPR, int maxIterations) {
	// Call upon the function to read all the URLs inside the collection.txt and create a linked list
	URLNode collectionFiles = collectionId("collection.txt");
	
	// Call upon the function to create a graph with Adjacency Matrix Representation
	Graph dataGraph = getGraph("collection.txt");

	// Calculate number of outlinks
	calculateOutLinks(collectionFiles, dataGraph);
	// Calculate using the Simplified Weighted PageRank Algorithm
	// Write a function to calculate Page Rank
	int N = numOfVertices(dataGraph);
	URLNode traversingNode = collectionFiles;
	while (traversingNode != NULL) {
		traversingNode->newPageRank = 1.0/N;
		traversingNode->previousPageRank = 1.0/N;
		traversingNode = traversingNode->next;
	}
	int iteration = 0;
	double diff = diffPR;

	while (iteration < maxIterations && diff >= diffPR) {
		traversingNode = collectionFiles;
		while (traversingNode != NULL) {
			double sigma = 0;
			int counter3 = 0;
			while (counter3 < numOfVertices(dataGraph)) {
				if (checkEdges(dataGraph, counter3, traversingNode->numberID) == 1) {
					URLNode currentNode = collectionFiles;
					while (currentNode != NULL) {
						if (currentNode->numberID == counter3) {
							sigma = sigma + (currentNode->previousPageRank * calculateWOut(dataGraph, 
							 currentNode->numberID, traversingNode->numberID) * calculateWIn(dataGraph, 
							 currentNode->numberID, traversingNode->numberID));
						}
						currentNode = currentNode->next;
					}
				}
				counter3++;
			}
			double newPR = (1-d)/N + d*sigma;
			traversingNode->newPageRank = newPR;
			traversingNode = traversingNode->next;
		}
		// Equate all the previous and new page rank for the next iteration after calculating diff
		URLNode currentNode = collectionFiles;
		diff = 0;
		while (currentNode != NULL) {
			diff = diff + fabs(currentNode->newPageRank - currentNode->previousPageRank);
			currentNode->previousPageRank = currentNode->newPageRank;
			currentNode = currentNode->next;
		}
		iteration++;
	}
	
	// Sort the nodes into the correct order
	URLNode head = NULL;
	URLNode tail = NULL;
	traversingNode = collectionFiles;
	while (traversingNode != NULL) {
	    // Create a duplicate of the node
		URLNode createdNode = newNode(traversingNode->urlname, traversingNode->numberID, traversingNode->newPageRank,traversingNode->outLinks, traversingNode->previousPageRank);
		// Insert based on the conditions
		if (head == NULL) {
			head = createdNode;
			tail = createdNode;
		} else if (createdNode->newPageRank > head->newPageRank) {	
			createdNode->next = head;
			head = createdNode;
		} else if (createdNode->newPageRank < tail->newPageRank) {
			tail->next = createdNode;
			tail = createdNode;
		} else {
			URLNode currentNode = head->next;
			URLNode previousNode = head;
			while (currentNode != NULL) {
				if (createdNode->newPageRank < previousNode->newPageRank && createdNode->newPageRank > currentNode->newPageRank) {
					previousNode->next = createdNode;
					createdNode->next = currentNode;
				}
				previousNode = currentNode;
				currentNode = currentNode->next;
			}
		}
		traversingNode = traversingNode->next;
	}
	// Output a list of URLs in descending order based on Weighted PageRank values (use format string "%.7f") to a file pagerankList.c 
	// along with the number of outgoing links
	FILE *output = fopen("pagerankList.txt", "w");
	URLNode traversingSortedNode = head;
	while (traversingSortedNode != NULL) {
		fprintf(output,"%s, %d, %.7f\n", traversingSortedNode->urlname, traversingSortedNode->outLinks, traversingSortedNode->newPageRank);
		traversingSortedNode = traversingSortedNode->next;
	}
	fclose(output);
	dropGraph(dataGraph);
}
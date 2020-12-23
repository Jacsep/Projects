
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX 1000

typedef struct UnionNode {
	char *urlname;
	int order;
	struct UnionNode *next;
}UnionNode;

void permute(int *a, int l, int r);
void swap (int *x, int *y);

int main (int argc, char* argv[]) {
	// Read all the text files and create a union linked list avoiding any duplicates
	int counter = 1;
	int numOfUrls = 0;
	UnionNode *head = NULL;
	UnionNode *tail = NULL;
	while (counter < argc) {
		FILE *text = fopen(argv[counter], "r");
		char tempUrlName[MAX];

		while (fscanf(text, "%s", tempUrlName) != EOF) {
			if (head == NULL) {
				UnionNode *newNode = malloc(sizeof(*newNode));
				newNode->urlname = malloc(sizeof(tempUrlName)+1);
				strcpy(newNode->urlname, tempUrlName);
				newNode->next = NULL;
				head = newNode;
				tail = newNode;
				numOfUrls++;
			} else {
				UnionNode *tempNode = head;
				int checker = 0;
				while (tempNode != NULL) {
					if (strcmp(tempNode->urlname, tempUrlName) == 0) {
						checker++;
						break;
					}
					tempNode = tempNode->next;
				}
				if (checker == 0) {
					UnionNode *newNode = malloc(sizeof(*newNode));
					newNode->urlname = malloc(sizeof(tempUrlName)+1);
					strcpy(newNode->urlname, tempUrlName);
					newNode->next = NULL;
					tail->next = newNode;
					tail = newNode;
					numOfUrls++;
				}
			}
		}
		fclose(text);
		counter++;
	}

	// Create an array of the numbers to be used for permutation.
	int urlOrder[numOfUrls];
	counter = 1;
	while (counter <= numOfUrls) {
		urlOrder[counter-1] = counter;
		counter++;
	}
	permute(urlOrder, 0, numOfUrls-1);

}

void swap (int *x, int *y) {
	int temp;
	temp = *x;
	*x = *y;
	*y = temp;
}

void permute(int *a, int l, int r) {
	int i; 
	if (l == r) {
		int counter = 0;
		while (counter <= r) {
		    printf("%d", a[counter]);
		    counter++;
		}
		printf("\n");

	} else {
		for (i = 0; i<=r; i++) {
			swap((a+l),(a+i));
			permute(a,l+1,r);
			swap((a+l),(a+i));
		}
	}
}

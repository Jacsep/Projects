#ifndef PAGERANK_H
#define PAGERANK_H

#include <stdio.h>
#include "graph.h"

typedef struct StringToId *URLNode;

Graph getGraph (char *);
URLNode newNode(char *, int , double , int , double );
void calculateOutLinks(URLNode , Graph );
double calculateWIn (Graph , Vertex , Vertex );
double calculateWOut (Graph , Vertex , Vertex );
URLNode collectionId(char *);
void PageRankW(double , double , int );

#endif
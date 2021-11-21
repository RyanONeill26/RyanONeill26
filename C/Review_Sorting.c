//This project reads in all IGN reviews fron the last 20 years from a file
//and sorts them in order of highest to lowest review score

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFFER 256
#define MAX_REVIEWS 20000

//struct to hold the information within pointers
typedef struct IGN{

  char name[MAX_BUFFER];
  char platform[MAX_BUFFER];
  int score;
  int release_year;
  
} Games;

int next_field( FILE *f, char *buf, int max )
{
	int i=0, end=0, quoted=0;
	
	for(;;) {
		// fetch the next character from file		
		buf[i] = fgetc(f);
		// if we encounter quotes then flip our state and immediately fetch next char
		if(buf[i]=='"') { quoted=!quoted; buf[i] = fgetc(f); }
		// end of field on comma if we're not inside quotes
		if(buf[i]==',' && !quoted) { break; }
		// end record on newline or end of file
		if(feof(f) || buf[i]=='\n') { end=1; break; } 
		// truncate fields that would overflow the buffer
		if( i<max-1 ) { ++i; } 
	}

	buf[i] = 0; // null terminate the string
	return end; // flag stating whether or not this is end of the line
}

// Stuff to make life a bit neater in main
void fetch_reviews (  FILE *csv, Games *p) 
{
	char buf[MAX_BUFFER];

	next_field( csv, p->name, MAX_BUFFER );  // name and platform are just strings so read
	next_field( csv, p->platform, MAX_BUFFER ); // those directly into the struct

	// Load all the reviews from the file using buffer as intermediary
	next_field( csv, buf, MAX_BUFFER );
	p->score = atoi(buf);          // atoi stands for ASCII to Integer

	next_field( csv, buf, MAX_BUFFER ); // It converts strings to numbers
	p->release_year = atoi(buf);                  // It is not a totally safe function to use.

}

void print_reviews( Games *p )
{

	printf("%40s%15s%4d%6d\n\n", p->name, p->platform, p->score, p->release_year );

}

//using inserton sort
void insertionSort_forScores(Games arr[], int size) 
{ 
  int i;
  int j;
  Games temp;

  for (i = 1; i<size; i++)
  {
    j = i;//starting point
    //swap in order starting from the highest and then down to the lowest
    while(j>=0 && arr[j-1].score < arr[j].score)//while the score of the previous element is less than the current element
    {
      //swap the jth and j-1th elements so that arr[j-1].score > arr[j].score
      temp = arr[j];
      arr[j] = arr[j-1];
      arr[j-1] = temp;
      j = j-1;
    }
  }
  
}

int main ( int argc, char *argv[] ) 
{
	FILE *f;
	Games Array[MAX_REVIEWS];		
	Games p;

	// Users must pass the name of the input file through the command line. 
  //If there is an error a message appears to the user the program stops.
	if( argc < 2 ) { 
		printf("Unable to open file.\n"); 
		return EXIT_FAILURE; 
	}

	//Open the input file. If there is a problem, report failure and quit
	f = fopen(argv[1], "r");
	if(!f) { 
		printf("unable to open %s\n", argv[1]); 
		return EXIT_FAILURE; 
	}
	
	fetch_reviews( f, &p ); // discard the header data in the first line

	//Now read the reviews until the end of the file
	int num_reviews = 0;
	while(!feof(f)) 
  {
		fetch_reviews( f, &Array[num_reviews]);
		num_reviews++;
	}
  //Sort the reviews from highest to lowest
  insertionSort_forScores(Array, num_reviews);

  int i;
  for (i = 0; i<10; i++)
  {
    print_reviews( &Array[i]);//Print IGN's top 10 games of the last 20 years
  }
  
	//Close the file
	fclose(f);
	return EXIT_SUCCESS;
}

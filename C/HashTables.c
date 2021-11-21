//This project stores information on multiple people using a 
//hash table. The information is read into the program from a file and 
//the user can input specific names they'd like to find information on.
//This program also keeps track of the number of enteries in the hash
//table as well as the number of collisions due to two entires having the
//same hash value

#include<stdio.h>
#include<stdlib.h>
#include <string.h> //for strcpy and strcmp
#include <ctype.h>  //for isalnum

#define MAX_STRING_SIZE 20 //max length of a string
#define ARRAY_SIZE 	99991  //best be prime
#define INFO_SIZE 10 //number of input entries

typedef struct Element{
  int 	Person_ID;
	char 	Deposition_ID[MAX_STRING_SIZE];
	char 	Surname[MAX_STRING_SIZE];
	char 	Forename[MAX_STRING_SIZE];
	int 	Age;
	char 	Person_Type[MAX_STRING_SIZE];
	char 	Gender[MAX_STRING_SIZE];
	char 	Nationality[MAX_STRING_SIZE];
	char 	Religion[MAX_STRING_SIZE];
	char 	Occupation[MAX_STRING_SIZE];
	struct Element *next;
}Element;

Element* hashTable[ARRAY_SIZE];//creates a table a elements
int collisions = 0;
int num_terms = 0;
int Full_hash = 0;
//implementing double hashing 
//first hash function
int hash_function(char* s)
{ 
  int hash = 0; 
  while(*s)
  { 
	  hash = (hash + *s) % ARRAY_SIZE; 
	  s++; 
	} 
	return hash; 
}
//second hash function
int hash2(char* s)
{ 
	int hash = 0; 
	while(*s)
  {
		hash = 1 + (hash + *s) % (ARRAY_SIZE-1); 
		s++; 
	} 
	return hash; 
}

//creates a new element to add into the hash table
Element* createNewElement(char* Person_ID, char* Deposition_ID, char* Surname, char* Forename, char* Age, char* Person_Type, char* Gender, char* Nationality, char* Religion, char* Occupation)
{
	Element *new_element =  (Element*) malloc(sizeof(Element));
  //converting the integaers into strings
	new_element->Person_ID 		= atoi(Person_ID );
	new_element->Age				= atoi(Age);
  //copying the strings over
	strcpy(new_element->Deposition_ID,Deposition_ID);
	strcpy(new_element->Surname		,Surname);
	strcpy(new_element->Forename		,Forename);
	strcpy(new_element->Person_Type	,Person_Type);
	strcpy(new_element->Gender		,Gender);
	strcpy(new_element->Nationality	,Nationality);
	strcpy(new_element->Religion		,Religion);
	strcpy(new_element->Occupation	,Occupation);

	new_element->next = NULL;//setting up the linked list for collisions
	return new_element;
}

//searches for a specific name in the hash table
Element* search (char* name)
{
	int index = hash_function(name);
  int double_hash = hash2(name);
	int original_index = index;

  while(hashTable[index] != NULL)
  { 
    //while we are on occupied cells
		if(!strcmp(hashTable[index]->Surname,name))
    {
			return hashTable[index];//desired name has been found
		}
        
    index = (index + double_hash) % ARRAY_SIZE;//moving through the table

    if(index == original_index) break;//searched the whole list
  
	}
  return NULL;
}

//inserting an element into the hashtable
void insert(char* Person_ID, char* Deposition_ID, char* Surname, char* Forename, char* Age, char* Person_Type, char* Gender, char* Nationality, char* Religion, char* Occupation)
{

	Element* newName = createNewElement( Person_ID,  Deposition_ID,  Surname,  Forename,  Age,  Person_Type,  Gender,  Nationality,  Religion,  Occupation);

	int index = hash_function(Surname);
  int double_hash = hash2(Surname);
	int original_index= index;

	while(hashTable[index] != NULL)//occupied cells
  {
		index = (index + double_hash) % ARRAY_SIZE;
		collisions++;
		if(index == original_index)
    {
			printf("Table is full.\n");//searched the whole table and found no empty space
			Full_hash = 1;//flip the boolean to true
			return;
		}

	}
  //add the new element to the table
	hashTable[index] = newName;
	num_terms++;
}

//adds a new element to the table either directly or by creating a linked
//list of same hash value elements if there is a collision 
void addOrLink(char* Person_ID, char* Deposition_ID, char* Surname, char* Forename, char* Age, char* Person_Type, char* Gender, char* Nationality, char* Religion, char* Occupation)
{
  //doing the linked list implementation of same hash value surnames here
	Element *temp = search(Surname);
	if(temp != NULL)//name found
  {
		collisions++;//link same surname
		while(temp->next != NULL)
    {
			temp = temp->next;//working down the linked list
			collisions++;
		}
		temp->next = createNewElement(Person_ID,Deposition_ID,Surname,Forename,Age,Person_Type,Gender,Nationality,Religion,Occupation);

	}
	else
  {
		if(Full_hash != 1)
    {
      //only insert if the list isnt filled
			insert(Person_ID,Deposition_ID,Surname,Forename,Age,Person_Type,Gender,Nationality,Religion,Occupation);
		}
	}
	
}


//prints everyone with the same surname in the order they were entered in the list
void printInfo(Element* head)
{
  if (head == NULL) return;
 
  //recursion, ensures the first person entered into the table with a specific surname is printed first
  printInfo(head->next);
  //numbers are there for formatting
	printf("%9i",head->Person_ID);
  printf("%14s",head->Deposition_ID);
  printf("%16s",head->Surname);
  printf("%16s",head->Forename);
  printf("%4i", head->Age);
  printf("%12s",head->Person_Type);
  printf("%8s", head->Gender);
  printf("%12s",head->Nationality);
  printf("%9s", head->Religion);
  printf("%11s\n",head->Occupation);
}

//prints out information to the terminal
void printOccurences(char* name)
{
	Element *Name = search(name);
	if(Name != NULL)
  {
    //headings
		printf(">>> Person ID Deposition ID         Surname        Forename Age Person Type  Gender Nationality Religion Occupation\n");
    //print desired information
		printInfo(Name);
	}
  else
  {
    printf(">>> %s not in table\n",name);
  }
	return;

}
//CSV parser
int
next_field( FILE *f, char *buf, int max ) {
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

//Reads the contents of a file and adds them to the hash table - returns 1 if file was successfully read and 0 if not.
int load_file ( char *fname ) {
	FILE *f;
	char buf[INFO_SIZE][MAX_STRING_SIZE];

	// boiler plate code to ensure we can open the file
	f = fopen(fname, "r");
	if (!f) 
  { 
		printf("Unable to open %s\n", fname);
		return 0; 
	}
	
	char c;
	while(c!='\n')
  {
		c = fgetc(f);//gets rid of the file heading
	}

	// read until the end of the file
	while ( !feof(f) ) 
  {
		for(int i = 0; i < INFO_SIZE;i++)
    {
			next_field(f,buf[i], MAX_STRING_SIZE);//each group of 10 buf entries will be the information the user desires. Age, Personal_ID, ect.
		}
		addOrLink(buf[0], buf[1],buf[2],buf[3],buf[4],buf[5],buf[6],buf[7],buf[8],buf[9]); 
	}

	// always remember to close your file stream
	fclose(f);

	return 1;
}

int main(int argc, char *argv[])
{
  //if the termial read no inputs, exit the program
	if( argc < 2 ) { 
	return EXIT_FAILURE; 
	}

	load_file(argv[1]);
	printf("File %s loaded\n", argv[1]);

	float load = (float)num_terms / ARRAY_SIZE;

	printf(" Capacity: %i\n Num Terms: %i\n Collisions: %i\n Load: %f\n", ARRAY_SIZE, num_terms,collisions,load);

	char buf[MAX_STRING_SIZE];
  //asking the user which name they'd like to retrieve information on
	printf("Enter term to get frequency or type \"quit\" to escape\n");
	
	for (;;)
  {
		fgets(buf, MAX_STRING_SIZE, stdin);//retieving the user input

    if ((strlen(buf) > 0) && (buf[strlen (buf) - 1] == '\n'))
    {
     buf[strlen (buf) - 1] = '\0';//terminates the entry if there is a newline
    }
		if(!strcmp(buf,"quit")) //if the user enters quit
    {
      printf(">>> "); 
      return 0;
    }
		printOccurences(buf);//print the output the user desires
	}
	
  return 0;
}

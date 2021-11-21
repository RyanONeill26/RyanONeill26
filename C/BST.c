//this file is a section of a larger project. The purpose of this file is to write functions that will
//be called in main in order to create a balanced binary search tree. The elements being entered into
//the tree are books, the keys for the binary search tree are the book IDs which are generated using a function

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>

typedef struct Tree_Node 
{
    int   doc_id;           // unique identifier for the document
    char *name;             // file name of the document    
    int   word_count;       // number of words in the document      
    struct Tree_Node *right, *left; // pointer to the next nodes in the tree

} Tree_Node;

Tree_Node *tree;

//keeps track of depth and current node when generating the ID
int bst_level; 
int bst_node; 

int num_inserts;	//number of inserts made into the bst
int num_nodes; 	//counts number of nodes travsersed
int num_searches;//number of searches initiated into the bst
int total_searches;//number of total search iterations per search
int no_item_found;//counter to check the amount of search failures

//initializes all the counters and returns 1 if sucessful 
int
bstdb_init () {

	bst_node = 0;
	bst_level = 0;
	num_inserts = 0;
	num_nodes = 0;
	num_searches = 0;
	total_searches = 0;
	no_item_found = 0;
	return 1;
}

// Generates new id based on where the last element was inserted. 
// follows the equation (1 + 2*node)/(2^depth)*a large midpoint number
// when node number is equal 2^depth the node gets set back to 0 and the depth is incremented
// the function dictates that the ID's in the right subtree will be numbers
// in the greater half of the root/node number (1/2 -> 1) and the IDs in the left
//subtree will be numbers in the lesser half of the root/node number (0 -> 1/2)
int generate_id()
{

	int ID = (1+2*bst_node)/(pow(2, bst_level))*UINT_MAX/4;

	bst_node++;
	if(bst_node == pow(2, bst_level)){
		bst_node = 0;
		bst_level++;
	}
	
	return ID;

}

//basic bst insert function which uses recursion
int insert(Tree_Node** root, char* name, int word_count, int ID){

    if((*root) == NULL)
    {
	  // count the number of inserts
	  num_inserts++;
	  //initialising tree node
      *root  = (Tree_Node*)malloc(sizeof(Tree_Node));
      (*root)->name = name;
	  (*root)->word_count = word_count;
	  (*root)->doc_id = ID;
      (*root)->right = NULL;
      (*root)->left = NULL;
      return ID;
    }

    else if(ID < (*root)->doc_id)
    {
      insert(&((*root)->left), name, word_count, ID);
    }

    else if(ID >= (*root)->doc_id)
    {
      insert(&((*root)->right), name, word_count, ID);
    }

    else {return -1;}//insertion error
    
}

//add an entry into the bst
int
bstdb_add ( char *name, int word_count ) 
{
	int ID = generate_id();
	ID = insert(&tree, name, word_count, ID);
	return ID;//will return the book ID if insertion was successful, will be -1 otherwise
}

//search for the word count of the book
int
bstdb_get_word_count ( int doc_id ) 
{
	Tree_Node *p = tree;
    
    // Count how many times this function was called so we can get the average number of nodes traversed for each query
    total_searches++;
    
    while (p != NULL) 
	{
        // count the number of traversals
        num_searches++;
        // If we found the node, return it. Otherwise keep searching.
        if (p->doc_id == doc_id) { break; }//found it
        else if (p->doc_id < doc_id && p->right != NULL) {p = p->right;}//right sub-tree
		else if (p->doc_id > doc_id && p->left != NULL) {p = p->left;}//left sub-tree
		else {no_item_found++; return -1;}//can't find the ID
    }
	return p->word_count;
	
}

//search for the name of the book
char*
bstdb_get_name ( int doc_id ) 
{
	Tree_Node *p = tree;
    
    // Count how many times this function was called so we can get the average number of nodes traversed for each query
    total_searches++;
    
    while (p != NULL) 
	{
        // count the number of traversals
        num_searches++;
        // If we found the node, return it. Otherwise keep searching.
        if (p->doc_id == doc_id) { break; }//found it
        else if (p->doc_id < doc_id && p->right != NULL) {p = p->right;}//right sub-tree
		else if (p->doc_id > doc_id && p->left != NULL) {p = p->left;}//left sub-tree
		else {no_item_found++; return NULL;}//can't find the ID
    }
	return p->name;
}

//returns the depth of a tree
int node_height(Tree_Node *root)
{
	if(root == NULL) return 0;//base case, an empty tree is a balanced tree
	//getting heights of left and right subtrees
	int left_height = node_height(root->left);
	int right_height = node_height(root->right);

	//find max(subtree_height) + 1 to get the height of the tree
	return fmax(left_height,right_height) + 1;
}

//returns 1 if bst is balanced, 0 if not
int isBalanced(Tree_Node* root)
{
	if(root == NULL) return 1;//base case, an empty tree is a balanced tree

	//getting heights of left and right subtrees
	int left_height = node_height(root->left);
	int right_height = node_height(root->right);

	if(abs(left_height - right_height) <= 1 && isBalanced(root->left) && isBalanced(root->right)) return 1;

	return 0;
}

//preorder traversal through the bst
void traverse(Tree_Node * root)
{
	num_nodes++;
	if(root->left != NULL) traverse(root->left);//traverse left sub-tree
	if(root->right != NULL) traverse(root->right);//traverse right sub-tree
}


//returns 1 if a duplicate is found and a 0 otherwise
int checking_duplicate(Tree_Node* root, int doc_id) 
{
    if(root == NULL) return 0;
    if (doc_id == root->doc_id) return 1;
    else
	{
        int left = checking_duplicate(root->left, doc_id);
        int right = checking_duplicate(root->right, doc_id);
        return left||right;
    }
}

//acts as a setup for the checking_duplicate function and returns 1 if a duplicate is found, 0 otherwise
int isDuplicate(Tree_Node* root) 
{
    if (root != NULL) 
	{   
        if(checking_duplicate(root->left, root->doc_id) == 1) return 1;  
        if(checking_duplicate(root->right, root->doc_id) == 1) return 1;

        return isDuplicate(root->left)||isDuplicate(root->right);   
    }
    else return 0;
}

//shows the stats of the bst
void
bstdb_stat () {

	printf("STATS\n\n");
	printf("Height of the tree:                 %i\n", node_height(tree));
	printf("Is the tree balanced?               %c\n",((isBalanced(tree) == 1))? 'Y' : 'N');
	printf("Is each entry in the tree unique?   %c\n\n",((isDuplicate(tree) == 0))? 'Y' : 'N');
	traverse(tree);
	printf("Total nodes:                        %i\n", num_nodes);
	printf("Total inserts:                      %i\n", num_inserts);
	printf("Do the number of nodes in the tree match the number of insertions?     %c\n\n",((num_nodes == num_inserts))? 'Y' : 'N');
	printf("Total searches performed:           %i\n", total_searches);
	int average_search = num_searches/total_searches;
	printf("Nodes traversed in all searches     %i\n",num_searches);
	printf("Average nodes traversed per search: %i\n", average_search);
	printf("Items not found:                    %i\n", no_item_found);

}

//function uses recursion to free the memory used in the bst
void free_bst(Tree_Node* root)
{
	if (root == NULL) return;
 
    free_bst(root->left);
    free_bst(root->right);
     

    free(root);
}

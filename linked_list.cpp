//this project uses a linked list in order to link all the words in
//a book together and count the number of times each unique word in 
//the book appears
#include <iostream>
#include <string>
#include "word.hpp"

using namespace std;
//forward decarations
bool check(word* w, word* s);
void invert(word* w);
void clean_up(word* w);

int main() 
{
  word* book = nullptr;//start with an empty book

//these words from the book are read in from a file
  while(cin.eof() == false)
  {
    string t_word;
    cin >> t_word;
    word *new_word = new word();//allocating memory 
    new_word->assign(t_word);
    //if inputted word is already in the list
    //then increment its count and move on to the next 
    //iteration of the loop, otherwise add the new word to the list
    if(check(book, new_word))
    {
      continue;
    }
    new_word->next = book;
    book = new_word;
    book->count++;
  }

  invert(book);//printing 
  clean_up(book);//deleting

}
//checks if a certain word appears in the list more than once
//if it does, increment the word's count
bool check(word* w, word* s)
{
  if(w != nullptr)
  {
    if(*w == *s)
    {
      w->count++;
      return true;
    } 
    else if(w->next)
    {
      return check(w->next, s);
    }
  }
  return false;
}
//invert the linked list so it can be printed in order
void invert(word* w)
{
  word* prev = nullptr;
  word* curr = w;
  word* next = nullptr;
 
  while (curr != nullptr)
  {
    next = curr ->next;
    curr->next = prev;
    prev = curr;
    curr = next;
  }    
  w = prev;

  while (w != nullptr)
  {
    cout <<"\""<< *w << "\" " << w->count <<endl;
    w = w->next;
  }
}
//deleting the memory allocated to the linked list
void clean_up(word* w)
{
  while (w != nullptr)
  {
    delete w;
    w=w->next;
  }
}

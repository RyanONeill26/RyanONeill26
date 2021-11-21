#pragma once
#include <string>

class word : public std::string 
{
  public:
  word *next; // use this to link the next object in the linked list
  int count; // use this to store count
};

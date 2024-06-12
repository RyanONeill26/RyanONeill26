This project was created in order to analyse how Search and MDP algorithms compare when attempting to find the shortest 
path through a maze. 

NB: This project was created using Python version 3.11.0, please download this version of Python to run this project
    as it will not work when using an Python version older than 3.10, and may not work if 3.11 is not used. 


The mazes generated in this project where created using the pyamaze Python package.
        Command to Install: pip install pyamaze
        
A note from the pyamaze creator (taken from: https://github.com/MAN1986/pyamaze/blob/main/pyamaze/pyamaze.py):
"
    License
    https://www.youtube.com/c/LearningOrbis
    Copyright (c) 2021 Muhammad Ahsan Naeem
    mahsan.naeem@gmail.com


    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"


maze_generator.py: Includes code that generates 10x10, 25x25, and 50x50 mazes and saves them locally to the project.
        Command to run: 'python maze_generator.py' OR 'py maze_generator.py'

search.py: Includes functions that run the BFS, DFS, and A-Star algorithms. 
        Command to run: 'python search.py' OR 'py search.py'

MDP.py: Includes functions that run the MDP Policy, and Value iteration algorithms.
        Command to run: 'python MDP.py' OR 'py MDP.py'

main.py: Imports functions from search.py and MDP.py and allows the user to generate a maze (or use a pre-existing maze) 
         and select an algorithm to navigate through the maze.
         Command to run: 'python main.py' OR 'py main.py'
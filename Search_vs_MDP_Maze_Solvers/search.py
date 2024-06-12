from collections import deque
from queue import PriorityQueue

# Algorithm that searches through the maze by checking every possible next step through every path at once
def BFS(maze, start=None):

    # If a start point is not specified, pick one
    if start is None:
        start = (maze.rows,maze.cols)

    # Initialize values
    # A FIFO queue that paths that are currently being checked will be entered into
    list_of_paths = deque()
    list_of_paths.append(start)

    BFSpath = {}
    # Set the starter cell to be explored
    explored = [start]
    bSearch=[]

    while len(list_of_paths)>0:

        currCell = list_of_paths.popleft()
        
        # If we're already at the goal then we don't need to do any searching
        if currCell == maze._goal:
            break
        
        # Check if it is possible to move in any new direction 
        for direction in 'NEWS':
            # Only searching valid next steps in the maze
            if maze.maze_map[currCell][direction] == True:
                match(direction):
                    case 'N':
                        childCell = (currCell[0]-1,currCell[1])
                    case 'E':
                        childCell = (currCell[0],currCell[1]+1)
                    case 'W':
                        childCell = (currCell[0],currCell[1]-1)
                    case 'S':
                        childCell = (currCell[0]+1,currCell[1])
                    
                # If we've already investigated a cell, skip it
                if childCell in explored:
                    continue

                # Update values
                list_of_paths.append(childCell)
                explored.append(childCell)
                BFSpath[childCell] = currCell
                bSearch.append(childCell)
    
    fwdPath = {}
    cell=maze._goal

    # Reverse the trip through the maze to get the BFS path 
    while cell != (maze.rows,maze.cols):
        fwdPath[BFSpath[cell]]=cell
        cell=BFSpath[cell]

    return bSearch,BFSpath,fwdPath


# Algorithm that searches through the maze by checking every possible path in its entirety through the maze
def DFS(maze, start=None):
    
    # If a start point is not specified, pick one
    if start is None:
        start = (maze.rows,maze.cols)
    
    # Initialize values
    # Uses a stack to store the list of possible paths through the maze
    list_of_paths = [start]
    explored = [start]
    
    dfsPath = {}
    dSeacrh = []

    while len(list_of_paths)>0:
        
        # Pop the most recent path out of the stack
        currCell = list_of_paths.pop()
        dSeacrh.append(currCell)

        # If we're already at the goal then we don't need to do any searching
        if currCell == maze._goal:
            break

        possible_paths = 0
        
        # Check if it is possible to move in any new direction 
        for direction in 'NEWS':
            # Only searching valid next steps in the maze
            if maze.maze_map[currCell][direction] == True:
                match(direction):
                    case 'N':
                        childCell = (currCell[0]-1,currCell[1])
                    case 'E':
                        childCell = (currCell[0],currCell[1]+1)
                    case 'W':
                        childCell = (currCell[0],currCell[1]-1)
                    case 'S':
                        childCell = (currCell[0]+1,currCell[1])
                
                # If we've already investigated a cell, skip it
                if childCell in explored:
                    continue
                
                # Update values
                possible_paths += 1
                explored.append(childCell)
                list_of_paths.append(childCell)
                dfsPath[childCell] = currCell
        # If there is more than one possible path to explore, mark it for later
        if possible_paths>1:
            maze.markCells.append(currCell)

    fwdPath = {}
    cell = maze._goal

    # Reverse the trip through the maze to show the DFS path
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    
    return dSeacrh,dfsPath,fwdPath


# Used to measure the Manhattan distance between the current cell and the goal
def hueristic(cell1,cell2):

    x1,y1 = cell1
    x2,y2 = cell2

    return abs(x1-x2) + abs(y1-y2)



def Astar(maze, start=None):
    
    # If a start point is not specified, pick one
    if start is None:
        start = (maze.rows,maze.cols)
    
    # Initialize values
    # Initializing the g score for the start cell as 0, and infinity for all other cells
    g_score = {cell:float('inf') for cell in maze.grid}
    g_score[start] = 0
    # Initializing the f score for the start cell as the heuristic of the start cell and the goal, and infinity for all other cells
    f_score = {cell:float('inf') for cell in maze.grid}
    f_score[start] = hueristic(start,(1,1))
    # Create a priority queue where the priority is the cell with the cheapest cost
    open = PriorityQueue()
    # Enter values into the priority queue as a tuple
    open.put((hueristic(start,(1,1)),hueristic(start,(1,1)),start))
    aPath = {}


    while not open.empty():

        currCell=open.get()[2]
        
        # If we're already at the exit then we don't need to do any searching
        if currCell == (1,1):
            break
        
        # Check if it is possible to move in any new direction 
        for direction in 'NEWS':
            # Only searching valid next steps in the maze
            if maze.maze_map[currCell][direction] == True:
                match(direction):
                    case 'N':
                        childCell = (currCell[0]-1,currCell[1])
                    case 'E':
                        childCell = (currCell[0],currCell[1]+1)
                    case 'W':
                        childCell = (currCell[0],currCell[1]-1)
                    case 'S':
                        childCell = (currCell[0]+1,currCell[1])
                
                # Calculate the cost of moving to the next cell                 
                temp_g_score = g_score[currCell]+1
                temp_f_score = temp_g_score+hueristic(childCell,(1,1))

                # If the updated cost is better (less) than the current cost, update the values
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score,hueristic(childCell,(1,1)),childCell))
                    aPath[childCell] = currCell
    fwdPath={}
    cell=(1,1)

    # Reversing the trip through the maze to get the Astar path
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    
    return fwdPath
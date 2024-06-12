from pyamaze import maze, agent, COLOR
from search import BFS, DFS, Astar
from MDP import value_iteration, policy_iteration
from timeit import timeit
import tracemalloc
import copy 

# Percentage of loops that will be present in the newly generated mazes
LOOP_PERCENTAGE = 15

# Initialize maze
mz = {}
maze_chosen = False
# Choose a pre-made or new maze to generate
while maze_chosen == False:
    
    maze_type = input("If you would like to select a premade maze, enter 'premade'; if you would like to create a new maze, enter 'new': ")

    match maze_type:
        case 'new':
            rows = int(input("Please enter the number of rows for the maze: "))
            columns = int(input("Please enter the number of columns for the maze: "))
            # Create the maze
            mz = maze(rows, columns)
            mz.CreateMaze(loopPercent=LOOP_PERCENTAGE, theme='light')
            maze_chosen = True
        case 'premade':
            size = input("Select the size of the premade maze you would like to test: 10x10, 25x25, 50x50\n")
            file_name = 'saved_mazes\\maze_' + size + '.csv'
            # Load the maze
            mz = maze()
            mz.CreateMaze(loadMaze=file_name)
            maze_chosen = True
        case default:
            print("INVALID INPUT")


# Choose an algorithm to Navigate the maze
algorithm_chosen = False

while algorithm_chosen == False:
    
    algorithm = input("Please Choose one of the following algorithms to navigate maze: BFS, DFS, Astar, MDP Value Iteration, MDP Policy Iteration: ")
    
    match algorithm:
        case 'BFS':
            # Begin monitoring the memory useage of the program
            tracemalloc.start()

            # Run BFS
            bSearch,bfsPath,fwdPath = BFS(mz)
            # Create a copy of the path to report stats later
            final_path = copy.deepcopy(fwdPath)
            final_path_length = len(final_path) + 1

            # Record the amount of memory used
            algorithm_mem_usage = tracemalloc.get_traced_memory()
            # Stop monitoring 
            tracemalloc.stop()

            # Trace the path 
            a = agent(mz, footprints=True, color=COLOR.yellow, shape='square')
            b = agent(mz, 1,1, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(mz.rows,mz.cols))
            c = agent(mz, footprints=True, color=COLOR.red, shape='square')
            mz.tracePath({a:bSearch}, delay=100)
            mz.tracePath({b:bfsPath}, delay=100)
            mz.tracePath({c:fwdPath}, delay=100)

            # Run the algorithm on the maze
            mz.run()

            # Grab how long the algorithm takes to run
            algorithm_time = timeit(stmt='BFS(mz)', number=1000, globals=globals())

            algorithm_chosen = True
        case 'DFS':
            # Begin monitoring the memory useage of the program
            tracemalloc.start()

            # Run DFS
            dSearch,dfsPath,fwdPath = DFS(mz) # (5,1) is Start Cell, Change that to any other valid cell
            # Create a copy of the path to report stats later
            final_path = copy.deepcopy(fwdPath)
            final_path_length = len(final_path) + 1
            
            # Record the amount of memory used
            algorithm_mem_usage = tracemalloc.get_traced_memory()
            # Stop monitoring 
            tracemalloc.stop()

            # Trace the path
            a = agent(mz, footprints=True, color=COLOR.yellow, shape='square')
            b = agent(mz, 1,1, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(mz.rows,mz.cols))
            c = agent(mz, footprints=True, color=COLOR.red, shape='square')
            mz.tracePath({a:dSearch}, showMarked=True, delay=100)
            mz.tracePath({b:dfsPath}, delay=100)
            mz.tracePath({c:fwdPath}, delay=100)

            # Run the algorithm on the maze
            mz.run()

            # Grab how long the algorithm takes to run
            algorithm_time = timeit(stmt='DFS(mz)', number=1000, globals=globals())

            algorithm_chosen = True
        case 'Astar':
            # Begin monitoring the memory useage of the program
            tracemalloc.start()

            # Run A-Star
            path = Astar(mz)
            # Create a copy of the path to report stats later
            final_path = copy.deepcopy(path)
            final_path_length = len(final_path) + 1

            # Record the amount of memory used
            algorithm_mem_usage = tracemalloc.get_traced_memory()
            # Stop monitoring 
            tracemalloc.stop()

            # Trace the path
            a = agent(mz, footprints=True, shape='square', color=COLOR.red)
            mz.tracePath({a:path}, delay=100)

            # Run the algorithm on the maze
            mz.run()

            # Grab how long the algorithm takes to run
            algorithm_time = timeit(stmt='Astar(mz)', number=1000, globals=globals())

            algorithm_chosen = True
        case 'MDP Value Iteration':
            # Begin monitoring the memory useage of the program
            tracemalloc.start()

            # MDP Value Iteration
            path = value_iteration(mz)
            # Create a copy of the path to report stats later
            final_path = copy.deepcopy(path)
            final_path_length = len(final_path)

            # Record the amount of memory used
            algorithm_mem_usage = tracemalloc.get_traced_memory()
            # Stop monitoring 
            tracemalloc.stop()

            # Trace the path
            a = agent(mz, footprints=True, shape='square', color=COLOR.red)
            mz.tracePath({a: path}, delay=100)

            # Run the algorithm on the maze
            mz.run()

            # Grab how long the algorithm takes to run
            algorithm_time = timeit(stmt='value_iteration(mz)', number=1000, globals=globals())

            algorithm_chosen = True
        case 'MDP Policy Iteration':
            # Begin monitoring the memory useage of the program
            tracemalloc.start()

            # MDP Policy Iteration
            path = policy_iteration(mz)
            # Create a copy of the path to report stats later
            final_path = copy.deepcopy(path)
            final_path_length = len(final_path)

            # Record the amount of memory used
            algorithm_mem_usage = tracemalloc.get_traced_memory()
            # Stop monitoring 
            tracemalloc.stop()

            # Trace the path
            a = agent(mz, footprints=True, shape='square', color=COLOR.red)
            mz.tracePath({a: path}, delay=100)
            # Run the algorithm on the maze
            mz.run()

            # Grab how long the algorithm takes to run
            algorithm_time = timeit(stmt='policy_iteration(mz)', number=1000, globals=globals())

            algorithm_chosen = True
        case default:
            print("INVALID INPUT")

# Report the stats of the algoritm execution
print(f'{algorithm} Estimated Time: {algorithm_time} seconds')
print(f'{algorithm} Estimated Minimum Memory Requirement: {algorithm_mem_usage[1] - algorithm_mem_usage[0]} bytes')
print(f'{algorithm} Correctness Estimate via Measuring the Path Length: {final_path_length} steps')

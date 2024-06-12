from pyamaze import maze, agent, textLabel, COLOR

# Percentage of loops that will be present in the newly generated mazes
LOOP_PERCENTAGE = 15

# Create the small maze
small_mz = maze(10,10)
small_mz.CreateMaze(loopPercent=LOOP_PERCENTAGE, theme='light', saveMaze=True)
# Create the medium maze
medium_mz = maze(25,25)
medium_mz.CreateMaze(loopPercent=LOOP_PERCENTAGE, theme='light', saveMaze=True)
# Create the large maze
large_mz = maze(50,50)
large_mz.CreateMaze(loopPercent=LOOP_PERCENTAGE, theme='light', saveMaze=True)
# The code to generate this game was modifed from: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py

import numpy as np
import random
import pygame
import sys
import math
from collections import defaultdict
import time
import tracemalloc

# Initialize colours used to create the board
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
# Initialize the row and column count
ROW_COUNT = 6
COLUMN_COUNT = 7
# Initialize player a opponent, as well as their piece values
PLAYER = 0
OPP = 1

EMPTY = 0
PLAYER_PIECE = 1
OPP_PIECE = 2

WINDOW_LENGTH = 4

# Function to initialize the game board
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

# Funcction to drop a piece to a location of the board
def drop_piece(board, row, col, piece):
	board[row][col] = piece

# Function used by Minimax to evaluate the state of the board
def evaluate(board, player_piece):
	if is_terminal_node(board):
		if winning_move(board, OPP_PIECE):
			return (None, 100000000000000)
		elif winning_move(board, PLAYER_PIECE):
			return (None, -10000000000000)
		else: # Game is over, no more valid moves
			return (None, 0)
	else: # Depth is zero
		return (None, score_position(board, player_piece))

# Checking if a location on the board is available
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

# Getting all of the available locations on the board
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

# Finding the next available row for the selected column
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

# Display the board
def print_board(board):
	print(np.flip(board, 0))

# Check if the player has won the game with its last move
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

# Helper function for the scoring function used by the Minimax function
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = OPP_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

# Scoring function used to evaluate the state of the board
def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

# Check if the game is over
def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, OPP_PIECE) or len(get_valid_locations(board)) == 0


# Epsilon greedy function for the Q-Learning algorithm
def epsilon_greedy(Q, epsilon, action_space, state):
	action_prob = np.random.random()
	# With probability (1-epsilon), take a random action to explore
	if action_prob < epsilon:
		action = np.random.choice(action_space)
	# With probability (epsilon), take the optimal action to exploit
	else:
		action = np.argmax(Q[state])

	return action

# RL Tabular Q-Learning function
def q_learning(board, num_episodes=10000, gamma=0.9, alpha=0.9, epsilon=0.8):
	# Action space size for Connect 4 is the number of columns - Initialize to 0s
	Q = defaultdict(lambda: np.zeros(COLUMN_COUNT))  
	action_space = list(range(COLUMN_COUNT))  
    
    
    # Begin Iterating through the episodes (simulated online learning)
	for i_episode in range(num_episodes):
		# Copy the current state of the board
		curr_board = np.copy(board)
		done = False
        
		while not done:
			# Convert the board to a tuple
			state = tuple(curr_board.flatten())  
            
            # Select action based on the probabilities for the epsilon greedy algorithm
			action = epsilon_greedy(Q, epsilon, action_space, state)
            #print(f'THAT: {action}')
			col = action
            
			# Check if the selected location is empty
			if is_valid_location(curr_board, col):  # Check if the selected columnn has a free spot
                # Update the board with the player's move
				row = get_next_open_row(curr_board, col)
				drop_piece(curr_board, row, col, 1)
                
				# Check if the game is over
				if is_terminal_node(curr_board):
					done = True
					# Reward for winning or drawing
					if winning_move(curr_board, 1) or (not winning_move(curr_board, -1) and not winning_move(curr_board, 1)):
						reward = 100
				else:
					# Opponent's move (randomly select an empty cell)
					free_col_list = get_valid_locations(curr_board)
					opp_col = random.choice(free_col_list)
					# Update the board with the player's move
					opp_row = get_next_open_row(curr_board, opp_col)
					drop_piece(curr_board, opp_row, opp_col, -1)
                        
                    # Check if the game is over after the opponent's move
					if is_terminal_node(curr_board):
						done = True
                    	# Reward for drawing
						if (not winning_move(curr_board, -1) and not winning_move(curr_board, 1)): 
							reward = 100
						# Negative reward for loosing
						else: 
							reward = -100 
					# No reward if the game is still ongoing
					else:
						reward = 0  
            # Otherwise, the algorithm picked an illegal (not free) location and will be punished
			else:
				reward = -10 
				done = True
                
			# Convert the next board state to a tuple
			next_state = tuple(curr_board.flatten()) 
            
            # Q-learning update
			# Grab the best action by using the maximum Q value of the next state of the board
			best_next_action = np.argmax(Q[next_state])
			# Use the Bellman Equation to calculate the Temporal Difference target
			td_target = reward + gamma*Q[next_state][best_next_action]
			# Subtract the Temporal Difference from the former Q-Value estimation
			td_error = td_target - Q[state][action]
			# Estimate the new Q-Value
			Q[state][action] += alpha * td_error
    
	return Q


# Minimax function (without pruning)
def minimax(board, depth, isMaximizingPlayer, player_piece):

	# Initialize the best values
	best_column = random.choice(get_valid_locations(board))
	if isMaximizingPlayer:
		best_value = -math.inf
	else:
		best_value = math.inf
	
	# If the game is over, return a static evaluation of the position
	if depth == 0 or is_terminal_node(board):
		score = evaluate(board, player_piece)
		return score
	
	# Use recursion to find the best scores
	for col in get_valid_locations(board):
		row = get_next_open_row(board, col)
		b_copy = board.copy()
		drop_piece(b_copy, row, col, player_piece)
		# Find the value of the next step's piece
		if player_piece == PLAYER_PIECE:
			next_piece = OPP_PIECE
		else:
			next_piece = PLAYER_PIECE
		# Get the score for the next step
		new_score = minimax(b_copy, depth-1, isMaximizingPlayer=(not isMaximizingPlayer), player_piece=next_piece)[1]

		# Player is looking to maximize the next move
		if isMaximizingPlayer:
			# Record the best score
			if new_score > best_value:
				best_value = new_score
				best_column = col
		
		# Player is looking to minimize the output
		else:
			# Record the best score
			if new_score < best_value:
				best_value = new_score
				best_column = col

	return best_column, best_value


# Minimax function (with pruning)
def minimax_pruning(board, depth, alpha, beta, isMaximizingPlayer, player_piece):
	# Initialize the best values
	best_column = random.choice(get_valid_locations(board))
	if isMaximizingPlayer:
		best_value = -math.inf
	else:
		best_value = math.inf
	
	# If the game is over, return a static evaluation of the position
	if depth == 0 or is_terminal_node(board):
		score = evaluate(board, player_piece)
		return score
	
	# Use recursion to find the best scores
	for col in get_valid_locations(board):
		row = get_next_open_row(board, col)
		b_copy = board.copy()
		drop_piece(b_copy, row, col, player_piece)
		# Find the value of the next step's piece
		if player_piece == PLAYER_PIECE:
			next_piece = OPP_PIECE
		else:
			next_piece = PLAYER_PIECE
		# Get the score for the next step
		new_score = minimax_pruning(b_copy, depth-1, alpha=alpha, beta=beta, isMaximizingPlayer=(not isMaximizingPlayer), player_piece=next_piece)[1]

		# Player is looking to maximize the next move
		if isMaximizingPlayer:
			# Record the best score
			if new_score > best_value:
				best_value = new_score
				best_column = col
			# Prune alpha
			alpha = max(alpha, new_score)
		
		# Player is looking to minimize the output
		else:
			# Record the best score
			if new_score < best_value:
				best_value = new_score
				best_column = col
			# Prune beta
			beta = min(beta, new_score)

		if beta <= alpha:
			break
			
	return best_column, best_value


# Function to create a default player who makes random moves unless it can make a winning move or block the opponent's winning move
def default_player(board, player_piece, opp_piece):
    # Check for winning move for player
	for col in get_valid_locations(board):
		row = get_next_open_row(board, col)
		board[row][col] = player_piece
		if winning_move(board, player_piece):
			board[row][col] = 0
			return col
		board[row][col] = 0

    # Check for blocking opponent's winning move
	for col in get_valid_locations(board):
		row = get_next_open_row(board, col)
		board[row][col] = opp_piece
		if winning_move(board, opp_piece):
			board[row][col] = 0
			return col
		board[row][col] = 0

    # If no winning or blocking move, choose random free column
	return random.choice(get_valid_locations(board))


# Create the board in a pygame window
def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == OPP_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


# Get the algorithm the Player would like to use and play against
selected_algo = False
while not selected_algo:
	# Player algorithm
	player_algo = int(input("Please choose one of the following algorithms you would like to use by entering a number between 1-4:\n1. Minimax(without pruning)\n2. Minimax(with pruning)\n3. Tabular Q-Learning\n4. Default\n"))
	# Opponent algorithm
	opp_algo = int(input("Please choose one of the following algorithms you would like play against by entering a number between 1-4:\n1. Minimax(without pruning)\n2. Minimax(with pruning)\n3. Tabular Q-Learning\n4. Default\n"))
	# Check if the input entered was valid
	if (player_algo in range(1,5)) and (opp_algo in range(1,5)):
		selected_algo = True
	else:
		print("ERROR: Enter please select a number between 1-4 that represents the algorithms you would like to use.\n")

# Get number of Games the Player would like to play
TOTAL_GAMES = int(input("How many games would you like to play?: "))

# Create the game
board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
# Initialize epsilon
ep = 0.9
# Initialize turn order
turn = random.choice([PLAYER, OPP])

# Check to see which player goes first in order to see which player is the naximizing player for the minimax algorithm
if turn == PLAYER:
	player_max = True
else:
	player_max = False

# Initialize counters to keep track of game stats
num_games = 0
player_wins = 0
opp_wins = 0
draws = 0
# Initialize lists to keep track of algorithm performance for the player
player_time_per_turn = []
player_time_per_turn_per_game = []
player_memory_per_turn = []
player_memory_per_turn_per_game = []
# Initialize lists to keep track of algorithm performance for the opponent
opp_time_per_turn = []
opp_time_per_turn_per_game = []
opp_memory_per_turn = []
opp_memory_per_turn_per_game = []

# Start the game
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	if turn == PLAYER and not game_over:
		# Select the chosen player algorithm
		match player_algo:
			# Minimax (without pruning)
			case 1:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				player_col = minimax(board, 5, player_max, PLAYER_PIECE)[0]
				# Record the maximum amount of memory used
				player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				player_time_per_turn.append(post_algo_time - pre_algo_time)
			# Minimax (with pruning)
			case 2:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				player_col = minimax_pruning(board, 5, -math.inf, math.inf, player_max, PLAYER_PIECE)[0]
				# Record the maximum amount of memory used
				player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				player_time_per_turn.append(post_algo_time - pre_algo_time)
			# Tabular Q-Learning
			case 3:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				Q = q_learning(board, epsilon=ep)
				# Record the maximum amount of memory used
				player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				player_time_per_turn.append(post_algo_time - pre_algo_time)
				# Retrive the players move
				player_col = np.argmax(Q[tuple(board.flatten())])
				# Lower the value of epsilon for the next iteration to encourage exploitation over exploration
				ep -= 0.02
			# Default player
			case 4:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				player_col = default_player(board, PLAYER_PIECE, OPP_PIECE)
				# Record the maximum amount of memory used
				player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				player_time_per_turn.append(post_algo_time - pre_algo_time)
		# Make the player's move
		if is_valid_location(board, player_col):
			player_row = get_next_open_row(board, player_col)
			drop_piece(board, player_row, player_col, PLAYER_PIECE)
			if winning_move(board, PLAYER_PIECE):
				message = "You won!"
				label = myfont.render(message, 1, RED)
				screen.blit(label, (40,10))
				player_wins += 1
				game_over = True
			print_board(board)
			draw_board(board)
			pygame.time.wait(2000)
			turn += 1
			turn = turn % 2
	# Ask for the opponent's input
	if turn == OPP and not game_over:				
		# Select the chosen opponent algorithm
		match opp_algo:
			# Minimax (without pruning)
			case 1:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				opp_col = minimax(board, 5, (not player_max), OPP_PIECE)[0]
				# Record the maximum amount of memory used
				opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				opp_time_per_turn.append(post_algo_time - pre_algo_time)
			# Minimax (with pruning)
			case 2:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				opp_col = minimax_pruning(board, 5, -math.inf, math.inf, (not player_max), OPP_PIECE)[0]
				# Record the maximum amount of memory used
				opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				opp_time_per_turn.append(post_algo_time - pre_algo_time)
			# Tabular Q-Learning
			case 3:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				Q = q_learning(board, epsilon=ep)
				# Record the maximum amount of memory used
				opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				opp_time_per_turn.append(post_algo_time - pre_algo_time)
				# Retrive the opponent's move
				opp_col = np.argmax(Q[tuple(board.flatten())])
				# Lower the value of epsilon for the next iteration to encourage exploitation over exploration
				ep -= 0.02
			# Default player
			case 4:
				# Start timing the algorithm
				pre_algo_time = time.perf_counter()
				# Begin monitoring the memory useage of the program
				tracemalloc.start()
				# Execute the algorithm
				opp_col = default_player(board, OPP_PIECE, PLAYER_PIECE)
				# Record the maximum amount of memory used
				opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            	# Stop monitoring 
				tracemalloc.stop()
				# Stop timing the algorithm
				post_algo_time = time.perf_counter()
				# Grab how long the algorithm takes to run
				opp_time_per_turn.append(post_algo_time - pre_algo_time)
		if is_valid_location(board, opp_col):
			#pygame.time.wait(500)
			opp_row = get_next_open_row(board, opp_col)
			drop_piece(board, opp_row, opp_col, OPP_PIECE)
			if winning_move(board, OPP_PIECE):
				message = "Opponent won!"
				label = myfont.render(message, 1, YELLOW)
				screen.blit(label, (40,10))
				opp_wins += 1
				game_over = True
			print_board(board)
			draw_board(board)
			pygame.time.wait(2000)
			turn += 1
			turn = turn % 2
	if game_over:
		num_games += 1
		# If the game is over and nobody won, record the draw
		if not winning_move(board, PLAYER_PIECE) and not winning_move(board, OPP_PIECE):
			message = "Draw!"
			label = myfont.render(message, 1, BLUE)
			screen.blit(label, (40,10))
			draws += 1
			pygame.time.wait(2000)
		# Paint over the message to get rid of it for the next game
		label = myfont.render(message, 1, (BLACK))
		screen.blit(label, (40,10))
		# Take the average time it took the player to complete a turn for every game that was played
		player_time_per_turn_per_game.append(np.mean(player_time_per_turn))
		player_time_per_turn = []
		# Take the average memory used by the player to complete a turn for every game that was played
		player_memory_per_turn_per_game.append(np.mean(player_memory_per_turn))
		player_memory_per_turn = []
		# Take the average time it took the opponent to complete a turn for every game that was played
		opp_time_per_turn_per_game.append(np.mean(opp_time_per_turn))
		opp_time_per_turn = []
		# Take the average memory used by the opponent to complete a turn for every game that was played
		opp_memory_per_turn_per_game.append(np.mean(opp_memory_per_turn))
		opp_memory_per_turn = []
		# Only exit when we've reach the total
		if num_games == TOTAL_GAMES:
			continue
		else:
			board = create_board()
			pygame.display.update()
			game_over = False

# Create a dictionary where the keys are the numbers corresponding to the algorithms the user choose and the values are the names of the corresponding algorithms
algo_dict = {1:'Minimax(without pruning)', 2:'Minimax(with pruning)', 3:'Tabular Q-Learning', 4:'Default'}

print()
print(f'Stats across {num_games} games:')
print(f'PLAYER ({algo_dict[player_algo]} algorithm):')
print(f'	Wins: {player_wins}')
print(f'	Average Time per Turn: {np.mean(player_time_per_turn_per_game)} Seconds')
print(f'	Average Maximum Memory Usage per Turn: {np.mean(player_memory_per_turn_per_game)} Bytes')
print()
print(f'OPPONENT ({algo_dict[opp_algo]} algorithm):')
print(f'	Wins: {opp_wins}')
print(f'	Average Time per Turn: {np.mean(opp_time_per_turn_per_game)} Seconds')
print(f'	Average Maximum Memory Usage per Turn: {np.mean(opp_memory_per_turn_per_game)} Bytes')
print()
print(f'DRAWS: {draws}')
print()
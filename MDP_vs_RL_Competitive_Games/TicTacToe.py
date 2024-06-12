# The code to generate the game was modified from: https://github.com/code-io0/tic-tac-toe-minimax/blob/main/main.py

import numpy as np
import pygame
import sys
from pygame.locals import *
from math import inf
import itertools
from collections import defaultdict
import random    
import time
import tracemalloc

# Function to draw the Tic Tac Toe Board
def draw_board():
	for row in range(3):
		for col in range(3):
			if board[row][col] == 1:
				screen.blit(o_image, ((col*200)+8, (row*200)+8))
			elif board[row][col] == -1:
				screen.blit(x_image, ((col*200)+8, (row*200)+8))

# Function to check if a player has won the game
def win(state, player):

	# All the possible win states
	win_state = [
		[state[0][0], state[0][1], state[0][2]],
		[state[1][0], state[1][1], state[1][2]],
		[state[2][0], state[2][1], state[2][2]],
		[state[0][0], state[1][0], state[2][0]],
		[state[0][1], state[1][1], state[2][1]],
		[state[0][2], state[1][2], state[2][2]],
		[state[0][0], state[1][1], state[2][2]],
		[state[2][0], state[1][1], state[0][2]],
	]

	# Check if there is a win
	if [player, player, player] in win_state:
		return True
	else:
		return False


# Check if the game is over
def game_over(state):
	return win(state, OPP) or win(state, PLAYER) or not empty_cells(state)


# Evaluate scores for the minimax function
def evaluate(state):

	if win(state, OPP):
		return OPP
	elif win(state, PLAYER):
		return PLAYER

	else:
		return 0

# Check the empty locations of the board
def empty_cells(board):

	cells = []

	for row in range(3):
		for col in range(3):
			if board[row][col] == 0:
				cells.append([row, col])

	return cells


# Display the win, lose, or draw messages on the board when the game has ended
def display_message(msg):
	text = game_font.render(msg, True, white, blue)
	text_rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))
	screen.blit(text, text_rect)


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
	# Action space size for Tic Tac Toe is 9 (3x3 board) - Initialize to 0s
	Q = defaultdict(lambda: np.zeros(9)) 
	action_space = list(range(9))
    
	# Begin Iterating through the episodes (simulated online learning)
	for episode in range(num_episodes):
		# Copy the current state of the board
		curr_board = np.copy(board)
		done = False
        
		while not done:
			# Convert the board to a tuple
			state = tuple(curr_board.flatten())  
            
			# Select action based on the probabilities for the epsilon greedy algorithm
			action = epsilon_greedy(Q, epsilon, action_space, state)
			# Convert the action location to (row, col) format  
			row, col = action // 3, action % 3
            
			# Check if the selected location is empty
			if curr_board[row, col] == 0:  
				# Update the board with the player's move
				curr_board[row, col] = 1  
                
                # Check if the game is over
				if game_over(curr_board):
					done = True
                    # Reward for winning or drawing
					if win(curr_board, 1) or (not win(curr_board, -1) and not win(curr_board, 1)):
						reward = 100
				else:
					# Opponent's move (randomly select an empty cell)
					empty_cells_list = empty_cells(curr_board)
					opp_row, opp_col = random.choice(empty_cells_list)
					# Update the board with the opponent's move
					curr_board[opp_row, opp_col] = -1  
                       
					# Check if the game is over after the opponent's move
					if game_over(curr_board):
						done = True
                       	# Reward for drawing
						if (not win(curr_board, -1) and not win(curr_board, 1)): 
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
def minimax(state, depth, isMaximizingPlayer, player_piece):

	# Initialize the values
	if isMaximizingPlayer:
		best = [-1, -1, -inf]
	else:
		best = [-1, -1, inf]

	# If the game is over, return a static evaluation of the position
	if game_over(state) or depth == 0:
		score = evaluate(board)
		return [-1, -1, score]

	# Use recursion to find the best scores
	for cell in empty_cells(state):
		row, col = cell
		state[row][col] = player_piece
		# Get the score for the next step
		score = minimax(state, depth - 1, isMaximizingPlayer=(not isMaximizingPlayer),player_piece=-player_piece)
		state[row][col] = 0
		score[0], score[1] = row, col

		# Computer is looking to maximize the next move
		if isMaximizingPlayer:
			if score[2] > best[2]:
				# Max value
				best = score 

		# Opponent is looking to minimize the output
		else:
			if score[2] < best[2]:
				# Min value
				best = score 

	return best

# Minimax function (with pruning)
def minimax_pruning(state, depth, alpha, beta, isMaximizingPlayer, player_piece):

	# Initialize the values
	if isMaximizingPlayer:
		best = [-1, -1, -inf]
	else:
		best = [-1, -1, inf]

	# If the game is over, return a static evaluation of the position
	if game_over(state) or depth == 0:
		score = evaluate(board)
		return [-1, -1, score]

	# Use recursion to find the best scores
	for cell in empty_cells(state):
		row, col = cell
		state[row][col] = player_piece
		# Get the score for the next step
		score = minimax_pruning(state, depth - 1, alpha=alpha, beta=beta, isMaximizingPlayer=(not isMaximizingPlayer), player_piece=-player_piece)
		state[row][col] = 0
		score[0], score[1] = row, col

		# Player is looking to maximize the next move
		if isMaximizingPlayer:
			if score[2] > best[2]:
				# Max value
				best = score 
			# Prune alpha
			alpha = max(alpha, score[2])

		# Player is looking to minimize the output
		else:
			if score[2] < best[2]:
				# Min value
				best = score 
			# Prune beta
			beta = min(beta, score[2])

		if beta <= alpha:
			break

	return best

# Function to create a default player who makes random moves unless it can make a winning move or block the opponent's winning move
def default_player(board, player, opp):
    # Check winning move for player
    for cell in empty_cells(board):
        row, col = cell
        board[row][col] = player
        if win(board, player):
            return row, col
        board[row][col] = 0

    # Check blocking opponent's winning move
    for cell in empty_cells(board):
        row, col = cell
        board[row][col] = opp
        if win(board, opp):
            board[row][col] = player
            return row, col
        board[row][col] = 0

    # If no winning or blocking move, choose random empty location
    return random.choice(empty_cells(board))


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
pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
# Load the images used for the game
bg_image = pygame.image.load("TicTacToe_utilities\\TicTacToe_Background.png")
bg_image = pygame.transform.scale(bg_image, (600,600))
o_image = pygame.image.load("TicTacToe_utilities\\TicTacToe_O.png")
x_image = pygame.image.load("TicTacToe_utilities\\TicTacToe_X.png")

game_font = pygame.font.SysFont('arial', 70)
white = pygame.Color('white')
blue = pygame.Color("#8114FF")

# Initialize the board
board = np.zeros((3,3))
# Initialize epsilon
ep = 0.3
# Initialize the players and the turn order
OPP = 1
PLAYER = -1
TURN = random.choice([OPP, PLAYER])

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

# Check to see which player goes first in order to see which player is the maximizing player for the minimax algorithm
if TURN == PLAYER:
	player_max = True
else:
	player_max = False

# Start the game
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	# Player's turn
	if TURN == 0:
		if not game_over(board):
			# Grab the depth of the board
			depth = len(empty_cells(board))
			match player_algo:
				# Minimax (without pruning)
				case 1:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					player_move = minimax(board, depth, player_max, PLAYER)
					# Record the maximum amount of memory used
					player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					player_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the player's move
					row, col = player_move[0],  player_move[1]
				# Minimax (with pruning)
				case 2:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					player_move = minimax_pruning(board, depth, -inf, inf, player_max, PLAYER)
					# Record the maximum amount of memory used
					player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					player_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the player's move
					row, col = player_move[0],  player_move[1]
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
					# Retrive the player's move
					player_move = np.argmax(Q[tuple(board.flatten())])
					# Converting the grid (list) format of the board into row,col coordinates
					row, col = player_move // 3, player_move % 3
					# Lower the value of epsilon for the next iteration to encourage exploitation over exploration
					ep -= 0.05
				# Default player
				case 4:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					player_move = default_player(board, PLAYER, OPP)
					# Record the maximum amount of memory used
					player_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					player_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the player's move
					row, col = player_move[0],  player_move[1]
			# Make the player's move
			board[row][col] = PLAYER
		# End turn
		TURN = 1

	# Opponent's turn
	elif TURN == 1:
		if not game_over(board):
			# Grab the depth of the board
			depth = len(empty_cells(board))
			match opp_algo:
				# Minimax (without pruning)
				case 1:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					opp_move = minimax(board, depth, (not player_max), OPP)
					# Record the maximum amount of memory used
					opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					opp_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the opponent's move
					row, col = opp_move[0], opp_move[1]
				# Minimax (with pruning)
				case 2:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					opp_move = minimax_pruning(board, depth, -inf, inf, (not player_max), OPP)
					# Record the maximum amount of memory used
					opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					opp_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the opponent's move
					row, col = opp_move[0], opp_move[1]
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
					opp_move = np.argmax(Q[tuple(board.flatten())])
					# Converting the grid (list) format of the board into row,col coordinates
					row, col = opp_move // 3, opp_move % 3
					# Lower the value of epsilon for the next iteration to encourage exploitation over exploration
					ep -= 0.05
				# Default player
				case 4:
					# Start timing the algorithm
					pre_algo_time = time.perf_counter()
					# Begin monitoring the memory useage of the program
					tracemalloc.start()
					# Execute the algorithm
					opp_move = default_player(board, OPP, PLAYER)
					# Record the maximum amount of memory used
					opp_memory_per_turn.append(tracemalloc.get_traced_memory()[1])
            		# Stop monitoring 
					tracemalloc.stop()
					# Stop timing the algorithm
					post_algo_time = time.perf_counter()
					# Grab how long the algorithm takes to run
					opp_time_per_turn.append(post_algo_time - pre_algo_time)
					# Retrive the opponent's move
					row, col = opp_move[0], opp_move[1]
			# Make the opponent's move
			board[row][col] = OPP
		# End turn
		TURN = 0


	screen.blit(bg_image, (0,0))
	draw_board()
	pygame.display.update()
	pygame.time.wait(2000)

	# Announce the result
	if game_over(board):
		num_games += 1
		if evaluate(board) == 1:
			display_message("  Opponent won!  ")
			opp_wins += 1
		elif evaluate(board) == -1:
			display_message("  You won!  ")
			player_wins += 1
		else:
			display_message("  Its a draw  ")
			draws += 1
		# Reset the board
		pygame.display.update()
		pygame.time.delay(2000)
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
		# Exit when we've played a specified number of games
		if num_games == TOTAL_GAMES:
			break
		board = np.zeros((3,3))

# Create a dictionary where the keys are the numbers corresponding to the algorithms the user choose and the values are the names of the corresponding algorithms
algo_dict = {1:'Minimax(without pruning)', 2:'Minimax(with pruning)', 3:'Tabular Q-Learning', 4:'Default'}

# Print the stats
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
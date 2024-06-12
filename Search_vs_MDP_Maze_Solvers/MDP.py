import numpy as np
import operator

# Set a global variable for the threshold of both algorithms
THRESH = 0.01

# A function that return the possible actions for a given state in a maze, (x,y)
def get_actions(maze,x,y):

    possible_actions = maze.maze_map[(x,y)]
    actions = []
    
    for direction, bool in possible_actions.items():
        # If it is possible to take an action, make note of it
        if bool==1:
            actions.append(direction)
    
    return actions


# A function that navigates a maze using MDP Policy Iteration
def value_iteration(maze, decay=0.9, threshold=THRESH):

    # Initialize reward, action, initial policy, optimal policy and value dicts
    rewards = {}
    policy = {}
    optimal_policy = {}
    value = {}

    # Grab the list of every state (cell) in the maze
    state_list=list(maze.maze_map.keys())

    
    # Initialize the rewards each state in the maze
    for state in state_list:
        # Goal cell
        if state == (1,1):
            rewards[state] = 1000
        # Every other state
        else:
            rewards[state] = -1
    

    # Set the policy for each action to be 1/the total number of actions in a state to initialize a random policy
    for state in state_list:
        
        policy[state] = {}

        for action in get_actions(maze, *state):
            policy[state][action] = 1.0 / len(get_actions(maze, *state))

    # Initialize the value of each state in the maze
    for state in state_list:
        value[state] = 0
        # Goal state
        if state == (1,1):
            value[state] = 10000

    # Begin the interation process
    while True:
        # Initialize the variable that stores the change in value at each iteration
        delta = 0

        # Start of an iteration
        for state in state_list:
            # Store the value of the current state before the iteration begins
            old_v = value[state]

            # Initialize the calculated value for the current state
            v = {}

            # Decide what action to take at the current state
            for action, a_prob in policy[state].items():
                match(action):
                    case 'N':
                        nxt = (state[0]-1, state[1])
                    case 'E':
                        nxt = (state[0], state[1]+1)
                    case 'W':
                        nxt = (state[0], state[1]-1)
                    case 'S':
                        nxt = (state[0]+1, state[1]) 

                # Bellman Equation - Calculate the new value for the current action
                v[action] = rewards[state] + (decay * value[nxt])

            # Grab the best action and the best value for the current state dictionary
            best_action_value = max(v.items(), key=operator.itemgetter(1))
            
            best_action = best_action_value[0]
            best_value = best_action_value[1]

            # Calculate the change between the old value and the new value of the current state
            delta = max(delta, np.abs(best_value - old_v))
            # Store the value of the best possible action at the current state in the optimal policy                        
            optimal_policy[state] = best_action
            # Record the best value of the currrent state
            value[state] = best_value
                
        # If the change is less than the provided threshold, exit      
        if delta < threshold:
            break

    # Get the best policy path
    value_iteration_path = []
    # Set the starter state to the beginning of the maze
    current_state = (maze.rows,maze.cols)
    value_iteration_path.append(current_state)

    # Grab the action to take at each state by following the optimal policy 
    while current_state != (1,1):
        
        direction = optimal_policy[current_state]

        match(direction):
            case 'N':
                current_state = (current_state[0]-1, current_state[1])
            case 'E':
                current_state = (current_state[0], current_state[1]+1)
            case 'W':
                current_state = (current_state[0], current_state[1]-1)
            case 'S':
                current_state = (current_state[0]+1, current_state[1])

        # Record the steps taken
        value_iteration_path.append(current_state)
    
    return value_iteration_path




def policy_iteration(maze, decay=0.9, threshold=THRESH):

    # Initialize reward and value arrays
    rewards = {}
    policy = {}
    optimal_policy = {}
    value={}
    
    # Grab the list of every state (cell) in the maze
    state_list=list(maze.maze_map.keys())

    
    # Initialize the rewards each state in the maze
    for state in state_list:
        # Goal state
        if state == (1,1):
            rewards[state] = 1000
        # Every other state
        else:
            rewards[state] = -1


    # Initialize the value of each state state in the maze
    for state in state_list:
        value[state] = 0
        # Goal state
        if state ==(1,1):
            value[state] = 10000


    # Set the policy to be 1/the total number of actions in a state to initialize a random policy
    for state in state_list:
        
        policy[state] = {}

        for action in get_actions(maze, *state):
            policy[state][action] = 1.0 / len(get_actions(maze, *state))

    
    # Policy iteration

    # Begin the interation process
    while True:
        
        # Start by evaluating the current policy  
        while True:
            # Initialize the variable that stores the change in value at each iteration
            delta = 0
            
            for state in state_list:
                # Store the value of the current state before the iteration begins
                old_v = value[state]

                # Initialize the calculated value for the current state
                v = 0
                
                for action, a_prob in policy[state].items():
                    match(action):
                        case 'N':
                            nxt = (state[0]-1, state[1])
                        case 'E':
                            nxt = (state[0], state[1]+1)
                        case 'W':
                            nxt = (state[0], state[1]-1) 
                        case 'S':
                            nxt = (state[0]+1, state[1])
                    
                    # Bellman Equation w/o the Max - Calculate the new value for the current action
                    v += a_prob * (rewards[state] + decay * value[nxt])

                # Calculate the change between the old value and the new value of the current state
                delta = max(delta, abs(v - old_v))
                # Update the value of the current state
                value[state] = v
            
            # If the change is less than the provided threshold, exit 
            if delta < threshold:
                break
        # End of Policy Evaluation
        
        # Will be set to False if the policy changes
        policy_stable = True
        
        for state in state_list:
            # Record the best action we could take under the current policy
            old_best_action = max(policy[state], key=policy[state].get)
            action_values = {}
            
            # Calculate the action values for all possible actions of the current state
            for action in get_actions(maze, *state):
                match(action):
                        case 'N':
                            nxt = (state[0]-1, state[1])
                        case 'E':
                            nxt = (state[0], state[1]+1)
                        case 'W':
                            nxt = (state[0], state[1]-1)
                        case 'S':
                            nxt = (state[0]+1, state[1])
                # One Step Look Ahead
                action_values[action] = rewards[state] + (decay * value[nxt])
            
            # Grab the best action and the best value for the current state dictionary
            best_action_value = max(action_values.items(), key=operator.itemgetter(1))
            # Only best actions are relevant 
            best_action = best_action_value[0]

            # If the best action to take is not the action dictated by the policy, then iterate again
            if old_best_action != best_action:
                policy_stable = False

            # Updating the policy for the best (deterministic) action
            for action in policy[state]:
                if action == best_action:
                    policy[state][action] = 1
                else:
                    policy[state][action] = 0

            # Update the optimal policy to reflect the best action in the current state
            optimal_policy[state] = best_action
        
        # Exit if we have converged
        if policy_stable:
            break

    # Get the best policy path
    policy_iteration_path = []
    # Set the starter state to the beginning of the maze
    current_state = (maze.rows, maze.cols)
    policy_iteration_path.append(current_state)
    
    # Grab the action to take at each state by following the optimal policy
    while current_state != (1, 1):

        direction = optimal_policy[current_state]

        match(direction):
            case 'N':
                current_state = (current_state[0]-1, current_state[1])
            case 'E':
                current_state = (current_state[0], current_state[1]+1)
            case 'W':
                current_state = (current_state[0], current_state[1]-1)
            case 'S':
                current_state = (current_state[0]+1, current_state[1])

        # Record the steps taken
        policy_iteration_path.append(current_state)
    
    return policy_iteration_path


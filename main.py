import grid
import qtable
import random
import numpy

north = 0
east = 1
south = 2
west = 3
pickup = 4

blank = 0
can = 1
wall = 2

def generate_robot_initial_position():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return [x, y]

def highest_reward_action(actions):
    highest_reward = -1
    choice = 0
    for x in range(0, 5):
        if actions[x] > highest_reward:
            highest_reward = actions[x]
            choice = x
    return choice

def choose_action(actions, epsilon):
    if (epsilon * 1000) >= random.randint(1, 1000):
        choice = random.randint(0, 4)
    else:
        choice = highest_reward_action(actions)
        if actions[choice] == 0:
            choice = random.randint(0, 4)
        while actions[choice] < 0:
            choice = random.randint(0, 4)
    return choice

def execute_action(action, robot_position, grid_world, initial_state):
    reward = 0
    if initial_state[action] == wall:
        reward = -5
    elif action == north:
        # robot_position = [robot_position[0], robot_position[1] + 1]
        robot_position[1] = robot_position[1] + 1
    elif action == east:
        robot_position[0] = robot_position[0] + 1
    elif action == south:
        robot_position[1] = robot_position[1] - 1
    elif action == west:
        robot_position[0] = robot_position[0] - 1
    elif action == pickup and initial_state[action] == blank:
        reward = -1
    elif action == pickup and initial_state[action] == can:
        grid_world[robot_position[1]][robot_position[0]] = blank
        reward = 10
    return reward

def q_table_update(initial_state, new_state, reward, q_table, action, n, y):
    initial_reward = q_table[initial_state][action]
    temp_var = initial_reward+n*(reward+y*numpy.amax(q_table[new_state])-initial_reward)
    q_table[initial_state][action] = temp_var

def step(robot_position, grid_world, q_table, n, y, epsilon):
    initial_state = grid.get_state(robot_position, grid_world)
    action = choose_action(q_table[initial_state], epsilon)
    # print("State" + str(initial_state))
    # print("Q table" + str(q_table[initial_state]))
    # print("Action numpy" + str(numpy.amax(q_table[initial_state])))
    # if action == north:
    #     print("action is north")
    # elif action == east:
    #     print("action is right")
    # elif action == south:
    #     print("action is south")
    # elif action == west:
    #     print("action is left")
    # elif action == pickup:
    #     print("action is pickup")
    reward = execute_action(action, robot_position, grid_world, initial_state)
    new_state = grid.get_state(robot_position, grid_world)
    q_table_update(initial_state, new_state, reward, q_table, action, n, y)
    return reward

def episode(steps, robot_position, grid_world, q_table, n, y, epsilon):
    reward = 0
    for x in range(0, steps):
        # print(robot_position)
        # grid.print_grid(grid_world, robot_position)
        reward += step(robot_position, grid_world, q_table, n, y, epsilon)
        # print("Reward: " + str(reward))
    return reward

def train(episodes, steps, epsilon, q_table, n, y):
    curr_average = 0
    for x in range(0, episodes):
        robot_position = generate_robot_initial_position()
        # print(robot_position)
        grid_world = grid.create_grid()
        # grid.print_grid(grid_world)
        if (x + 1) % 50 == 0 and epsilon != 0.0:
            epsilon -= 0.001
            # print(str(x) + " -> " + str(epsilon))
        reward = episode(steps, robot_position, grid_world, q_table, n, y, epsilon)
        curr_average += reward
        if (x + 1) % 100 == 0:
            print("At episode " + str(x + 1) + ", the total reward is: " + str(curr_average/100))
            curr_average = 0

def test():
    print("TODO")


# robot_position = generate_robot_initial_position()
# print(robot_position)
# grid_world = grid.create_grid()
# grid.print_grid(grid_world)
q_table = qtable.create_q_table()
# print(grid.get_state(robot_position, grid_world))
train(5000, 200, 0.1, q_table, 0.2, 0.9)
# grid.print_grid(grid_world)
qtable.print_q_table(q_table)

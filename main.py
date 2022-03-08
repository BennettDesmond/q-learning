import grid
import qtable
import random
import numpy
import matplotlib.pyplot as plt
import statistics

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


def step(robot_position, grid_world, q_table, n, y, epsilon, training):
    initial_state = grid.get_state(robot_position, grid_world)
    action = choose_action(q_table[initial_state], epsilon)
    reward = execute_action(action, robot_position, grid_world, initial_state)
    new_state = grid.get_state(robot_position, grid_world)
    if training:
        q_table_update(initial_state, new_state, reward, q_table, action, n, y)
    return reward


def episode(steps, robot_position, grid_world, q_table, n, y, epsilon, training):
    reward = 0
    for x in range(0, steps):
        reward += step(robot_position, grid_world, q_table, n, y, epsilon, training)
    return reward


def train(episodes, steps, epsilon, q_table, n, y):
    curr_average = 0
    y_points = []
    for x in range(0, episodes):
        robot_position = generate_robot_initial_position()
        grid_world = grid.create_grid()
        if (x + 1) % 50 == 0 and epsilon != 0.0:
            epsilon -= 0.001
        reward = episode(steps, robot_position, grid_world, q_table, n, y, epsilon, True)
        curr_average += reward
        if (x + 1) % 100 == 0:
            y_points.append(reward)
            curr_average = 0
    return y_points


def test(episodes, steps, q_table, n, y):
    reward_total = 0
    reward_vals = []
    for x in range(0, episodes):
        robot_position = generate_robot_initial_position()
        grid_world = grid.create_grid()
        reward = episode(steps, robot_position, grid_world, q_table, n, y, 0.0, False)
        reward_total += reward
        reward_vals.append(reward)
    print("---------Test Results---------")
    print("Average reward value: " + str(reward_total/episodes))
    print("Standard deviation: " + str(statistics.pstdev(reward_vals)))


print("Welcome to The Robot Cleaning Machine")
n = int(input("Please enter number of episodes:\n"))
m = int(input("Please enter number of steps:\n"))
print("Training uses the following values:\nepsilon -> 0.1\nn -> 0.2\ny -> 0.9")
q_table = qtable.create_q_table()
plt.plot(train(n, m, 0.1, q_table, 0.2, 0.9), linestyle='solid')
plt.show()
test(n, m, q_table, 0.2, 0.9)

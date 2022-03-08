import random
north = 0
east = 1
south = 2
west = 3
current = 4

blank = 0
can = 1
wall = 2

def can_existence():
    rand_num = random.randint(1, 100)
    if rand_num < 51:
        return 0
    else:
        return 1

def create_grid():
    grid = []
    for row in range(0, 10):
        grid_row = []
        for column in range(0, 10):
            grid_row.append(can_existence())
        grid.append(grid_row)
    return grid

def print_grid(grid, robot_position):
    for row in range(9, -1, -1):
        grid_row_str = ""
        for column in range(0, 10):
            if (robot_position[0] == column and robot_position[1] == row) and grid[row][column] == 0:
                grid_row_str += "R  "
            elif (robot_position[0] == column and robot_position[1] == row) and grid[row][column] == 1:
                grid_row_str += "RC "
            elif grid[row][column] == 1:
                grid_row_str += "C  "
            else:
                grid_row_str += ".  "
        print(grid_row_str)

def get_state(robot_location, grid):
    state = [blank, blank, blank, blank, blank]

    if robot_location[1] == 9:
        state[north] = wall
    # elif grid[robot_location[0]][robot_location[1] + 1] == can:
    elif grid[robot_location[1] + 1][robot_location[0]] == can:
        state[north] = can

    if robot_location[0] == 9:
        state[east] = wall
    # elif grid[robot_loca[robot_location[0]tion[0] + 1][robot_location[1]] == can:
    elif grid[robot_location[1]][robot_location[0] + 1] == can:
        state[east] = can

    if robot_location[1] == 0:
        state[south] = wall
    # elif grid[robot_location[0]][robot_location[1] - 1] == can:
    elif grid[robot_location[1] - 1][robot_location[0]] == can:
        state[south] = can

    if robot_location[0] == 0:
        state[west] = wall
    # elif grid[robot_location[0] - 1][robot_location[1]] == can:
    elif grid[robot_location[1]][robot_location[0] - 1] == can:
        state[west] = can

    # if grid[robot_location[0]][robot_location[1]] == can:
    if grid[robot_location[1]][robot_location[0]] == can:
        state[current] = can
    # print(state)
    return tuple(state)

def remove_can(position):
    grid[robot]




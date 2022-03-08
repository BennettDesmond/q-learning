import itertools

blank = 0
can = 1
wall = 2

def create_q_table():
    q_table = {}

    for v in itertools.product([0, 1], repeat=5):
        q_table[v] = [0, 0, 0, 0, 0]

    for v in itertools.product([0, 1], repeat=4):
        state = (*v[:2], wall, *v[2:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (*v[:3], wall, *v[3:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (*v[:1], wall, *v[1:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (wall, *v)
        q_table[state] = [0, 0, 0, 0, 0]

    for v in itertools.product([0, 1], repeat=3):
        state = (*v[:1], wall, wall, *v[1:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (*v[:2], wall, wall, *v[2:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (wall, *v[:2], wall, *v[2:])
        q_table[state] = [0, 0, 0, 0, 0]
        state = (wall, wall) + v
        q_table[state] = [0, 0, 0, 0, 0]

    # print(len(q_table))
    # print(q_table)
    # q_table[(0,0,2,2,2)][0] = 8
    # print(q_table)
    return q_table

def print_q_table(q_table):
    for key, value in q_table.items():
        print(key, ' : ', value)

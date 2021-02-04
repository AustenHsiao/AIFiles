# Robby the Robot is a robot that picks up cans. He can move in any of the 4 cardinal directions,
# pick up a can, or stay where he is. I was made aware of this puzzle in an AI class I took at Portland
# State University-- we were learning about genetic algorithms and covered Robby the Robot in high level.
# I wanted to code it out to see first-hand how well the algorithm does.

# this isn't designed to stress test the genetic algorithm, only to see that it works

import random as r

r.seed()

# there are 7 different movements, go left, go right, go up, go down, stay put, random direction, and pick up can
# the board is defined as a 10x10 grid


# creates the 10x10 board where each square has a 50% chance to have a can (0 = no can, 1 = yes can)
def board():
    surface = [[r.randint(0, 1) for i in range(10)] for ii in range(10)]
    return surface


# Creates generation 0
def initial_n(n):
    strategy = []
    # there are 243 unique configurations for the sensors, so each strategy has 243 elements
    for i in range(n):
        strategy.append([r.randint(0, 6) for i in range(0, 243)])
    return strategy


# For a given strategy, returns the fitness
# I'm just going to say that every single trial starts at board[4][4] (center)
def fitness(strat):

    # 0 - left; 1 - right
    # 2 - up; 3 - down
    # 4 - stay put; 5 - random direction
    # 6 - pick up can
    move_list = {0: (0, -1), 1: (0, 1), 2: (-1, 0),
                 3: (+1, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)}
    credit = 0
    penalty = 0

    for i in range(50):
        board_copy = board()
        start = (4, 4)

        for move in strat:
            del_x = move_list[move][0]
            del_y = move_list[move][1]
            if move == 5:
                random_direction = move_list[r.randint(0, 3)]
                del_x = random_direction[0]
                del_y = random_direction[1]
            elif move == 6:
                if board_copy[start[0]][start[1]] == 1:
                    board_copy[start[0]][start[1]] = 0
                    credit += 10
                else:
                    penalty -= 1
            if start[0] + del_x < 0 or start[0] + del_x >= 10 or start[1] + del_y < 0 or start[1] + del_y >= 10:
                penalty -= 5
                continue
            start = (start[0] + del_x, start[1] + del_y)

    return (credit + penalty) / 50.0


# given 2 parents, breed n number of children
def breed_n(parent1, parent2, n):
    children = []
    # crossover
    for i in range(n):
        cutoff = r.randint(0, 242)
        child = parent1[:cutoff] + parent2[cutoff:]

        # mutations
        for gene_index in range(len(child)):
            if r.randint(0, 200) == 1:
                child[gene_index] = r.randint(0, 6)
        children.append(child)
    return children


# run for n generations and specified population in each generation
def run_n(n, population):
    with open("data.txt", 'w') as fp:
        if n == 0:
            return
        parents = initial_n(population)
        fitness_list = [fitness(i) for i in parents]

        # find the two highest fitness parents
        parent1_index = fitness_list.index(max(fitness_list))
        parent1 = parents[parent1_index]
        parent1_fitness = fitness_list[parent1_index]
        print("Best fitness in gen 0 :", parent1_fitness)
        fp.write(str(parent1_fitness)+'\n')
        parent2 = parents[find_second_highest_value(
            parent1_index, fitness_list)]

        # for all of the remaining generations, we need to breed the two highest fitness parents
        for x in range(1, n):
            next_generation = breed_n(parent1, parent2, population)
            fitness_list = [fitness(i) for i in next_generation]
            parent1_index = fitness_list.index(max(fitness_list))
            parent1 = next_generation[parent1_index]
            parent1_fitness = fitness_list[parent1_index]
            print("Best fitness in gen", x, ":", parent1_fitness)
            fp.write(str(parent1_fitness)+'\n')
            parent2 = next_generation[find_second_highest_value(
                parent1_index, fitness_list)]
    return


# returns the index of the second highest value given the index of the first highest value
def find_second_highest_value(first_index, values):
    maximum_i = 0
    for i in range(len(values)):
        if values[i] > values[maximum_i] and i != first_index:
            maximum_i = i
    return maximum_i


# The normal approach
def run_normal(board, x, y, n=243, points=0):
    if n == 0:
        return points/243.0

    if x < 0 or x >= 10 or y < 0 or y >= 10:
        points -= 5
        if x < 0:
            x = 0
        elif x >= 10:
            x = 9
        elif y < 0:
            y = 0
        else:
            y = 9

    if board[x][y] == 1:
        points += 10
        board[x][y] = 0

    if y != 0 and board[x][y-1] == 1:  # left
        return run_normal(board, x, y-1, n-1, points)
    elif y != 9 and board[x][y+1] == 1:  # right
        return run_normal(board, x, y+1, n-1, points)
    elif x != 0 and board[x-1][y] == 1:  # up
        return run_normal(board, x-1, y, n-1, points)
    elif x != 9 and board[x+1][y] == 1:  # down
        return run_normal(board, x+1, y, n-1, points)
    else:  # choose a random direction
        choice = r.randint(0, 3)
        if choice == 0:
            return run_normal(board, x, y-1, n-1, points)
        elif choice == 1:
            return run_normal(board, x, y+1, n-1, points)
        elif choice == 2:
            return run_normal(board, x-1, y, n-1, points)
        else:
            return run_normal(board, x+1, y, n-1, points)


if __name__ == '__main__':
    #run_n(1000, 200)
    sum_of_averages = 0.0
    for i in range(1000):
        sum_of_averages += run_normal(board(), 4, 4)
    print("Sum of averages:", sum_of_averages/100.0)

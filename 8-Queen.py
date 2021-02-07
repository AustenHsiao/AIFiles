# Genetic algorithm for the 8-queens problem. Assumptions: 8x8 board

import random as r
r.seed()


class QueenGA:
    def __init__(self, PopulationSize, NumIterations, filename):
        if PopulationSize > 500000:
            print("Choose a population less than 500000")
            exit()

        with open(filename, 'w') as fp:
            # initial parents and fitness
            parents = self.original_parents(PopulationSize)
            fitness = self.fitness(parents)

            ave = float(sum(fitness) / len(fitness))
            fp.write('0 ' + str(ave) + " " + str(max(fitness)) + '\n')

            # normalize the fitness values
            normalization_value = sum(fitness)
            weights_list = [(fit * 1.0 / normalization_value)
                            for fit in fitness]

            # Do everything for the rest of the iterations
            for i in range(1, NumIterations):
                print("Running generation", i)
                next_parents = []
                for ii in range(0, PopulationSize):
                    # randomly choose the next two parents based on the weights
                    # and subsequently breed them
                    next_gen = r.choices(parents, weights=weights_list, k=2)
                    parent1 = next_gen[0]
                    parent2 = next_gen[1]
                    # ENABLE THIS IF YOU DONT WANT BOTH PARENTS TO BE THE SAME BOARD
                    # while parent1 == parent2:
                    #    parent2 = r.choices(parents, weights=weights_list)[0]
                    child = self.breed(parent1, parent2)

                    # ENABLE THIS IF YOU DONT WANT DUPLICATE CHILDREN IN THE NEXT GENERATION
                    # There's a chance we get stuck here if the population size is higher
                    # than the number of combinations. So I've limited the population size
                    # to 500000
                    # while child in next_parents:
                    #    child = self.breed(parent1, parent2)

                    next_parents.append(child)
                fitness = self.fitness(next_parents)

                # overwrite the last generation's parents--we don't need it anymore
                for iii in range(0, len(next_parents)):
                    parents[iii] = next_parents[iii]

                ave = float(sum(fitness) * 1.0 / len(fitness))
                fp.write(str(i) + " " + str(ave) +
                         " " + str(max(fitness)) + '\n')

                normalization_value = sum(fitness)
                weights_list = [(fit * 1.0 / normalization_value)
                                for fit in fitness]

        final_children = [(parents[i], fitness[i])
                          for i in range(len(parents))]
        final_children = sorted(final_children, key=lambda x: x[1])
        parent1 = final_children.pop()
        parent2 = final_children.pop()

        print("Final Parent1:", parent1[0], " ", parent1[1], "\nFinal Parent2:",
              parent2[0], " ", parent2[1], "\nEND")

    # takes in a number (size of parent population) for the initial
    # generation. This is generated randomly. Each parent is going to be a list
    # containing tuples. Each tuple has the form (x, y) where x is the horizontal axis
    # and y is the vertical axis
    def original_parents(self, PopulationSize):
        parents = []
        for i in range(PopulationSize):
            parent = []
            for queens in range(8):
                proposed_x = r.randint(0, 7)
                proposed_y = r.randint(0, 7)
                while (proposed_x, proposed_y) in parent:
                    proposed_x = r.randint(0, 7)
                    proposed_y = r.randint(0, 7)
                parent.append((proposed_x, proposed_y))
            parents.append(parent)
        return parents

    # returns an array containing the fitness for each parent in the passed array.
    # I've defined fitness as 100 - (sum of the number of queens that can attack each queen)
    def fitness(self, parents):
        return [self.single_parent_fitness(chromosome) for chromosome in parents]

    # returns the fitness for a single parent
    # In the trivial case, if we have any repeats, this means that multiple queens occupy the same
    # spot. This can't happen, so it gets assigned a bad fitness.
    # Otherwise it checks to see if any thing can attack in all directions
    # (2x horizontal, 2x vertical, 4x diagonal)
    # Fitness is defined as 100 - (sum of the number of queens that can attack each queen)
    def single_parent_fitness(self, parent):
        if len(set(parent)) < len(parent):
            return -8

        attackers = 0
        for queen in parent:
            x = queen[0]
            y = queen[1]
            for x_left in range(x-1, -1, -1):
                if (x_left, y) in parent:
                    attackers += 1
                    break
            for x_right in range(x+1, 8):
                if (x_right, y) in parent:
                    attackers += 1
                    break
            for y_up in range(y-1, -1, -1):
                if (x, y_up) in parent:
                    attackers += 1
                    break
            for y_down in range(y+1, 8):
                if (x, y_down) in parent:
                    attackers += 1
                    break
            for up_left in range(1, min(x, y)+1):
                if (x-up_left, y-up_left) in parent:
                    attackers += 1
                    break
            for down_left in range(1, min(x, y)+1):
                if (x-down_left, y+down_left) in parent:
                    attackers += 1
                    break
            for up_right in range(1, max(x, y)+1):
                if (x+up_right, y-up_right) in parent:
                    attackers += 1
                    break
            for down_right in range(1, max(x, y)+1):
                if (x+down_right, y+down_right) in parent:
                    attackers += 1
                    break
        return 100-attackers

    # breeds two parents. Result has been through the possibility of mutation
    def breed(self, parent1, parent2):
        cutoff = r.randint(0, len(parent1)-1)
        child = parent1[0:cutoff] + parent2[cutoff:]
        self.mutate(child)
        return child

    # based on chance, a single location may be mutated to something random
    def mutate(self, chromosome):
        if r.randint(0, 100) == 1:
            chromosome[r.randint(0, len(chromosome)-1)
                       ] = (r.randint(0, 7), r.randint(0, 7))
        return


if __name__ == '__main__':
    QueenGA(500, 2000, "pop500_iter2000.txt")

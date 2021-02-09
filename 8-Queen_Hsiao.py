# Written by Austen Hsiao for CS541

import random as r
r.seed()


class QueenGA:
    def __init__(self, populationSize, numIterations, filename):
        with open(filename, 'w') as fp:
            # set up the initial parents with random numbers
            # find the fitness for each one
            parents = self.original_parents(populationSize)
            fitness = self.fitness(parents)
            fp.write("0 " + str(sum(fitness)*1.0 / len(fitness)) +
                     " " + str(max(fitness)) + '\n')
            print("gen 0 " + str(sum(fitness)*1.0 / len(fitness)))

            for generation in range(1, numIterations):
                next_parents = []
                for i in range(populationSize):
                    # choose 2 parents to breed
                    next_gen = r.choices(parents, weights=fitness, k=2)
                    parent1 = next_gen[0]
                    parent2 = next_gen[1]
                    next_parents.append(self.breed(parent1, parent2))
                parents = next_parents
                fitness = self.fitness(parents)
                fp.write(str(generation) + " " + str(sum(fitness)*1.0 /
                                                     len(fitness)) + " " + str(max(fitness)) + '\n')
                print("gen" + str(generation) + " " +
                      str(sum(fitness)*1.0 / len(fitness)))
        print("End")

    # creates the initial set of parents. Each parent is a list of 8 integers between 0 and 7.
    # Index 0 represents the row index of the queen in column 0, etc.
    def original_parents(self, populationSize):
        return [[r.randint(0, 7) for ii in range(8)] for i in range(populationSize)]

    # returns a list of fitness for each chromosome. parent[i]'s fitness is fitness[i]
    def fitness(self, chromosomes):
        return [self.single_fitness(chromosome) for chromosome in chromosomes]

    def single_fitness(self, chromosome):
        # we won't have any attacking queens from the top or bottom, so we only have to consider
        # if queens are on the same rows. This will be the starting point for our fitness.
        # A set of 8 numbers has 28 distinct pairs (8 choose 2), so a perfect board will have
        # a fitness of 28
        fitness = 28 - (len(chromosome) - len(set(chromosome)))

        # Then we have to consider diagonal attacks. For each queen, figure out if there are queens
        # +/-1 1 column away, +/-2 2 columns away... etc.. We only have to figure out the number of attacking
        # queens from columns left to right since we're counting pairs. We also need a way to stop counting
        # if the attacker is shielded by a previous attacker-- this is why I have close_bot and close_top.
        for i in range(8):
            close_bot = 0
            close_top = 0
            for right_attacker in range(i+1, 8):
                if close_top == 1 and close_bot == 1:
                    break
                if chromosome[right_attacker] == chromosome[i] + (right_attacker - i) and close_top == 0:
                    fitness -= 1
                    close_top = 1
                if chromosome[right_attacker] == chromosome[i] - (right_attacker - i) and close_bot == 0:
                    fitness -= 1
                    close_bot = 1
        return fitness

    # breeds two parents (random cross point and with the chance of a mutation) to create a child
    def breed(self, parent1, parent2):
        cross_point = r.randint(0, len(parent1)-1)
        child = self.mutate(parent1[:cross_point] + parent2[cross_point:])
        return child

    def mutate(self, chromosome):
        # 1% chance for 1 random position to be changed to a random number 0-7
        if r.randint(0, 99) == 1:
            chromosome[r.randint(0, len(chromosome) - 1)] = r.randint(0, 7)
        return chromosome


if __name__ == '__main__':
    #QueenGA(10, 1000, "Pop10_Iter1000.txt")
    #QueenGA(100, 1000, "Pop100_Iter1000.txt")
    #QueenGA(500, 3000, "Pop500_Iter3000.txt")
    QueenGA(1000, 1000, "Pop1000_Iter1000_2.txt")
    #QueenGA(1000, 500, "Pop1000_Iter500.txt")

# Robby the Robot using Q-learning
import random as r
import numpy as np
import matplotlib.pyplot as plt


class board:
    # define a 10x10 grid with 0=clean 1=can
    def __init__(self):
        self.position = (r.randint(0, 9), r.randint(0, 9))
        self.board = [[r.randint(0, 1) for i in range(10)] for ii in range(10)]

    # returns a 5-tuple containing the rewards from performing the actions (up, down, left, right, pick up)
    # does not actually make a move
    def observe(self):
        x = self.position[0]
        y = self.position[1]

        up, down, left, right = 0, 0, 0, 0
        if x - 1 < 0:
            up = -5
        if x + 1 > 9:
            down = -5
        if y - 1 < 0:
            left = -5
        if y + 1 > 9:
            right = -5
        if self.board[x][y]:
            return (up, down, left, right, 10)
        return (up, down, left, right, -1)

    # m is 0:4, corresponding to each of the actions, (up, down, left, right, pick up)
    # updates the position
    def move(self, m):
        x = self.position[0]
        y = self.position[1]
        new_x = x
        new_y = y

        if m == 0:
            new_x -= 1
        elif m == 1:
            new_x += 1
        elif m == 2:
            new_y -= 1
        elif m == 3:
            new_y += 1

        if new_x < 0 or new_x > 9:
            new_x = x
        if new_y < 0 or new_y > 9:
            new_y = y

        self.position = (new_x, new_y)
        return


class q_learn:
    # 5 actions (up(0), down(1), left(2), right(3), pick up a can(4))
    # 100 states-- initialized to 0
    def __init__(self):
        self.qTable = [[0 for i in range(5)] for ii in range(100)]
        self.episodes = 5000
        self.steps = 200
        self.learningRate = 0.2
        self.discountFactor = 0.9
        self.epsilon = 0.1  # decreases every 50 epochs until 0

    def greedyMove(self, board):
        # determine which action to take
        observed_rewards = np.array(board.observe())
        primary_move = np.random.choice(np.flatnonzero(
            observed_rewards == observed_rewards.max()))  # random tiebreaking for maximum value
        explore = np.random.choice(
            [True, False], p=[self.epsilon, 1-self.epsilon])

        # perform action, update Q matrix
        if not explore:
            reward = observed_rewards[primary_move]
            self.updateQ(board, reward, primary_move)
            board.move(primary_move)
            return

        # perform a different action (explore)
        explore_move = np.random.choice([0, 1, 2, 3, 4])
        while explore_move == primary_move:
            explore_move = np.random.choice([0, 1, 2, 3, 4])
        reward = observed_rewards[explore_move]
        self.updateQ(board, reward, explore_move)
        board.move(explore_move)

    def updateQ(self, board, reward, move):
        x = board.position[0] * board.position[1]
        y = move
        max_Q_next = max(qTable[x])
        self.qTable[x][y] += self.learningRate * \
            (reward + self.discountFactor * max_Q_next - self.qTable[x][y])

    # runs q learning using the values specified in the constructor to create the policy
    def train(self):
        for run in range(self.episodes):
            board = board()
            for i in range(self.steps):


if __name__ == '__main__':
    print(q_learn().greedyMove())

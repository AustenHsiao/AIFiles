# Robby the Robot using Q-learning. Written by Austen Hsiao for AI at PSU
import random as r
import numpy as np
import matplotlib.pyplot as plt

r.seed()


class Robby:
    def __init__(self):
        self.board = [[r.randint(0, 1) for i in range(10)] for ii in range(10)]
        self.currentLocation = (r.randint(0, 9), r.randint(0, 9))

    def checkSensor(self):
        x = self.currentLocation[0]
        y = self.currentLocation[1]
        current = (x, y)
        north = (x-1, y)
        south = (x+1, y)
        east = (x, y+1)
        west = (x, y-1)
        return "{c} {n} {s} {e} {w}".format(c=self.tileCheck(current), n=self.tileCheck(north), s=self.tileCheck(south), e=self.tileCheck(east), w=self.tileCheck(west))

    # used internally
    def tileCheck(self, tile):
        if tile[0] < 0 or tile[0] > 9 or tile[1] < 0 or tile[1] > 9:
            return 'W'  # Wall
        elif self.board[tile[0]][tile[1]] == 1:
            return 'C'  # Can
        return 'E'  # Empty

    def performAction(self, m):
        x = self.currentLocation[0]
        y = self.currentLocation[1]
        reward = 0
        moveTo_x = x
        moveTo_y = y
        # pick up can
        if m == 0:
            if self.board[x][y] == 1:
                self.board[x][y] = 0
                return 10
            else:
                return -1
        elif m == 1:  # north
            moveTo_x -= 1
        elif m == 2:  # south
            moveTo_x += 1
        elif m == 3:  # east
            moveTo_y += 1
        elif m == 4:  # west
            moveTo_y -= 1

        if moveTo_x < 0 or moveTo_x > 9:  # Wall
            moveTo_x = x
            reward = -5
        elif moveTo_y < 0 or moveTo_y > 9:
            moveTo_y = y
            reward = -5
        self.currentLocation = (moveTo_x, moveTo_y)
        return reward


class QLearn:
    def __init__(self):
        possibleState = ['W', 'C', 'E']
        self.qTable = {}
        for i in possibleState:
            for ii in possibleState:
                for iii in possibleState:
                    for iv in possibleState:
                        for v in possibleState:
                            self.qTable["{current} {north} {south} {east} {west}".format(
                                current=i, north=ii, south=iii, east=iv, west=v)] = [0, 0, 0, 0, 0]
        # This is ugly but it will make the logic very simple. The states are stored as key:value pairs:
        # "currentState northState southState eastState westState":[current, north, south, east, west]
        self.episodes = 5000
        self.steps = 200
        self.learningRate = 0.2
        self.discountFactor = 0.9

    def greedyMove(self, grid, epsilon):
        # 1 observe current state.
        # 2 choose action
        # 3 perform action
        # 4 observe new state
        # 5 update qtable

        # 1
        currentState = grid.checkSensor()
        actionList = self.qTable[currentState]
        # 2
        action = np.random.choice(
            np.flatnonzero(np.array(actionList) == np.array(actionList).max()))
        # action result 0 = pick up can; 1-4=>{go north, south, east, west}
        explore = np.random.choice(
            np.array([True, False]), p=[epsilon, 1-epsilon])
        if explore:
            explore_action = r.randint(0, 4)
            while explore_action == action:
                explore_action = r.randint(0, 4)
            action = explore_action
        # 3
        reward = grid.performAction(action)
        # 4
        nextState = grid.checkSensor()
        # 5
        self.qTable[currentState][action] = self.qTable[currentState][action] + self.learningRate * (reward + self.discountFactor *
                                                                                                     max(self.qTable[nextState]) - self.qTable[currentState][action])
        return reward

    def train(self):
        data = []
        epsilon = 0.1
        for episode in range(self.episodes):
            grid = Robby()
            reward = 0
            if episode % 50 and episode != 0:
                epsilon -= 0.0005
                if epsilon < 0:
                    epsilon = 0
            for step in range(self.steps):
                reward += self.greedyMove(grid, epsilon)
            if episode % 100 == 0:
                data.append((episode, reward))

        x = [i[0] for i in data]
        y = [i[1] for i in data]
        plt.scatter(x, y)
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.title('Training Reward')
        plt.savefig('TrainingReward.png')


if __name__ == '__main__':
    QLearn().train()

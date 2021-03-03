#Robby the Robot using Q-learning
import random as r

class board:
    def __init__(self):
        self.board = [ [r.randint(0,1) for i in range(10)] for ii in range(10)]


if __name__ == '__main__':
    print('1')
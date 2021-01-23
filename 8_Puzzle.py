# This script is written by Austen Hsiao for CS541. This assignment implements search
# algorithms for the 8-puzzle

########################################################################################
# The Node class creates a node in the tree of the puzzle problem. Every node
# stores information about its current state, its parent, how it got there (action)
# and the cost of moving there
########################################################################################
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


########################################################################################
# Frontier class will hold the frontier nodes. sqDimension refers to one dimension of
# the square grid (3 for the 8-puzzle, 4 for the 15-puzzle)
########################################################################################
class Frontier:
    def __init__(self, inputState, sqDimension):
        self.dimension = sqDimension
        self.parent = inputState
        # Find location of the blank space in 2d
        for i in range(0, len(inputState.state)):
            if inputState.state[i] == 'b':
                self.x = i // 3
                self.y = i % 3

        # Rows creates the board in 2d, this will make it easier to find allowable moves
        self.rows = self.twoDBoard()

    ##### locations() returns a list containing all the nodes of possible movement #####
    def locations(self):
        frontierList = []
        # Top
        topx = self.x - 1
        # Bot
        botx = self.x + 1
        # Right
        righty = self.y + 1
        # Left
        lefty = self.y - 1

        # if the blank can move up
        if topx >= 0 and topx < self.dimension:
            self.rows
            self.rows[self.x][self.y] = self.rows[topx][self.y]
            self.rows[topx][self.y] = 'b'

            top = Node(self.flatBoard(self.rows), self.parent, 'top', 1)

            # undo changes
            self.rows[topx][self.y] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            # add the node to the frontier list
            frontierList.append(top)
        if botx >= 0 and botx < self.dimension:
            self.rows[self.x][self.y] = self.rows[botx][self.y]
            self.rows[botx][self.y] = 'b'

            bot = Node(self.flatBoard(self.rows), self.parent, 'bot', 1)

            self.rows[botx][self.y] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            frontierList.append(bot)
        if righty >= 0 and righty < self.dimension:
            self.rows[self.x][self.y] = self.rows[self.x][righty]
            self.rows[self.x][righty] = 'b'

            right = Node(self.flatBoard(self.rows), self.parent, 'right', 1)

            self.rows[self.x][righty] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            frontierList.append(right)
        if lefty >= 0 and lefty < self.dimension:
            self.rows[self.x][self.y] = self.rows[self.x][lefty]
            self.rows[self.x][lefty] = 'b'

            left = Node(self.flatBoard(self.rows), self.parent, 'left', 1)

            self.rows[self.x][lefty] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            frontierList.append(left)
        return frontierList

    def twoDBoard(self):
        # returns a 2d board
        return [list(self.parent.state[i:i+self.dimension]) for i in range(0, len(self.parent.state), self.dimension)]

    def flatBoard(self, board):
        # the board has to be in 2d
        flat = []
        for i in board:
            flat += i
        return flat


########################################################################################
# The search class defines the basic search functions
########################################################################################
class Search:
    def __init__(self, startState):
        self.root = startState

    # Given a board, startState, return bool for whether or not it's solvable
    # based on inversion from the course page.
    # A board is solvable if the inversion parity is even
    def isSolvable(self):
        inversions = 0
        # cindex = comparison index
        # iindex = iterating index
        for cindex in range(0, len(self.root.state)):
            if self.root.state[cindex] == 'b':
                continue
            for iindex in range(cindex + 1, len(self.root.state)):
                if self.root.state[iindex] == 'b':
                    continue
                if self.root.state[cindex] > self.root.state[iindex]:
                    inversions += 1
        if inversions % 2 == 0:
            return True
        return False


########################################################################################
# The BestFirst class is derived from search. BestFirst algorithm
########################################################################################
class BestFirst(Search):
    def __init__(self, startState):
        super().__init__(startState)


if __name__ == '__main__':
    root = Node('b12345678')
    for i in Frontier(root, 3).locations():
        print(''.join(i.state))

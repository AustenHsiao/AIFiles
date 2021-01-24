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

    # set up the sort() function
    def __lt__(self, node):
        return self.cost < node.cost


########################################################################################
# Frontier class will hold the frontier nodes. sqDimension refers to one dimension of
# the square grid (3 for the 8-puzzle, 4 for the 15-puzzle)
########################################################################################
class Frontier:
    def __init__(self, inputState):
        if len(inputState.state) == 9:
            self.dimension = 3
        else:
            self.dimension = 4

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

            topBoard = self.flatBoard(self.rows)
            top = Node(topBoard, self.parent, 'top',
                       self.correctSpaceCost(topBoard))

            # undo changes
            self.rows[topx][self.y] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            # add the node to the frontier list
            frontierList.append(top)
        if botx >= 0 and botx < self.dimension:
            self.rows[self.x][self.y] = self.rows[botx][self.y]
            self.rows[botx][self.y] = 'b'

            botBoard = self.flatBoard(self.rows)
            bot = Node(botBoard, self.parent, 'bot',
                       self.correctSpaceCost(botBoard))

            self.rows[botx][self.y] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            frontierList.append(bot)
        if righty >= 0 and righty < self.dimension:
            self.rows[self.x][self.y] = self.rows[self.x][righty]
            self.rows[self.x][righty] = 'b'

            rightBoard = self.flatBoard(self.rows)
            right = Node(rightBoard, self.parent, 'right',
                         self.correctSpaceCost(rightBoard))

            self.rows[self.x][righty] = self.rows[self.x][self.y]
            self.rows[self.x][self.y] = 'b'

            frontierList.append(right)
        if lefty >= 0 and lefty < self.dimension:
            self.rows[self.x][self.y] = self.rows[self.x][lefty]
            self.rows[self.x][lefty] = 'b'

            leftBoard = self.flatBoard(self.rows)
            left = Node(leftBoard, self.parent, 'left',
                        self.correctSpaceCost(leftBoard))

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

    # correctSpaceCost() gives a cost based on the number of tiles in the correct space, the goal is '12345678b'
    def correctSpaceCost(self, board):
        cost = 0
        goal = [i for i in range(1, self.dimension*self.dimension)] + ['b']
        for i in range(0, self.dimension*self.dimension):
            if goal[i] != board[i]:
                cost += 1
        return cost


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
        # this is only good for 8-puzzle and 15 puzzle
        if len(startState.state) == 9:
            self.dimension = 3
        else:
            self.dimension = 4
        self.nodeQueue = Frontier(startState).locations()

    # Returns true if we're in the goal state. False otherwise
    def goalStateCheck(self, board):
        goal = ''.join([str(i) for i in range(
            1, self.dimension*self.dimension)] + ['b'])
        for i in range(0, len(goal)):
            if goal[i] != board[i]:
                return False
        return True

    def search(self):
        return self.privSearch(self.root)

    def privSearch(self, root):
        visited = [self.root.state]
        if self.goalStateCheck(root.state):
            currentRoot = root
            path = []
            while currentRoot != self.root:
                path.append(currentRoot.state)
                currentRoot = currentRoot.parent
            path.append(self.root.state)
            for i in path[::-1]:
                print(i)
            return visited

        moveLimit = 1000
        while len(self.nodeQueue) != 0 and moveLimit > 0:
            self.nodeQueue.sort()
            lowCost = self.nodeQueue.pop(0)
            if ''.join(lowCost.state) in visited:
                continue
            visited.append(''.join(lowCost.state))
            if self.goalStateCheck(lowCost.state):
                currentRoot = lowCost
                path = []

                while currentRoot != self.root:
                    path.append(''.join(currentRoot.state))
                    currentRoot = currentRoot.parent
                path.append(self.root.state)

                for i in range(len(path)-1, 0, -1):
                    print(path[i], ' --> ', sep='', end='')
                print(path[0], sep='')
                return visited
            for node in Frontier(lowCost).locations():
                if ''.join(node.state) not in visited:
                    self.nodeQueue += [node]
            moveLimit -= 1

        print("Solution was not found within 1000 actions\nVisited nodes:")
        return visited


if __name__ == '__main__':
    BestFirst(Node('152b43786')).search()

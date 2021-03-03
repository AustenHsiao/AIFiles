class Farmer:
    def __init__(self):
        self.left_side = ['G', 'B', 'F']
        self.right_side = []
        self.boat = []

    def issues(self):
        if len(self.boat) > 1:
            return True

        if 'G' in left_side and 'F' in left_side:
            return True
        elif 'G' in right_side and 'F' in right_side:
            return True
        elif 'G' in left_side and 'B' in left_side:
            return True
        elif 'G' in right_side and 'B' in right_side:
            return True
        return False

    def cross_river(self, n=0):
        while set(self.right_side) != set(['G', 'B', 'F']):

            if self.issues():


if __name__ == '__main__':

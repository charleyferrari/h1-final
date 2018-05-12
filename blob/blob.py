import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go


class GridMover:

    # Init grid mover class with row, col, and grid
    # Along with some helper variables for the algorithm
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.visited = [[self.row, self.col]]
        self.visitedlag = []
        self.checked = []
        self.grid = grid
        self.firstGridTouch = None
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.direction = 'SE'
        self.usedDirections = []
        self.doneLoop = False
        self.checked = []

    # Move through directions counterclockwise
    # (Ideally this would also include a random start to find the edge of the grid)
    def nextDirection(self):
        while True:
            if self.direction == 'Start':
                self.direction = 'SE'
                break
            if self.direction == 'SE':
                self.direction = 'NE'
                break
            if self.direction == 'NE':
                self.direction = 'NW'
                break
            if self.direction == 'NW':
                self.direction = 'SW'
                break
            if self.direction == 'SW':
                self.direction = 'SE'
                break

    def returnNextMove(self):
        booldict = dict(n=False, s=False, e=False, w=False)
        if self.direction == 'SE':
            # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1] not in self.visited:
                    booldict['e'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col] not in self.visited:
                    booldict['s'] = True
            # Prefer South, that will be on outside
            if booldict['s']:
                return [self.row+1, self.col]
            elif booldict['e']:
                return [self.row, self.col+1]
            else:
                self.nextDirection()
                self.returnNextMove()
        elif self.direction == 'NE':
            # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1] not in self.visited:
                    booldict['e'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col] not in self.visited:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                return [self.row-1, self.col]
            elif booldict['e']:
                return [self.row, self.col+1]
            else:
                self.nextDirection()
                self.returnNextMove()
        elif self.direction == 'NW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1] not in self.visited:
                    booldict['w'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col] not in self.visited:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                return [self.row-1, self.col]
            elif booldict['w']:
                return [self.row, self.col-1]
            else:
                self.nextDirection()
                self.returnNextMove()
        elif self.direction == 'SW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1] not in self.visited:
                    booldict['w'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col] not in self.visited:
                    booldict['s'] = True
            # Prefer South, that will be out outside
            if booldict['s']:
                return [self.row+1, self.col]
            elif booldict['w']:
                return [self.row, self.col-1]
            else:
                self.nextDirection()
                self.returnNextMove()

    # Main algorithm: Recursively moves in one of the diagonal directions
    def moveNext(self):
        booldict = dict(n=False, s=False, e=False, w=False)
        if self.direction == 'SE':
                # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1] not in self.visited:
                    booldict['e'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col] not in self.visited:
                    booldict['s'] = True
            # Prefer South, that will be on outside
            if booldict['s']:
                self.moveDown()
                if [self.row+1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['e']:
                self.moveRight()
                if [self.row, self.col+1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNext()
        elif self.direction == 'NE':
            # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1] not in self.visited:
                    booldict['e'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col] not in self.visited:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                self.moveUp()
                if [self.row-1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['e']:
                self.moveRight()
                if [self.row, self.col+1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNext()
        elif self.direction == 'NW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1] not in self.visited:
                    booldict['w'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col] not in self.visited:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                self.moveUp()
                if [self.row-1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['w']:
                self.moveLeft()
                if [self.row, self.col-1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNext()
        elif self.direction == 'SW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1] not in self.visited:
                    booldict['w'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col] not in self.visited:
                    booldict['s'] = True
            # Prefer South, that will be out outside
            if booldict['s']:
                self.moveDown()
                if [self.row+1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['w']:
                self.moveLeft()
                if [self.row, self.col-1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNext()
        else:
            self.moveNextSoft()

    # "Soft" algorithm. Needed due to a conflict in testing whether the cell is visited
    # and not moving, and allowing the move when the hard algorithm fails.
    # (I would have rather had a more elegant solution for this, but it works in a pinch!)
    def moveNextSoft(self):
        booldict = dict(n=False, s=False, e=False, w=False)
        if self.direction == 'SE':
            # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1]:
                    booldict['e'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col]:
                    booldict['s'] = True
            # Prefer South, that will be on outside
            if booldict['s']:
                self.moveDown()
                if [self.row+1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['e']:
                self.moveRight()
                if [self.row, self.col+1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNextSoft()
        elif self.direction == 'NE':
            # East
            if self.canMoveRight():
                if self.grid[self.row, self.col+1] and [self.row, self.col+1]:
                    booldict['e'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col]:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                self.moveUp()
                if [self.row-1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['e']:
                self.moveRight()
                if [self.row, self.col+1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNextSoft()
        elif self.direction == 'NW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1]:
                    booldict['w'] = True
            # North
            if self.canMoveUp():
                if self.grid[self.row-1, self.col] and [self.row-1, self.col]:
                    booldict['n'] = True
            # Prefer North, that will be on outside
            if booldict['n']:
                self.moveUp()
                if [self.row-1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['w']:
                self.moveLeft()
                if [self.row, self.col-1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNextSoft()
        elif self.direction == 'SW':
            # West
            if self.canMoveLeft():
                if self.grid[self.row, self.col-1] and [self.row, self.col-1]:
                    booldict['w'] = True
            # South
            if self.canMoveDown():
                if self.grid[self.row+1, self.col] and [self.row+1, self.col]:
                    booldict['s'] = True
            # Prefer South, that will be out outside
            if booldict['s']:
                self.moveDown()
                if [self.row+1, self.col] in self.visited:
                    self.doneLoop = True
            elif booldict['w']:
                self.moveLeft()
                if [self.row, self.col-1] in self.visited:
                    self.doneLoop = True
            else:
                self.nextDirection()
                self.moveNextSoft()

    # Some assignment helper functions
    def assignFirstGridTouch(self):
        if not self.firstGridTouch:
            if self.grid[self.row, self.col]:
                self.firstGridTouch = [self.row, self.col]

    def reassignAll(self):
        self.assignNewTop()
        self.assignNewBottom()
        self.assignNewLeft()
        self.assignNewRight()

    def assignNewTop(self):
        if self.grid[self.row, self.col]:
            if not self.top:
                self.top = self.row
            elif self.row < self.top:
                self.top = self.row

    def assignNewBottom(self):
        if self.grid[self.row, self.col]:
            if not self.bottom:
                self.bottom = self.row
            elif self.row > self.bottom:
                self.bottom = self.row

    def assignNewLeft(self):
        if self.grid[self.row, self.col]:
            if not self.left:
                self.left = self.col
            elif self.col < self.left:
                self.left = self.col

    def assignNewRight(self):
        if self.grid[self.row, self.col]:
            if not self.right:
                self.right = self.col
            elif self.col > self.right:
                self.right = self.col

    # Testing if moves are possible
    def canMoveRight(self):
        if self.col >= 9:
            return False
        else:
            return True

    def canMoveLeft(self):
        if self.col <= 0:
            return False
        else:
            return True

    def canMoveUp(self):
        if self.row <= 0:
            return False
        else:
            return True

    def canMoveDown(self):
        if self.row >= 9:
            return False
        else:
            return True

    # Make the move. Append the visited cell. make new assignments
    # if you're on the grid. Assign firstTouchGrid when you touch the grid
    # for the first time.
    def moveRight(self):
        self.col += 1
        self.visited.append([self.row, self.col])
        if not self.firstGridTouch:
            if self.grid[self.row, self.col]:
                self.assignFirstGridTouch()
        else:
            self.reassignAll()

    def moveLeft(self):
        self.col -= 1
        self.visited.append([self.row, self.col])
        if not self.firstGridTouch:
            if self.grid[self.row, self.col]:
                self.assignFirstGridTouch()
        else:
            self.reassignAll()

    def moveUp(self):
        self.row -= 1
        self.visited.append([self.row, self.col])
        if not self.firstGridTouch:
            if self.grid[self.row, self.col]:
                self.assignFirstGridTouch()
        else:
            self.reassignAll()

    def moveDown(self):
        self.row += 1
        self.visited.append([self.row, self.col])
        if not self.firstGridTouch:
            if self.grid[self.row, self.col]:
                self.assignFirstGridTouch()
        else:
            self.reassignAll()

    # Check moves
    # Ideally this is where I would get my checked cells, but didn't have time to add that.
    def checkRight(self):
        self.checked.append([self.row, self.col+1])
        return self.grid[self.row, self.col+1]

    def checkLeft(self):
        self.checked.append([self.row, self.col-1])
        return self.grid[self.row, self.col-1]

    def checkUp(self):
        self.checked.append([self.row-1, self.col])
        return self.grid[self.row-1, self.col]

    def checkDown(self):
        self.checked.append([self.row+1, self.col])
        return self.grid[self.row+1, self.col]


grid = np.array([
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
x = GridMover(4, 1, grid)

while True:
    x.moveNext()
    if x.doneLoop:
        break

print(dict(
    left=x.left,
    right=x.right,
    top=x.top,
    bottom=x.bottom,
    visited=len(x.visited)))

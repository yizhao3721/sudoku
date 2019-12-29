# @app.after_request
# def main():
#    grid = input
#import pandas as pd
#grid = []

# validates initial user input, so if there are two or more of the same number in a row/col/box, returns false


def validate_input(grid):
    # make sure each row is duplicate free
    for row in range(9):
        # print("hello")
        for i in range(1,10):
            count = 0
            for col in range(9):
                if(grid[row][col] == i):
                    count += 1
                    # print("yo")
                    # print(count)
            if(count > 1):
                return False
    # each col is duplicate free
    for col in range(9):
        # print("hello")
        for i in range(1, 10):
            count = 0
            for row in range(9):
                if(grid[row][col] == i):
                    count += 1
                    # print("yo")
                    # print(count)
            if(count > 1):
                return False
    # each box is duplicate free
    for box_left in range(0, 7, 3):
        for box_top in range(0, 7, 3):
            for i in range(1, 10):
                count = 0
                for row in range(box_left, box_left+3):
                    for col in range(box_top, box_top+3):
                        if(grid[row][col] == i):
                            count += 1
                            # print("yo")
                            # print(count)
                if(count > 1):
                    return False
    return True
    """
    for i in range(1,10):
        for col in range(9):
            count = 0
            for row in range(9):
                if(grid[row][col] == i):
                    count += 1
            if(count > 1):
                return False
    for i in range(1,10):
        for box_left in range(0,7,3):
            for box_top in range(0,7,3):
                count = 0
                for row in range(box_left, box_left+3):
                    for col in range(box_top, box_top+3):
                        if(grid[row][col] == i):
                            count += 1
            if(count > 1):
                return False"""


# check to see if number is already in row
def check_row(row, i, grid):
    for col in range(0, 9):
        if grid[row][col] == i:
            return False
    return True

# is number already in col


def check_col(col, i, grid):
    for row in range(0, 9):
        if grid[row][col] == i:
            return False
    return True

# is number already in box


def check_box(row, col, i, grid):
    box_left = row - row % 3
    box_top = col - col % 3
    for k in range(3):
        for j in range(3):
            if grid[k + box_left][j + box_top] == i:
                return False
    return True

# can input number in grid


def valid_input(row,col, i, grid):
    if(check_row(row, i, grid)):
        if(check_col(col, i, grid)):
            if(check_box(row, col, i, grid)):
                return True
    return False

# find the next blank cell


def next_blank_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return (-1, -1)

# solve sudoku using backtracking


def solveDoku(grid):
    if(not validate_input(grid)):
        return False

    (row, col) = next_blank_cell(grid)
    if (row == -1 or col == -1):
        return (True, grid)
    #print(row, col)
    for i in range(1, 10):

        if(valid_input(row, col, i, grid)):

            grid[row][col] = i
            if(solveDoku(grid)):
                return (True, grid)

            grid[row][col] = 0

    return False

# def main():
    # print(solveDoku(grid))
    # print(grid)

# if __name__ == "__main__":
    # main()

# class Node(object):
#     def __init__(self, parent, r, c, potentialValues):
#         self.parent = parent
#         self.row = r
#         self.col = c
#         self.values = potentialValues # is a list of potential values
#     def getParent():
#         return self.parent
#     def getRow():
#         return self.row
#     def getCol():
#         return self.col
#     def get
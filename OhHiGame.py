import numpy as np

# Define some usefull "constants"
NONE = 0
RED = 1
BLUE = 2


def printColor(color):
    if (color == NONE):
        print("NONE")

    elif (color == BLUE):
        print("BLUE")

    elif (color == RED):
        print("RED")

    else:
        print(color)


def get_opposite(color):
    if(color == RED):
        return BLUE
    elif(color == BLUE):
        return RED
    else:
        return NONE


class Solver:
    def __init__(self, size, board):
        self.size = size
        self.board = np.array(board)

    def Solve(self):
        lastBoard = np.zeros((self.size, self.size))

        # Look for obvious solutions as long as more progress is made
        while(lastBoard[lastBoard != self.board].size != 0):
            lastBoard = np.copy(self.board)

            if(not self.__check_all_row_col()):
                return False

            for x in range(self.size):
                for y in range(self.size):
                    if(not self.__check_adjacents(x, y)):
                        return False  # Gone down wrong path, not solvable

        # If checks don't work, something failed and the board is not solvable
        if(not self.__check_all_row_col()):
            return False

        # If the board is still not solved, try the breadth first search
        if(self.board[self.board == NONE].size != 0):
            # Try the recursive method if all else fails
            try_colors = [RED, BLUE]

            point = np.argwhere(self.board == NONE)[0]
            x = point[0]
            y = point[1]
            for color in try_colors:
                if(self.__is_valid(x, y, color)):
                    board_copy = np.copy(self.board)
                    board_copy[x, y] = color
                    new_game = Solver(self.size, board_copy)
                    if(new_game.Solve()):
                        self.board = new_game.board
                        return True
            return False
        else:
            return True

    # Find needed color and if the board is still solvable
    def __check_adjacents(self, x, y):

        # Left
        if (y - 2 >= 0):
            if (self.board[x][y-1] == self.board[x][y-2] and
                    self.board[x][y-1] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x][y-1])
                                               )):
                    return False  # Not solvable

        # Right
        if (y + 2 < self.size):
            if (self.board[x][y+1] == self.board[x][y+2] and
                    self.board[x][y+1] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x][y+1])
                                               )):
                    return False  # Not solvable

        # Up
        if (x - 2 >= 0):
            if (self.board[x-1][y] == self.board[x-2][y] and
                    self.board[x-1][y] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x-1][y])
                                               )):
                    return False  # Not solvable

        # Down
        if (x + 2 < self.size):
            if (self.board[x+1][y] == self.board[x+2][y] and
                    self.board[x+1][y] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x+1][y])
                                               )):
                    return False  # Not solvable

        # Middle Vertical
        if (x + 1 < self.size and x - 1 >= 0):
            if (self.board[x+1][y] == self.board[x-1][y] and
                    self.board[x+1][y] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x+1][y])
                                               )):
                    return False  # Not solvable

        # Middle Horizontal
        if (y + 1 < self.size and y - 1 >= 0):
            if (self.board[x][y+1] == self.board[x][y-1] and
                    self.board[x][y-1] != NONE):
                if(not self.__assert_should_be(x, y,
                                               get_opposite(self.board[x][y-1])
                                               )):
                    return False  # Not solvable

        return True  # Still solvable

    # Check if there are three empty spaces in the rowcol
    def __has_three_in_row(self, rowcol):
        count = 0
        for i in range(rowcol.size):
            if(rowcol[i] == NONE):
                count = count + 1
                if(count >= 3):
                    return True
            else:
                count = 0

        return False

    # Check if the row/col is valid or has an obvious solution
    def __check_row_col(self, num, get):
        current = get(num)

        for color in [RED, BLUE]:
            colorcount = current[current == color].size
            if(colorcount == self.size / 2):
                if(self.__has_three_in_row(current)):
                    return False  # Impossible to complete row
                else:
                    current[current == NONE] = get_opposite(color)
            elif(colorcount > self.size / 2):
                return False  # Invalid rowcol

        # Check for duplicates
        nums = np.arange(current.size)
        nums = nums[nums != num]  # No point checking myself
        for n in nums:
            to_check = get(n)
            if(to_check[to_check == NONE].size == 0):
                # Only check full columns
                diff = to_check != current
                current_diff = current[diff]
                to_check_diff = to_check[diff]
                if(current_diff.size < 2):
                    return False  # It shouldn't be less than two at this point
                elif(current_diff.size == 2 and current_diff[0] == NONE and
                        current_diff[1] == NONE):
                    # Finish this one based off the diff
                    current_diff[0] = to_check_diff[1]
                    current_diff[1] = to_check_diff[0]

        return True

    def __check_all_row_col(self):
        def getCol(col): return self.board[:, col]
        def getRow(row): return self.board[row, :]

        for n in range(self.size):
            for func in [getCol(n), getRow(n)]:
                if(not self.__check_row_col(n, func)):
                    return False

        return True

    def __is_valid(self, x, y, color):

        # Left
        if (y - 2 >= 0):
            if (self.board[x][y-1] == self.board[x][y-2] and
                    self.board[x][y-1] == color):
                return False

        # Right
        if (y + 2 < self.size):
            if (self.board[x][y+1] == self.board[x][y+2] and
                    self.board[x][y+1] == color):
                return False

        # Up
        if (x - 2 >= 0):
            if (self.board[x-1][y] == self.board[x-2][y] and
                    self.board[x-1][y] == color):
                return False

        # Down
        if (x + 2 < self.size):
            if (self.board[x+1][y] == self.board[x+2][y] and
                    self.board[x+1][y] == color):
                return False

        # Middle Vertical
        if (x + 1 < self.size and x - 1 >= 0):
            if (self.board[x+1][y] == self.board[x-1][y] and
                    self.board[x+1][y] == color):
                return False

        # Middle Horizontal
        if (y + 1 < self.size and y - 1 >= 0):
            if (self.board[x][y+1] == self.board[x][y-1] and
                    self.board[x][y-1] == color):
                return False

        row = self.board[x, :]
        col = self.board[:, y]

        # Don't break max in row
        if(row[row == color].size >= self.size / 2 or
                col[col == color].size >= self.size / 2):
            return False

        for row_n in range(self.size):
            test_row = self.board[row_n, :]
            diff = test_row != row
            if(test_row[test_row == NONE].size == 0 and
                    test_row[diff].size == 1 and
                    test_row[diff][0] == color):
                return False

        for col_n in range(self.size):
            test_col = self.board[:, col_n]
            diff = test_col != col
            if(test_col[test_col == NONE].size == 0 and
                    test_col[diff].size == 1 and
                    test_col[diff][0] == color):
                return False

        # All checks passed
        return True

    def __assert_should_be(self, x, y, color):
        isColor = self.board[x, y]
        if(isColor == NONE):
            self.board[x, y] = color
        elif (isColor != color):
            return False  # Unable to complete the board

        return True

# End Class: Solver

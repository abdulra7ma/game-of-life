import copy
from random import randint

from graphics import GameOfLife


class Board(object):
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column
        self._main_board = self.generate_board(self.row, self.column)

    def generate_board(self, row: int, column: int) -> list:
        board = []

        for i in range(row):
            board.append([])
            for _ in range(column):
                rand_value = randint(
                    0, 2
                )  # 33% alive cell if the value is equal to 0
                if rand_value == 0:
                    board[i].append(1)
                else:
                    board[i].append(0)

        return board

    def draw_board(self, board: list) -> None:
        for row in board:
            for cell in row:
                print(cell, end=" ")
            print()

    def _get_neighbours_indexes(self, cell_pos: tuple) -> list:
        next = 1
        previous = -1

        n2 = (cell_pos[0] + previous, cell_pos[1])
        n4 = (cell_pos[0], cell_pos[1] + previous)
        n5 = (cell_pos[0], cell_pos[1] + next)
        n7 = (cell_pos[0] + next, cell_pos[1])

        n1 = (n2[0], n2[1] + previous)
        n3 = (n5[0] + previous, n5[1])
        n6 = (n4[0] + next, n4[1])
        n8 = (n7[0], n7[1] + next)

        indexes_list = [n1, n2, n3, n4, n5, n6, n7, n8]
        cells_indexes = []

        for c in indexes_list:
            if (c[0] <= (self.row - 1) and c[0] >= 0) and (
                c[1] <= (self.column - 1) and c[1] >= 0
            ):
                cells_indexes.append(c)
 
        return cells_indexes

    def _get_alive_neighbours_count(self, cell_pos: tuple) -> int:
        count = 0

        for c in self._get_neighbours_indexes(cell_pos):
            if self._main_board[c[0]][c[1]] == 1:
                count += 1
        return count

    def _is_alive(self, cell_pos: tuple, cells: list) -> True or False:
        if (
            self._get_alive_neighbours_count(cell_pos) in (2, 3)
            and cells[cell_pos[0]][cell_pos[1]] == 1
        ):
            return True
        return False

    def update_board(self) -> list:
        board = self.get_new_board

        for row in range(self.row):
            for col in range(self.column):
                cell = self.get_main_board[row][col]
                cell_pos = (row, col)

                if cell == 1:
                    if not self._is_alive(cell_pos, self._main_board):
                        board[cell_pos[0]][cell_pos[1]] = 0
                else:
                    if self._get_alive_neighbours_count(cell_pos) == 3:
                        board[cell_pos[0]][cell_pos[1]] = 1

        # update the main board
        self.update_main_board(board)

    def update_main_board(self, new_board) -> None:
        self._main_board = new_board

    @property
    def get_new_board(self):
        return copy.deepcopy(self.get_main_board)

    @property
    def get_main_board(self):
        return self._main_board

    def set_main_board(self, board):
        self._main_board = board

if __name__ == "__main__":
    row = int(input("Rows of the board: "))
    column = int(input("Columns of the board: "))

    board = Board(row, column)
    GameOfLife(board)
    
    

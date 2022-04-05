import copy
from random import randint, choice
from typing import List


SEED_COLORS = ["green", "yellow"]


class Chicken:
    """
    create a chicken related objects

    Logic of constructing a new chicken object:
        if status = 2 and gender = 1:
            this object is chicken female

        elif status = 2 and gender = 0:
            this object is chicken male

        else:
            this object is chicken chick
    """

    def __init__(self, status: int, gender: int) -> None:
        """
        status: indicates the chicken status
                if chick(status == 0) or chicken(status == 1)

        gender: indicates the chicken gender
                if gender == 0 than it's male chicken,
                if gender == 1 than it's female chicken.
        """

        self.status = status
        self.gender = gender

    @property
    def is_chick(self):
        return self.status == 1

    @property
    def is_chicken_male(self):
        return self.status == 2 and self.gender == 0

    @property
    def is_chicken_female(self):
        return self.status == 2 and self.gender == 1

    def __str__(self) -> str:
        return f"{self.status}"


class Seed:
    """
    if the seed color is green than any chicken objects can eat it
    else if the color is yellow than the only chickens that can it the seed are male or female chickens
    """

    def __init__(self, color) -> None:
        self.color = color if color in SEED_COLORS else "green"
        self.status = 3
        self.seed_colors = SEED_COLORS

    def is_eatable(self, chick_obj) -> bool:
        """
        checks if the given chicken object can eat this seed
        """
        return (chick_obj.status == 1 and self.color in self.seed_colors) or (
            chick_obj.status == 1 and self.color == "green"
        )

    def __str__(self) -> str:
        return f"{self.status}"


class Board(object):
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column
        self._main_board = self.generate_board()

        self.chick = 1
        self.chicken = 2

        self.male_chicken = (2, 0)
        self.female_chicken = (2, 1)

    def generate_board(self) -> list:
        board = []

        for i in range(self.row):
            board.append([])
            for _ in range(self.column):
                rand_status = randint(0, 3)
                rand_gender = randint(0, 1)

                if rand_status == 0:
                    board[i].append(Chicken(rand_status, rand_gender))
                elif rand_status == 1:
                    board[i].append(Chicken(rand_status, rand_gender))
                else:
                    board[i].append(Seed(choice(SEED_COLORS)))

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

    def _is_alive(self, cell_pos: tuple, cells: list) -> bool:
        if (
            self._get_alive_neighbours_count(cell_pos) in (2, 3)
            and cells[cell_pos[0]][cell_pos[1]] == 1
        ):
            return True
        return False

    def has_seed_neighbour(self, cell_indx: tuple) -> bool:
        """
        checks if one the `cell_indx` neighbours is a Seed object or not
        """
        for indx in self._get_neighbours_indexes(cell_indx):
            try:
                if self.get_main_board[indx[0]][indx[1]].status == 3:
                    return True
            except AttributeError:
                pass
        return False

    def get_seed_indx(self, cell_indx: tuple) -> tuple:
        """
        return the first seed neighbour object of given `cell_indx`
        """
        for indx in self._get_neighbours_indexes(cell_indx):
            try:
                if self.get_main_board[indx[0]][indx[1]].status == 3:
                    return indx
            except AttributeError:
                pass

    def eat_seed(
        self, chicken_cell_indx: tuple, seed_cell_indx: tuple, board
    ) -> None:
        cell = self._main_board[chicken_cell_indx[0]][chicken_cell_indx[1]]

        board[seed_cell_indx[0]][seed_cell_indx[1]] = cell
        board[chicken_cell_indx[0]][chicken_cell_indx[1]] = 0

    def update_board(self) -> list:
        board = self.get_new_board

        for row in range(self.row):
            for col in range(self.column):
                cell_pos = (row, col)
                cell = self.get_main_board[row][col]

                try:
                    if cell.status == self.chicken:
                        if self.has_seed_neighbour(cell_pos):
                            seed = self.get_seed_indx(cell_pos)
                            self.eat_seed(cell_pos, seed, board)
                    elif cell.status == self.chick:
                        if self.has_seed_neighbour(cell_pos):
                            seed = self.get_seed_indx(cell_pos)
                            if (
                                self.get_main_board[seed[0]][seed[1]].color
                                == "green"
                            ):
                                self.eat_seed(cell_pos, seed, board)
                except AttributeError:
                    pass

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
    from graphics import GameOfLife

    row = int(input("Rows of the board: "))
    column = int(input("Columns of the board: "))

    board = Board(row, column)
    GameOfLife(board)

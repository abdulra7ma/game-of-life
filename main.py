import copy
from random import randint, choice
from typing import List


SEED_COLORS = ["green", "yellow"]


class Chicken:
    """
    create a chicken related objects

    Logic of constructing a new chicken object:
        if status = 1:
            this object is chick
        if status = 2:
            this object is chicken

    """

    def __init__(self, status: int) -> None:
        """
        status: indicates the chicken status
                if chick(status == 0) or chicken(status == 1)
        """

        self.status = status
        self._eated_seeds = 0
        self._able_to_breed = False
        self._breed_times = 2

    def eat_seed(self):
        self._eated_seeds += 1

    @property
    def able_to_breed(self):
        if self.can_breed:
            self._able_to_breed = True
            return self._able_to_breed

        self._able_to_breed = False
        return self._able_to_breed

    @property
    def is_chick(self):
        return self.status == 1

    @property
    def is_chicken(self):
        return self.status == 2

    @property
    def can_breed(self):
        if self.is_chick:
            return False

        if (
            self._breed_times > 0
            and self.eated_seeds < 6
            and self.eated_seeds > 2
        ):
            return True

        return False

    @property
    def eated_seeds(self):
        return self._eated_seeds

    def has_breed(self):
        """
        decrease the number of time a cell can breed
        """
        self._breed_times -= 1

    def __str__(self) -> str:
        return f"{self.status}"


class Seed:
    """
    if the seed color is green than any chicken objects can eat it
    else if the color is yellow than the only chickens that can it
    the seed are male or female chickens
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

        self.EMPTY_CELL = 0
        self.CHICK = 1
        self.CHICKEN = 2
        self.SEED = 3

    def generate_board(self) -> list:
        board = []

        for i in range(self.row):
            board.append([])
            for _ in range(self.column):
                rand_status = randint(0, 5)  # 20% to spawn a chicken object
                seed_status = randint(1, 3)  # 33% to spawn a chicken object

                if seed_status == 3:
                    board[i].append(
                        Seed(choice(SEED_COLORS))
                    )  # append a seed cell
                elif rand_status == 2:
                    board[i].append(
                        Chicken(rand_status)
                    )  # append a chicken cell
                else:
                    board[i].append(0)  # append an empty cell

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
                if self.get_main_board[indx[0]][indx[1]].status == self.SEED:
                    return True
            except AttributeError:
                pass
        return False

    def is_seed_object(self, cell_index):
        return (
            True
            if self.get_main_board[cell_index[0]][cell_index[1]].status
            == self.SEED
            else False
        )

    def get_seed_indx(self, cell_indx: tuple) -> tuple:
        """
        return the first seed neighbour object of given `cell_indx`
        """
        for indx in self._get_neighbours_indexes(cell_indx):
            try:
                if self.is_seed_object(indx):
                    return indx
            except AttributeError:
                pass

    def eat_seed(
        self, chicken_cell_indx: tuple, seed_cell_indx: tuple, board
    ) -> None:
        cell = self.get_main_board[chicken_cell_indx[0]][chicken_cell_indx[1]]
        cell.eat_seed()

        board[chicken_cell_indx[0]][chicken_cell_indx[1]] = self.EMPTY_CELL
        board[seed_cell_indx[0]][seed_cell_indx[1]] = cell

    def update_board(self) -> list:
        board = self.get_new_board

        for row in range(self.row):
            for col in range(self.column):
                cell_pos = (row, col)
                cell = self.get_main_board[row][col]

                if hasattr(cell, "status"):
                    if isinstance(cell, Chicken):
                        if cell.status == self.CHICKEN:
                            if cell.eated_seeds >= 6:
                                # kill the chicken object
                                # if it eated more than 6 seeds
                                board[cell_pos[0]][
                                    cell_pos[1]
                                ] = self.EMPTY_CELL
                            else:
                                if self.has_seed_neighbour(cell_pos):
                                    seed = self.get_seed_indx(cell_pos)
                                    board[cell_pos[0]][
                                        cell_pos[1]
                                    ] = self.EMPTY_CELL
                                    board[seed[0]][seed[1]] = cell
                                    cell.eat_seed()

                                if cell.able_to_breed:
                                    # spawn new chicken chick
                                    if self.has_free_cells(cell_pos, board):
                                        # randomly choice a
                                        # cell to spawn the new chick
                                        new_chick_cell = choice(
                                            self.get_free_cells(
                                                cell_pos, board
                                            )
                                        )
                                        board[new_chick_cell[0]][
                                            new_chick_cell[1]
                                        ] = Chicken(status=self.CHICK)
                                        cell.has_breed()

                        elif cell.status == self.CHICK:
                            if cell.eated_seeds >= 3:
                                cell.status = self.CHICKEN

                                # restore the eated_seeds counter
                                cell._eated_seeds = 0

                                # replace the old cell with the new one
                                board[cell_pos[0]][cell_pos[1]] = cell
                            else:
                                if self.has_seed_neighbour(cell_pos):
                                    seed = self.get_seed_indx(cell_pos)
                                    if (
                                        self.get_main_board[seed[0]][
                                            seed[1]
                                        ].color
                                        == "green"
                                    ):
                                        board[cell_pos[0]][
                                            cell_pos[1]
                                        ] = self.EMPTY_CELL
                                        board[seed[0]][seed[1]] = cell
                                        cell.eat_seed()

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

    def has_free_cells(self, cell_pos, board) -> bool:
        """
        checks if one cell has free cells or not
        """
        cells = self._get_neighbours_indexes(cell_pos)
        return (
            True
            if len([cell for cell in cells if board[cell[0]][cell[1]] == 0])
            > 1
            else False
        )

    def get_free_cells(self, cell_pos, board) -> list:
        """
        Get all the free cells around one cell
        """
        return [
            cell
            for cell in self._get_neighbours_indexes(cell_pos)
            if board[cell[0]][cell[1]] == 0
        ]


if __name__ == "__main__":
    from graphics import GameOfLife

    row = int(input("Rows of the board: "))
    column = int(input("Columns of the board: "))

    board = Board(column, row)
    GameOfLife(board)

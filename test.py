from random import randint
import copy


def generate_board(row: int, column: int) -> list:
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


def draw_board(cells_array: list) -> None:
    for row in cells_array:
        for cell in row:
            print(cell, end=" ")
        print()


def get_neighbours_indexes(cell_pos: tuple, cells):
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
        if (c[0] <= (row - 1) and c[0] >= 0) and (
            c[1] <= (column - 1) and c[1] >= 0
        ):
            cells_indexes.append(c)

    return cells_indexes


def get_alive_neighbours_count(cell_pos: tuple, cells: list) -> int:
    count = 0

    for c in get_neighbours_indexes(cell_pos, cells):
        if cells[c[0]][c[1]] == 1:
            count += 1
    return count


def is_alive(cell_pos: tuple, cells: list) -> True or False:
    if (
        get_alive_neighbours_count(cell_pos, cells) in (2, 3)
        and cells[cell_pos[0]][cell_pos[1]] == 1
    ):
        return True
    return False


def update_board(cell: int, cell_pos: tuple, og_cells, cells: list) -> list:
    if cell == 1:
        if not is_alive(cell_pos, og_cells):
            cells[cell_pos[0]][cell_pos[1]] = 0
    else:
        if get_alive_neighbours_count(cell_pos, og_cells, up=True) == 3:
            cells[cell_pos[0]][cell_pos[1]] = 1


if __name__ == "__main__":
    row = int(input())
    column = int(input())

    # r1 = [int(num) for num in input().split()]
    # r2 = [int(num) for num in input().split()]
    # r3 = [int(num) for num in input().split()]

    main_cells = generate_board(row, column)

    print("First Board")
    draw_board(main_cells)

    cells = copy.deepcopy(main_cells)

    for i in range(row):
        for j in range(column):
            cell_indx = (i, j)
            cell = main_cells[cell_indx[0]][cell_indx[1]]

            if cell == 1:
                if not is_alive(cell_indx, main_cells):
                    cells[cell_indx[0]][cell_indx[1]] = 0
            else:
                if get_alive_neighbours_count(cell_indx, main_cells) == 3:
                    cells[cell_indx[0]][cell_indx[1]] = 1

    print("\nSecond Board")
    draw_board(cells)
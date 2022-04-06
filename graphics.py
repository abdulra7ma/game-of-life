import tkinter
from main import Chicken, Seed, Board
from PIL import Image, ImageTk


class GameOfLife:
    def __init__(self, board: Board):
        self.parent = tkinter.Tk()
        self.board = board
        self.CELL_WIDTH = 40
        self.CELL_HIEGHT = 42

        self.initailizeGUI()

    def initailizeGUI(self):
        """
        initiate the main elements on tkinter GUI

        Variables:
            canvas: where we draw the cells of the game
            restart_button: button to restart the game with a
                            new board of random cells
        """
        self.canvas = tkinter.Canvas(
            self.parent,
            width=self.CELL_WIDTH * self.board.row,
            height=self.CELL_HIEGHT * self.board.column,
        )
        self.canvas.pack()

        # draw the first generate cells
        self.draw_board(self.board.get_main_board)

        # next_button = tkinter.Button(
        #     self.parent, text="next board", command=lambda: self.update_board()
        # )
        # next_button.pack()

        restart_button = tkinter.Button(
            self.parent, text="reset the game", command=lambda: self.rest()
        )
        restart_button.pack()

        # excutes the `loop` function after
        # one second of starting the GUI
        self.parent.after(1000, self.loop)

        self.run()

    def draw_board(self, board):
        """
        draw the given board on the canvas
        """

        for i in range(self.board.row):
            for j in range(self.board.column):

                cell = board[i][j]

                if cell.__class__.__name__ == Chicken.__name__:
                    if cell.status == 2:
                        self.draw_rectangle(
                            i,
                            j,
                            "pink",  # chickens color
                        )
                    else:
                        self.draw_rectangle(i, j, "blue")  # chicks color

                elif cell.__class__.__name__ == Seed.__name__:
                    if cell.color == "green":
                        self.draw_rectangle(i, j, "green")
                    else:
                        self.draw_rectangle(i, j, "yellow")
                else:
                    self.draw_rectangle(i, j, "brown")

    def draw_rectangle(self, i, j, color):
        x = self.CELL_WIDTH
        y = self.CELL_HIEGHT

        self.canvas.create_rectangle(
            i * x,
            j * x,
            i * x + y,
            j * x + y,
            fill=color,
        )

    def draw_image(self, i, j, img):
        x = self.CELL_WIDTH
        y = self.CELL_HIEGHT

        self.canvas.create_image(i * x, j * y, image=img)

    def update_board(self):
        self.board.update_board()
        self.draw_board(self.board.get_main_board)

    def loop(self):
        self.update_board()
        self.parent.after(1000, self.loop)

    def rest(self):
        """
        Reset the cells board and initiate a new board of random cells
        """

        board = self.board.generate_board()
        self.draw_board(board)
        self.board.set_main_board(board)
        self.update_board()
        self.parent.after(2000, self.loop)

    def run(self):
        """Go into the Tk main processing loop."""

        self.parent.mainloop()

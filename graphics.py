import time
import tkinter


class GameOfLife:
    def __init__(self, board):
        self.parent: tkinter.TK = tkinter.Tk()
        self.board = board

        self.initailizeGUI()

    def initailizeGUI(self):
        self.canvas = tkinter.Canvas(
            self.parent,
            width=1080,
            height=540,
        )
        self.canvas.pack()

        self.draw_board(self.board.get_main_board)

        # restart butten
        restart_button = tkinter.Button(
            self.parent, text="reset the game", command=lambda: self.rest()
        )
        restart_button.pack()

        self.parent.after(1000, self.loop)

        self.run()

    def draw_board(self, board):
        x = 7.5
        y = 6.5
        for i in range(self.board.row):
            for j in range(self.board.column):
                if board[i][j] == 1:
                    self.canvas.create_rectangle(
                        i * x,
                        j * x,
                        i * x + y,
                        j * x + y,
                        fill="chartreuse2",
                    )
                else:
                    self.canvas.create_rectangle(
                        i * x,
                        j * x,
                        i * x + y,
                        j * x + y,
                        fill="brown4",
                    )

    def update_board(self):
        self.board.update_board()
        self.draw_board(self.board.get_main_board)

    def loop(self):
        self.update_board()
        self.parent.after(1000, self.loop)

    def rest(self):
        board = self.board.generate_board(self.board.row, self.board.column)
        self.draw_board(board)
        self.board.set_main_board(board)
        self.update_board()
        self.parent.after(2000, self.loop)

    def run(self):
        """Go into the Tk main processing loop."""
        self.parent.mainloop()

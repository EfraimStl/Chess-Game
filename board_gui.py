from tkinter import *
import pygame


class BoardGui:
    def __init__(self, game_logic):
        self.root = Tk()
        self.root.configure(bg="#444941", pady=10, padx=50)
        self.root.title("Chess")
        self.root.resizable(width=False, height=False)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = (screen_width - self.root.winfo_reqwidth())

        # Set the window size to match the screen size
        self.root.geometry(f"+{window_width // 4}+{0}")

        self.first_click = None
        self.second_click = None

        self.game_logic = game_logic

        self.wp_image = PhotoImage(file="images/chess_pieces_images/white_pawn.png")
        self.wb_image = PhotoImage(file="images/chess_pieces_images/white_bishop.png")
        self.wn_image = PhotoImage(file="images/chess_pieces_images/white_knight.png")
        self.wr_image = PhotoImage(file="images/chess_pieces_images/white_rook.png")
        self.wk_image = PhotoImage(file="images/chess_pieces_images/white_king.png")
        self.wq_image = PhotoImage(file="images/chess_pieces_images/white_queen.png")

        self.bp_image = PhotoImage(file="images/chess_pieces_images/black_pawn.png")
        self.bb_image = PhotoImage(file="images/chess_pieces_images/black_bishop.png")
        self.bn_image = PhotoImage(file="images/chess_pieces_images/black_knight.png")
        self.br_image = PhotoImage(file="images/chess_pieces_images/black_rook.png")
        self.bk_image = PhotoImage(file="images/chess_pieces_images/black_king.png")
        self.bq_image = PhotoImage(file="images/chess_pieces_images/black_queen.png")

        self.empty_image = PhotoImage(file="images/transparent.png")

        self.promote_select = None

        self.button_matrix = [[None for _ in range(8)] for _ in range(8)]

        self.board_setup()

    def board_setup(self):

        button_size = 70
        chessboard = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]

        for row in range(8):
            for col in range(8):
                # Alternate colors
                fill_color = "#D5EEBB" if (row + col) % 2 == 0 else "#5F7A61"
                piece_code = chessboard[row][col]
                image = getattr(self, f"{piece_code}_image", self.empty_image)

                # Create Button for each square
                square_button = Button(
                    self.root,
                    image=image,
                    text=" ",
                    width=button_size,
                    height=button_size,
                    bg=fill_color,
                    activebackground="#444941",
                    compound="center",
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                self.button_matrix[row][col] = square_button
                # Grid the button
                square_button.grid(row=row, column=col)

    def update_board(self, from_row, from_col, to_row, to_col):
        from_button = self.button_matrix[from_row][from_col]
        to_button = self.button_matrix[to_row][to_col]

        to_button.configure(image=from_button.cget("image"))
        from_button.configure(image=self.empty_image)

    def board_promote(self):
        window = Toplevel(self.root)
        var = StringVar(window, "Queen")
        values = ["Queen", "Rook", "Bishop", "Knight"]

        def set_result(value):
            self.promote_select = value
            window.destroy()

        for value in values:
            Radiobutton(window, text=value, variable=var, value=value, indicatoron=False, bg="#7FC8A9") \
                .pack(fill=X, ipady=5)
        Button(window, text="Submit", command=lambda: set_result(var.get())).pack(fill=X, ipady=7)
        window.mainloop()

    def on_square_click(self, row, col):
        import game_over
        if self.first_click is None and self.game_logic.back_chess_board[row][col] is not None:
            self.first_click = (row, col)
        elif self.first_click is not None:
            self.second_click = (row, col)

            castling, rook, move_rook = self.game_logic.castling(self.first_click, self.second_click)
            en_passant = self.game_logic.en_passant(self.first_click, self.second_click)

            if en_passant:
                print("en passant")
                self.game_logic.move(self.first_click, self.second_click)
                self.game_logic.whose_turn()
                self.play_sound()
                self.update_board(self.first_click[0], self.first_click[1], self.second_click[0], self.second_click[1])
                self.button_matrix[self.first_click[0]][self.second_click[1]].configure(image=self.empty_image)


            if castling:
                print("castle")
                self.game_logic.move(self.first_click, self.second_click)
                self.game_logic.move(rook, move_rook)
                self.game_logic.whose_turn()
                self.play_sound()
                self.update_board(self.first_click[0], self.first_click[1], self.second_click[0], self.second_click[1])
                self.update_board(rook[0], rook[1], move_rook[0], move_rook[1])


            if self.game_logic.check_move(self.first_click, self.second_click):
                # Move the piece in the game logic if it doesn't cause a check
                if not self.game_logic.is_self_check(self.first_click, self.second_click):

                    self.game_logic.move(self.first_click, self.second_click)
                    self.play_sound()

                    # switch turn between players
                    self.game_logic.whose_turn()

                    # check if checkmate or stalemate
                    checkmate = self.game_logic.is_checkmate_or_stalemate()


                    # Update the GUI board
                    self.update_board(self.first_click[0], self.first_click[1], self.second_click[0], self.second_click[1])

                    if checkmate and checkmate[1] != "stalemate":
                        color = checkmate[1]
                        self.root.destroy()
                        game_over.GameOver(color)
                    elif checkmate:
                        color = "stalemate"
                        self.root.destroy()
                        game_over.GameOver(color)

            self.first_click = None
            self.second_click = None

        print(f"Square clicked: Row {row}, Column {col}")

    @staticmethod
    def play_sound():
        pygame.mixer.init()
        pygame.mixer.music.load("./images/sound.wav")
        pygame.mixer.music.play()

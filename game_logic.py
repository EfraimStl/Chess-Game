import copy

from pieces import Pawn, Bishop, Knight, Rook, King, Queen
from util import is_occupied_by_same_color, is_path_clear


class GameLogic:
    def __init__(self):
        self.back_chess_board = [
            [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"),
             Knight("black"), Rook("black")],
            [Pawn("black") for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn("white") for _ in range(8)],
            [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"),
             Knight("white"), Rook("white")]
        ]
        self.turn = "white"

    def check_move(self, first_click, second_click):
        from_row, from_col = first_click
        to_row, to_col = second_click
        if hasattr(self.back_chess_board[from_row][from_col], "color") and self.back_chess_board[from_row][
            from_col].color == self.turn:
            if self.back_chess_board[from_row][from_col] is not None:
                if not is_occupied_by_same_color(first_click, second_click, self.back_chess_board):
                    if self.back_chess_board[from_row][from_col].is_legal_move(first_click, second_click,
                                                                               self.back_chess_board):
                        if is_path_clear(first_click, second_click, self.back_chess_board):
                            return "alright"

    def move(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.back_chess_board[from_row][from_col]

        # if object has attribute of first turn (pawn, king, rook) make it false
        if hasattr(piece, 'first_turn'):
            piece.first_turn = False

        # move object from source square to destination
        self.back_chess_board[from_row][from_col] = None
        self.back_chess_board[to_row][to_col] = piece


    def is_valid_move(self, from_square, to_square):
        pass

    def castling(self):
        # If it's rook and king first turn, should be able to castle
        pass

    def whose_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def is_check(self):
        # should check if there is a clear path to the opponent's king
        opponent_king_position = None
        # find the opponent's king position
        for row in range(8):
            for col in range(8):
                if type(self.back_chess_board[row][col]) == King and self.back_chess_board[row][col].color != self.turn:
                    opponent_king_position = (row, col)
                    print(f"{self.back_chess_board[row][col].color} king position is {opponent_king_position}")

        # Checking if opponent's king is threatened
        for row in range(8):
            for col in range(8):
                if self.check_move((row, col), opponent_king_position) == "alright":
                    print("check")
                    return True

        return False
    # opponent_color = "black" if self.turn == "white" else "white"
    # opponent_king_position = next(((row, col) for row in range(8) for col in range(8) if
    #                                isinstance(self.back_chess_board[row][col], King) and
    #                                self.back_chess_board[row][col].color == opponent_color), None)
    # return opponent_king_position is not None and any(
    #     self.threatens_king((row, col), opponent_king_position) for row in range(8) for col in range(8))

    def is_self_check(self, from_square, to_square):
        temp_game = copy.deepcopy(self)
        temp_game.move(from_square, to_square)
        return temp_game.is_check()

    def is_checkmate(self):
        # If is_check, function should check if there is a way to block it (by moving the king or other piece)
        pass

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
        self.potential_en_passant = None

    def check_move(self, first_click, second_click):
        from_row, from_col = first_click
        # to_row, to_col = second_click
        if hasattr(self.back_chess_board[from_row][from_col], "color") and self.back_chess_board[from_row][
            from_col].color == self.turn:
            if self.back_chess_board[from_row][from_col] is not None:
                if not is_occupied_by_same_color(first_click, second_click, self.back_chess_board):
                    if self.back_chess_board[from_row][from_col].is_legal_move(first_click, second_click,
                                                                               self.back_chess_board):
                        if is_path_clear(first_click, second_click, self.back_chess_board):
                            return True
        return False

    def move(self, from_square, to_square):
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square
            piece = self.back_chess_board[from_row][from_col]

            # if object has attribute of first turn (pawn, king, rook) make it false
            if hasattr(piece, 'first_turn') and piece.first_turn:
                piece.first_turn = False
                if isinstance(self.back_chess_board[from_row][from_col], Pawn) and abs(from_row - to_row) == 2:
                    self.potential_en_passant = to_square

            # move object from source square to destination
            self.back_chess_board[from_row][from_col] = None
            self.back_chess_board[to_row][to_col] = piece

    def castling(self, from_square, to_square):
        # If it's rook and king first turn, should be able to castle
        from_row, from_col = from_square
        to_row, to_col = to_square

        king = from_square
        rook = None
        move_rook = None

        temp_board = copy.deepcopy(self)
        temp_board.whose_turn()

        if isinstance(self.back_chess_board[from_row][from_col], King)\
                and self.back_chess_board[from_row][from_col].first_turn\
                and not temp_board.is_check():
            # black castle
            # short castle
            if isinstance(self.back_chess_board[0][7], Rook) and to_square == (0, 6)\
                    and self.back_chess_board[0][7].first_turn\
                    and all(self.back_chess_board[0][col] is None for col in [5, 6])\
                    and not any(self.is_self_check(king, (0, col)) for col in [5, 6]):
                rook = (0, 7)
                move_rook = (0, 5)
                return True, rook, move_rook
            # long castle
            elif isinstance(self.back_chess_board[0][0], Rook) and to_square == (0, 2) \
                    and self.back_chess_board[0][0].first_turn \
                    and all(self.back_chess_board[0][col] is None for col in [2, 3])\
                    and not any(self.is_self_check(king, (0, col)) for col in [2, 3]):

                rook = (0, 0)
                move_rook = (0, 3)
                return True, rook, move_rook
            # white castle
            # long castle
            elif isinstance(self.back_chess_board[7][0], Rook) and to_square == (7, 2) \
                    and self.back_chess_board[7][0].first_turn\
                    and all(self.back_chess_board[7][col] is None for col in [2, 3]) \
                    and not any(self.is_self_check(king, (7, col)) for col in [2, 3]):

                rook = (7, 0)
                move_rook = (7, 3)
                return True, rook, move_rook
            # short castle
            elif isinstance(self.back_chess_board[7][7], Rook) and to_square == (7, 6) \
                    and  self.back_chess_board[7][7].first_turn\
                    and all(self.back_chess_board[7][col] is None for col in [5, 6]) \
                    and not any(self.is_self_check(king, (7, col)) for col in [5, 6]):

                rook = (7, 7)
                move_rook = (7, 5)
                return True, rook, move_rook

        del temp_board
        return False, rook, move_rook

    def whose_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def kings_position(self):
        opponent_king_position = None
        self_king_position = None

        for row in range(8):
            for col in range(8):
                if type(self.back_chess_board[row][col]) == King:
                    if self.back_chess_board[row][col].color != self.turn:
                        opponent_king_position = (row, col)
                        print(f"{self.back_chess_board[row][col].color} king position is {opponent_king_position}")
                    else:
                        self_king_position = (row, col)
                        print(f"{self.back_chess_board[row][col].color} king position is {self_king_position}")

        return self_king_position, opponent_king_position

    def is_check(self):
        # should check if there is a clear path to the opponent's king
        opponent_king_position = self.kings_position()[1]
        print(opponent_king_position)

        # Checking if opponent's king is threatened
        for row in range(8):
            for col in range(8):
                if self.check_move((row, col), opponent_king_position):
                    print("check")
                    return True

        return False

    def is_self_check(self, from_square, to_square):
        temp_game = copy.deepcopy(self)
        temp_game.move(from_square, to_square)
        temp_game.whose_turn()
        return temp_game.is_check()

    def is_checkmate_or_stalemate(self):
        # Checks if there is a valid move, on there is no legal move the method checks if it is a check.
        # If there is a check this is a checkmate, else this is a stalemate.
        for row in range(8):
            for col in range(8):
                piece_position = (row, col)
                for row_2 in range(8):
                    for col_2 in range(8):
                        destination = (row_2, col_2)
                        if self.check_move(piece_position, destination):
                            if self.is_self_check(piece_position, destination) is False:
                                print(f"not checkmate {piece_position}{destination}")
                                return False
        # if no valid move founds, check if it is a checkmate or a stalemate
        copy_for_test = copy.deepcopy(self)
        copy_for_test.whose_turn()
        if not copy_for_test.is_check():
            print("stalemate")
            return True, "stalemate"

        print("checkmate")
        return True, copy_for_test.turn

    def promoting(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        promote_row = 8 if self.turn == "white" else 0

        if isinstance(self.back_chess_board[from_row][from_col], Pawn) and to_row == promote_row:
            pass

    def en_passant(self, from_square, to_square):
        from pieces import Pawn
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if isinstance(self.back_chess_board[from_row][from_col], Pawn) and self.potential_en_passant is not None \
                    and abs(from_col - self.potential_en_passant[1]) == 1 and to_col == self.potential_en_passant[1]:
                if self.back_chess_board[from_row][from_col].color == "black" and from_row == 4:
                    self.potential_en_passant = None
                    self.back_chess_board[from_row][to_col] = None
                    return True
                elif self.back_chess_board[from_row][from_col].color == "white" and from_row == 3:
                    self.potential_en_passant = None
                    self.back_chess_board[from_row][to_col] = None
                    return True
        return False

    def is_tie(self):
        count = 0


import copy

from pieces import Pawn, Bishop, Knight, Rook, King, Queen
from util import is_occupied_by_same_color, is_path_clear


class GameLogic:
    def __init__(self):
        """
        Class for the logic of the game
        """
        self.back_chessboard = [
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
        """
        Checks if move from source to destination is a valid move
        Args:
            first_click - a tuple
            second_click - a tuple
         Returns:
            bool: True if the move is valid, False otherwise
        """
        from_row, from_col = first_click
        # to_row, to_col = second_click
        if hasattr(self.back_chessboard[from_row][from_col], "color") and self.back_chessboard[from_row][
            from_col].color == self.turn:
            if self.back_chessboard[from_row][from_col] is not None:
                if not is_occupied_by_same_color(first_click, second_click, self.back_chessboard):
                    if self.back_chessboard[from_row][from_col].is_legal_move(first_click, second_click,
                                                                              self.back_chessboard):
                        if is_path_clear(first_click, second_click, self.back_chessboard):
                            return True
        return False

    def move(self, from_square, to_square):
        """
        Makes the move of the object from source to destination
        Args:
            from_square - a tuple
            to_square - a tuple
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square
            piece = self.back_chessboard[from_row][from_col]

            # if object has attribute of first turn (pawn, king, rook) make it false
            if hasattr(piece, 'first_turn') and piece.first_turn:
                piece.first_turn = False
                if isinstance(self.back_chessboard[from_row][from_col], Pawn) and abs(from_row - to_row) == 2:
                    self.potential_en_passant = to_square

            # move object from source square to destination
            self.back_chessboard[from_row][from_col] = None
            self.back_chessboard[to_row][to_col] = piece

    def castling(self, from_square, to_square):
        """
        If it's rook's and king's first turn, should be able to castle
        Args:
            from_square - a tuple
            to_square - a tuple
        Returns:
            tuple:
                bool: True if castling is a valid move
                tuple: Rook source
                tuple: Rook destination
        """
        from_row, from_col = from_square
        to_row, to_col = to_square

        king = from_square
        rook = None
        move_rook = None

        temp_board = copy.deepcopy(self)
        temp_board.whose_turn()

        if isinstance(self.back_chessboard[from_row][from_col], King)\
                and self.back_chessboard[from_row][from_col].first_turn\
                and not temp_board.is_check():
            # black castle
            # short castle
            if isinstance(self.back_chessboard[0][7], Rook) and to_square == (0, 6)\
                    and self.back_chessboard[0][7].first_turn\
                    and all(self.back_chessboard[0][col] is None for col in [5, 6])\
                    and not any(self.is_self_check(king, (0, col)) for col in [5, 6]):
                rook = (0, 7)
                move_rook = (0, 5)
                return True, rook, move_rook
            # long castle
            elif isinstance(self.back_chessboard[0][0], Rook) and to_square == (0, 2) \
                    and self.back_chessboard[0][0].first_turn \
                    and all(self.back_chessboard[0][col] is None for col in [2, 3])\
                    and not any(self.is_self_check(king, (0, col)) for col in [2, 3]):

                rook = (0, 0)
                move_rook = (0, 3)
                return True, rook, move_rook
            # white castle
            # long castle
            elif isinstance(self.back_chessboard[7][0], Rook) and to_square == (7, 2) \
                    and self.back_chessboard[7][0].first_turn\
                    and all(self.back_chessboard[7][col] is None for col in [2, 3]) \
                    and not any(self.is_self_check(king, (7, col)) for col in [2, 3]):

                rook = (7, 0)
                move_rook = (7, 3)
                return True, rook, move_rook
            # short castle
            elif isinstance(self.back_chessboard[7][7], Rook) and to_square == (7, 6) \
                    and  self.back_chessboard[7][7].first_turn\
                    and all(self.back_chessboard[7][col] is None for col in [5, 6]) \
                    and not any(self.is_self_check(king, (7, col)) for col in [5, 6]):

                rook = (7, 7)
                move_rook = (7, 5)
                return True, rook, move_rook

        return False, rook, move_rook

    def whose_turn(self):
        """
        Switch turns between black and white
        """
        self.turn = "black" if self.turn == "white" else "white"

    def kings_position(self):
        """
        Track the kings position
        Returns:
            tuple:
                tuple: Position of players' king
                tuple: Position of opponents' king
        """
        opponent_king_position = None
        self_king_position = None

        for row in range(8):
            for col in range(8):
                if type(self.back_chessboard[row][col]) == King:
                    if self.back_chessboard[row][col].color != self.turn:
                        opponent_king_position = (row, col)
                    else:
                        self_king_position = (row, col)

        return self_king_position, opponent_king_position

    def is_check(self):
        """
        Checks if there is a clear path to the opponent's king
        Returns:
            bool: True if it is a check
        """
        opponent_king_position = self.kings_position()[1]

        # Checking if opponent's king is threatened
        for row in range(8):
            for col in range(8):
                if self.check_move((row, col), opponent_king_position):
                    return True
        return False

    def is_self_check(self, from_square, to_square):
        """
        Checks if a move will block or prevent the check on the player's king
        Returns:
            bool: True if the move does not prevent or block the check
        """
        temp_game = copy.deepcopy(self)
        temp_game.move(from_square, to_square)
        temp_game.whose_turn()
        return temp_game.is_check()

    def is_checkmate_or_stalemate(self):
        """
        If there is no valid move the method checks if there is a checkmate or a stalemate
        Returns:
            tuple:
                bool: True if it is checkmate or stalemate
                string: the word "stalemate" if it is stalemate, else the winner's color
        """
        for row in range(8):
            for col in range(8):
                piece_position = (row, col)
                for row_2 in range(8):
                    for col_2 in range(8):
                        destination = (row_2, col_2)
                        if self.check_move(piece_position, destination):
                            if self.is_self_check(piece_position, destination) is False:
                                return False
        # if no valid move founds, check if it is a checkmate or a stalemate
        copy_for_test = copy.deepcopy(self)
        copy_for_test.whose_turn()
        if not copy_for_test.is_check():
            print("stalemate")
            return True, "stalemate"

        print("checkmate")
        return True, copy_for_test.turn

    def en_passant(self, from_square, to_square):
        """
        Checks if there is a legal en passant move
        Args:
            from_square - a tuple
            to_square - a tuple
        Returns:
            bool: True if the move is "en passant" move
        """
        from pieces import Pawn
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if isinstance(self.back_chessboard[from_row][from_col], Pawn) and self.potential_en_passant is not None \
                    and abs(from_col - self.potential_en_passant[1]) == 1 and to_col == self.potential_en_passant[1]:
                if (self.back_chessboard[from_row][from_col].color == "black" and from_row == 4)\
                        or (self.back_chessboard[from_row][from_col].color == "white" and from_row == 3):
                    self.potential_en_passant = None
                    self.back_chessboard[from_row][to_col] = None
                    return True
        return False


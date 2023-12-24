from util import is_eating


class Pawn:
    def __init__(self, color):
        """
        Class for pawn pieces
        Args:
            color - a string
        """
        self.color = color
        self.first_turn = True
        self.potential_en_passant = None

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal pawn move
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if is_eating(from_square, to_square, board):
                if from_col == to_col:
                    return False
            else:
                if from_col != to_col:
                    return False
            # self.potential_en_passant = None
            if self.first_turn:
                if self.color == "black":
                    if -2 <= from_row - to_row < 0:
                        return True
                elif 0 < from_row - to_row <= 2:
                    return True
                return False
            else:
                if self.color == "black":
                    if from_row - to_row == -1:
                        return True
                elif from_row - to_row == 1:
                    return True
        return False


class Rook:
    def __init__(self, color):
        """
        Class for rook pieces
        Args:
            color - a string
        """
        self.color = color
        self.first_turn = True

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal rook move
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if from_row == to_row or from_col == to_col:
                return True
        return False


class Bishop:
    def __init__(self, color):
        """
        Class for bishop pieces
        Args:
            color - a string
        """
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal bishop move
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        if from_square is not None and to_square is not None:
            form_row, from_col = from_square
            to_row, to_col = to_square

            if abs(form_row - to_row) == abs(from_col - to_col):
                return True
        return False


class Knight:
    def __init__(self, color):
        """
        Class for knight pieces
        Args:
            color - a string
        """
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal knight move
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if (abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2) or (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1):
                return True
        return False


class Queen:
    def __init__(self, color):
        """
        Class for queen pieces
        Args:
            color - a string
        """
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal queen move
        (due to is_path_clear in util it cna always return True)
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        return True


class King:
    def __init__(self, color):
        """
        Class for king pieces
        Args:
            color - a string
        """
        self.color = color
        self.first_turn = True

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal king move
        Args:
            from_square - a tuple
            to_square - a tuple
            board - two-dimensional list
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
                return True

        return False



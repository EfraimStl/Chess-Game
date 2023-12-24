from util import is_eating


class Pawn:
    """
    Class for pawn pieces
    """
    def __init__(self, color):
        self.color = color
        self.first_turn = True
        self.potential_en_passant = None

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal pawn move
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
    """
    Class for rook pieces
    """
    def __init__(self, color):
        self.color = color
        self.first_turn = True

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal rook move
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if from_row == to_row or from_col == to_col:
                return True
        return False


class Bishop:
    """
    Class for bishop pieces
    """
    def __init__(self, color):
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal bishop move
        """
        if from_square is not None and to_square is not None:
            form_row, from_col = from_square
            to_row, to_col = to_square

            if abs(form_row - to_row) == abs(from_col - to_col):
                return True
        return False


class Knight:
    """
    Class for knight pieces
    """
    def __init__(self, color):
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal knight move
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if (abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2) or (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1):
                return True
        return False


class Queen:
    """
    Class for queen pieces
    """
    def __init__(self, color):
        self.color = color

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal queen move
        (due to is_path_clear in util it cna always return True)
        """
        return True


class King:
    """
    Class for king pieces
    """
    def __init__(self, color):
        self.color = color
        self.first_turn = True

    def is_legal_move(self, from_square, to_square, board):
        """
        Checks if move is a legal king move
        """
        if from_square is not None and to_square is not None:
            from_row, from_col = from_square
            to_row, to_col = to_square

            if abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
                return True

        return False



def is_occupied_by_same_color(from_square, to_square, board):
    """
    Implement checks for whether the destination square is occupied by a piece of the same color
    """
    if from_square is not None and to_square is not None:
        from_row, from_col = from_square
        to_row, to_col = to_square
        if board[to_row][to_col] is not None and board[from_row][from_col].color == \
                board[to_row][to_col].color:
            return True
    return False


def is_path_clear(from_square, to_square, board):
    """
    Checks if path from source to destination is clear
    """
    from pieces import Knight
    if from_square is not None and to_square is not None:
        from_row, from_col = from_square
        to_row, to_col = to_square

        # knight does not have to have a clear path
        if type(board[from_row][from_col]) == Knight:
            return True

        # piece can only move vertically, horizontally or diagonally
        if from_row == to_row or from_col == to_col or abs(from_row - to_row) == abs(from_col - to_col):
            step_row = 0 if from_row == to_row else 1 if from_row < to_row else -1
            step_col = 0 if from_col == to_col else 1 if from_col < to_col else -1

            # current square
            current_row, current_col = from_row + step_row, from_col + step_col

            # while not in destination check if it gets occupied be a piece
            while current_row != to_row or current_col != to_col:
                if board[current_row][current_col] is not None:
                    return False
                current_row += step_row
                current_col += step_col
            return True
    return False


def is_eating(from_square, to_square, board):
    """
    Checks if the move is an eating move
    """
    if from_square is not None and to_square is not None:
        from_row, from_col = from_square
        to_row, to_col = to_square
        if board[to_row][to_col] is not None:
            if board[to_row][to_col].color != board[from_row][from_col]:
                return True
    return False

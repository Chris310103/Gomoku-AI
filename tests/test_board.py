from gomoku_ai.common.board import (
    BLACK,
    WHITE,
    can_win_points,
    five_in_a_row,
    legal_moves,
    opponent,
)


def empty_board(size: int = 15):
    return [[0 for _ in range(size)] for _ in range(size)]


def test_opponent():
    assert opponent(BLACK) == WHITE
    assert opponent(WHITE) == BLACK


def test_horizontal_five_in_a_row():
    board = empty_board()

    for col in range(3, 8):
        board[7][col] = BLACK

    assert five_in_a_row(board, 7, 5, BLACK)


def test_vertical_five_in_a_row():
    board = empty_board()

    for row in range(2, 7):
        board[row][8] = WHITE

    assert five_in_a_row(board, 4, 8, WHITE)


def test_only_four_is_not_a_win():
    board = empty_board()

    for col in range(3, 7):
        board[7][col] = BLACK

    assert not five_in_a_row(board, 7, 5, BLACK)


def test_empty_board_returns_center_move():
    board = empty_board()

    assert legal_moves(board) == [(7, 7)]


def test_legal_moves_do_not_include_occupied_position():
    board = empty_board()
    board[7][7] = BLACK

    moves = legal_moves(board, radius=1)

    assert (7, 7) not in moves
    assert len(moves) == 8


def test_can_win_points_finds_both_ends():
    board = empty_board()

    for col in range(4, 8):
        board[7][col] = BLACK

    winning_moves = set(can_win_points(board, BLACK))

    assert winning_moves == {(7, 3), (7, 8)}
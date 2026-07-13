from gomoku_ai.common.board import BLACK, WHITE, legal_moves
from gomoku_ai.search.heuristics import heuristic, line_score, order_moves


def empty_board(size: int = 15):
    return [[0 for _ in range(size)] for _ in range(size)]


def test_five_has_very_high_score():
    score = line_score([BLACK, BLACK, BLACK, BLACK, BLACK], BLACK)

    assert score >= 1_000_000


def test_open_four_is_stronger_than_open_three():
    open_four_score = line_score(
        [0, BLACK, BLACK, BLACK, BLACK, 0],
        BLACK,
    )
    open_three_score = line_score(
        [0, BLACK, BLACK, BLACK, 0],
        BLACK,
    )

    assert open_four_score > open_three_score


def test_opponent_stone_breaks_pattern():
    score = line_score(
        [WHITE, BLACK, BLACK, BLACK, 0],
        BLACK,
    )

    assert score == 0


def test_heuristic_is_positive_for_advantaged_player():
    board = empty_board()

    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    black_score = heuristic(board, BLACK)
    white_score = heuristic(board, WHITE)

    assert black_score > 0
    assert white_score < 0
    assert black_score == -white_score


def test_order_moves_prioritizes_immediate_win():
    board = empty_board()

    board[7][4] = BLACK
    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    moves = legal_moves(board)
    ordered_moves = order_moves(board, moves, BLACK)

    assert ordered_moves[0] in {(7, 3), (7, 8)}


def test_order_moves_prioritizes_immediate_block():
    board = empty_board()

    board[8][4] = WHITE
    board[8][5] = WHITE
    board[8][6] = WHITE
    board[8][7] = WHITE

    moves = legal_moves(board)
    ordered_moves = order_moves(board, moves, BLACK)

    assert ordered_moves[0] in {(8, 3), (8, 8)}
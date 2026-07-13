from copy import deepcopy

from gomoku_ai.common.board import BLACK, WHITE, EMPTY, legal_moves
from gomoku_ai.search.heuristics import heuristic
from gomoku_ai.search.minimax import find_best_move, minimax


def empty_board(size: int = 15):
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def test_find_best_move_takes_immediate_win():
    board = empty_board()

    board[7][4] = BLACK
    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    move = find_best_move(board, BLACK, depth=2)

    assert move in {(7, 3), (7, 8)}


def test_find_best_move_blocks_opponent_win():
    board = empty_board()

    board[8][4] = WHITE
    board[8][5] = WHITE
    board[8][6] = WHITE
    board[8][7] = WHITE

    move = find_best_move(board, BLACK, depth=2)

    assert move in {(8, 3), (8, 8)}


def test_find_best_move_returns_legal_empty_position():
    board = empty_board()

    board[7][7] = BLACK
    board[7][8] = WHITE

    move = find_best_move(board, BLACK, depth=2)
    row, col = move

    assert move in legal_moves(board)
    assert board[row][col] == EMPTY


def test_find_best_move_does_not_modify_board():
    board = empty_board()

    board[7][7] = BLACK
    board[7][8] = WHITE

    original_board = deepcopy(board)

    find_best_move(board, BLACK, depth=2)

    assert board == original_board


def test_minimax_depth_zero_uses_heuristic():
    board = empty_board()

    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    expected_score = heuristic(board, BLACK)

    score, move = minimax(
        board=board,
        depth=0,
        current_player=BLACK,
        ai_player=BLACK,
        alpha=float("-inf"),
        beta=float("inf"),
    )

    assert score == expected_score
    assert move is None
from gomoku_ai.common.board import EMPTY, can_win_points, legal_moves, opponent
from gomoku_ai.search.heuristics import heuristic, order_moves

def find_best_move(board, player: int):
    # 1. If the current player can win immediately, take that move.
    winning_moves = can_win_points(board, player)
    if winning_moves:
        return winning_moves[0]

    # 2. If the opponent can win immediately, block it.
    opp = opponent(player)
    blocking_moves = can_win_points(board, opp)
    if blocking_moves:
        return blocking_moves[0]

    # 3. Otherwise, evaluate all candidate moves with a one-step heuristic.
    moves = legal_moves(board)
    moves = order_moves(board, moves, player)

    best_move = None
    best_score = float("-inf")

    for row, col in moves:
        board[row][col] = player

        score = heuristic(board, player)

        board[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

    if best_move is None:
        return 0, 0

    return best_move
from gomoku_ai.common.board import EMPTY, can_win_points, legal_moves, opponent
from gomoku_ai.search.heuristics import heuristic, order_moves

def minimax(board, depth: int, current_player: int, ai_player: int, alpha: float, beta: float):
    # 1. If search reaches the depth limit, evaluate the board.
    if depth == 0:
        return heuristic(board, ai_player), None

    # 2. If the current player can win immediately, this is a terminal-like state.
    winning_moves = can_win_points(board, current_player)
    if winning_moves:
        if current_player == ai_player:
            return 1_000_000 + depth, winning_moves[0]
        else:
            return -1_000_000 - depth, winning_moves[0]

    # 3. Generate candidate moves.
    moves = legal_moves(board)
    moves = order_moves(board, moves, current_player)

    if not moves:
        return 0, None

    next_player = opponent(current_player)

    # 4. AI's turn: choose the move with the highest score.
    if current_player == ai_player:
        best_score = float("-inf")
        best_move = None

        for row, col in moves:
            board[row][col] = current_player

            score, _ = minimax(
                board,
                depth - 1,
                next_player,
                ai_player,
                alpha,
                beta,
            )

            board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)

            alpha = max(alpha, best_score)

            if alpha >= beta:
                break

        return best_score, best_move

    # 5. Opponent's turn: choose the move with the lowest score for AI.
    else:
        best_score = float("inf")
        best_move = None

        for row, col in moves:
            board[row][col] = current_player

            score, _ = minimax(
                board,
                depth - 1,
                next_player,
                ai_player,
                alpha,
                beta,
            )

            board[row][col] = EMPTY

            if score < best_score:
                best_score = score
                best_move = (row, col)

            beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score, best_move

def find_best_move(board, player: int, depth: int=2):
    # 1. If the current player can win immediately, take that move.
    winning_moves = can_win_points(board, player)
    if winning_moves:
        return winning_moves[0]

    # 2. If the opponent can win immediately, block it.
    opp = opponent(player)
    blocking_moves = can_win_points(board, opp)
    if blocking_moves:
        return blocking_moves[0]

     # 3. Otherwise, use minimax search.
    _, best_move = minimax(
        board=board,
        depth=depth,
        current_player=player,
        ai_player=player,
        alpha=float("-inf"),
        beta=float("inf")
    )

    if best_move is None:
        moves = order_moves(board, legal_moves(board), player)
        return moves[0] if moves else (0, 0)

    return best_move


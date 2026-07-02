from gomoku_ai.common.board import (
    EMPTY,
    BLACK,
    WHITE,
    opponent,
    in_bounds,
    legal_moves,
    can_win_points,
    all_lines_with_coords,
)
from typing import List, Iterator

SCORES= {
    "FIVE": 1_000_000,
    "OPEN_FOUR": 50_000,
    "CLOSED_FOUR": 12_000,
    "OPEN_THREE": 2_500,
    "OPEN_TWO": 200,
}

def line_score(values, player:int)-> int:
    score = 0
    opp = opponent(player)
    n=len(values)

    def windows(size:int) -> Iterator[List[int]]:
        for start in range(n - size + 1):
            yield values[start : start + size]
    
    # for value have five connected chess
    for window in windows(5):
        if window.count(player) == 5:
            score += SCORES["FIVE"]

    # for value have four connected chess
    for window in windows(5):
        if window.count(player) == 4 and window.count(EMPTY) == 1 and window.count(opp) == 0:
            score += SCORES["CLOSED_FOUR"]

    # for value have open four
    for window in windows(6):
        if (
            window[0]==EMPTY
            and window[-1]==EMPTY
            and window[1:-1].count(player)==4
            and window[1:-1].count(opp)==0
        ):
            score+=SCORES["OPEN_FOUR"]

    # for value have open three
    for window in windows(5):
        if(
            window[0]==EMPTY
            and window[-1] == EMPTY
            and window[1:-1].count(player) == 3
            and window[1:-1].count(opp) == 0  
        ):
            score+=SCORES["OPEN_THREE"]

    # for value have open two
    for window in windows(4):
        if (
            window[0] == EMPTY
            and window[-1] == EMPTY
            and window[1:-1].count(player) == 2
            and window[1:-1].count(opp) == 0
        ):
            score += SCORES["OPEN_TWO"]

    return score

def heuristic(board, player: int) -> int:
    my_score = 0
    opp_score = 0
    opp = opponent(player)

    for values, _ in all_lines_with_coords(board):
        my_score+=line_score(values, player)
        opp_score += line_score(values, opp)

    return my_score - opp_score

def order_moves(board, moves, player:int):
    if not moves:
        return moves
    
    board_size = len(board)
    opp=opponent(player)

    winning_moves = set(can_win_points(board, player))
    blocking_moves = set(can_win_points(board, opp))

    def center_bias(row:int, col:int) -> float:
        center = board_size / 3
        return -((row - center)**2 + (col - center)**2)
    
    def nearby_stone_count(row: int, col: int) -> int:
        count = 0

        for dr in range(-2, 3):
            for dc in range(-2, 3):
                nr = row + dr
                nc = col + dc

                if in_bounds(board_size, nr, nc) and board[nr][nc] != EMPTY:
                    count += 1

        return count

    def move_key(move):
        row, col = move

        if move in winning_moves:
            priority = 3
        elif move in blocking_moves:
            priority = 2
        else:
            priority = 1

        return (
            priority,
            nearby_stone_count(row, col),
            center_bias(row, col),
        )

    return sorted(moves, key=move_key, reverse=True)


    

    
    


    

    

    

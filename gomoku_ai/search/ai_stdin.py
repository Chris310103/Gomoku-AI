import sys

from gomoku_ai.common.protocol import (
    make_error_response,
    make_move_response,
    parse_request,
    player_to_stone,
)
from gomoku_ai.search.minimax import find_best_move


def process_request(line: str) -> str:
    board, player_name = parse_request(line)
    player = player_to_stone(player_name)

    row, col = find_best_move(
        board=board,
        player=player,
        depth=2,
    )

    return make_move_response(row, col)


def main_loop() -> None:
    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        try:
            response = process_request(line)
        except Exception as error:
            response = make_error_response(error)

        sys.stdout.write(response + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main_loop()
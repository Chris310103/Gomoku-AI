import json

from gomoku_ai.common.board import BLACK, WHITE


def parse_request(line: str):
    request = json.loads(line.strip())

    board = request["board"]
    player = request.get("player", "white")

    return board, player


def player_to_stone(player: str) -> int:
    if player == "black":
        return BLACK
    if player == "white":
        return WHITE

    raise ValueError(f"Invalid player: {player}")


def make_move_response(row: int, col: int) -> str:
    return json.dumps({
        "row": int(row),
        "col": int(col),
    })


def make_error_response(error: Exception) -> str:
    return json.dumps({
        "row": -1,
        "col": -1,
        "error": str(error),
    })


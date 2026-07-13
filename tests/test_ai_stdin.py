import json
import subprocess
import sys

from gomoku_ai.common.board import BLACK, WHITE, EMPTY
from gomoku_ai.search.ai_stdin import process_request


def empty_board(size: int = 15):
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def test_process_request_returns_valid_move_json():
    board = empty_board()
    board[7][7] = BLACK
    board[7][8] = WHITE

    request = json.dumps({
        "board": board,
        "player": "black",
    })

    response = process_request(request)
    data = json.loads(response)

    row = data["row"]
    col = data["col"]

    assert 0 <= row < 15
    assert 0 <= col < 15
    assert board[row][col] == EMPTY


def test_process_request_takes_immediate_win():
    board = empty_board()

    board[7][4] = BLACK
    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    request = json.dumps({
        "board": board,
        "player": "black",
    })

    response = process_request(request)
    data = json.loads(response)

    assert (data["row"], data["col"]) in {
        (7, 3),
        (7, 8),
    }


def test_process_request_blocks_opponent_win():
    board = empty_board()

    board[8][4] = WHITE
    board[8][5] = WHITE
    board[8][6] = WHITE
    board[8][7] = WHITE

    request = json.dumps({
        "board": board,
        "player": "black",
    })

    response = process_request(request)
    data = json.loads(response)

    assert (data["row"], data["col"]) in {
        (8, 3),
        (8, 8),
    }


def test_ai_stdin_returns_json_error_for_invalid_player():
    board = empty_board()

    request = json.dumps({
        "board": board,
        "player": "red",
    })

    result = subprocess.run(
        [sys.executable, "-m", "gomoku_ai.search.ai_stdin"],
        input=request + "\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0

    response = json.loads(result.stdout.strip())

    assert response["row"] == -1
    assert response["col"] == -1
    assert "Invalid player" in response["error"]
    
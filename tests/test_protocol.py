import json

import pytest

from gomoku_ai.common.board import BLACK, WHITE
from gomoku_ai.common.protocol import (
    make_error_response,
    make_move_response,
    parse_request,
    player_to_stone,
)


def test_parse_request():
    line = json.dumps({
        "board": [[0, 1], [2, 0]],
        "player": "black",
    })

    board, player = parse_request(line)

    assert board == [[0, 1], [2, 0]]
    assert player == "black"


def test_parse_request_defaults_to_white():
    line = json.dumps({
        "board": [[0, 0], [0, 0]],
    })

    _, player = parse_request(line)

    assert player == "white"


def test_player_to_stone():
    assert player_to_stone("black") == BLACK
    assert player_to_stone("white") == WHITE


def test_player_to_stone_rejects_invalid_player():
    with pytest.raises(ValueError, match="Invalid player"):
        player_to_stone("red")


def test_make_move_response_returns_valid_json():
    response = make_move_response(7, 8)
    data = json.loads(response)

    assert data == {
        "row": 7,
        "col": 8,
    }


def test_make_error_response_returns_valid_json():
    response = make_error_response(ValueError("bad request"))
    data = json.loads(response)

    assert data["row"] == -1
    assert data["col"] == -1
    assert data["error"] == "bad request"
    
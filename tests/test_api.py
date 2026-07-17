from fastapi.testclient import TestClient

from backend.app.main import app
from gomoku_ai.common.board import BLACK, WHITE, EMPTY


client = TestClient(app)


def empty_board(size: int = 15):
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "gomoku-ai-api",
    }


def test_recommend_returns_legal_move():
    board = empty_board()
    board[7][7] = BLACK
    board[7][8] = WHITE

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "black",
            "depth": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()
    row = data["move"]["row"]
    col = data["move"]["col"]

    assert 0 <= row < 15
    assert 0 <= col < 15
    assert board[row][col] == EMPTY


def test_recommend_takes_immediate_win():
    board = empty_board()

    board[7][4] = BLACK
    board[7][5] = BLACK
    board[7][6] = BLACK
    board[7][7] = BLACK

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "black",
            "depth": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
            data["move"]["row"],
            data["move"]["col"],
        ) in {
            (7, 3),
            (7, 8),
        }


def test_recommend_rejects_invalid_player():
    board = empty_board()

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "red",
            "depth": 2,
        },
    )

    assert response.status_code == 422


def test_recommend_rejects_invalid_board_value():
    board = empty_board()
    board[7][7] = 9

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "black",
            "depth": 2,
        },
    )

    assert response.status_code == 422


def test_recommend_rejects_excessive_depth():
    board = empty_board()

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "black",
            "depth": 10,
        },
    )

    assert response.status_code == 422

def test_recommend_returns_search_metadata():
    board = empty_board()
    board[7][7] = BLACK
    board[7][8] = WHITE

    response = client.post(
        "/recommend",
        json={
            "board": board,
            "player": "black",
            "depth": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["player"] == "black"
    assert data["engine"] == "minimax_alpha_beta"
    assert data["depth"] == 2
    assert isinstance(data["evaluation_score"], int)
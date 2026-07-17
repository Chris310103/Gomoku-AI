from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RecommendRequest(BaseModel):
    board: list[list[int]]
    player: Literal["black", "white"]
    depth: int = Field(default=2, ge=1, le=4)

    @field_validator("board")
    @classmethod
    def validate_board(cls, board: list[list[int]]) -> list[list[int]]:
        if not board:
            raise ValueError("Board cannot be empty")

        board_size = len(board)

        if any(len(row) != board_size for row in board):
            raise ValueError("Board must be square")

        if any(cell not in (0, 1, 2) for row in board for cell in row):
            raise ValueError("Board cells must be 0, 1, or 2")

        return board


class MoveCoordinates(BaseModel):
    row: int
    col: int


class RecommendResponse(BaseModel):
    move: MoveCoordinates
    player: Literal["black", "white"]
    engine: Literal["minimax_alpha_beta"]
    depth: int
    evaluation_score: int
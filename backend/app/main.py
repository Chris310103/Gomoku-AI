from fastapi import FastAPI

from backend.app.schemas import (
    MoveCoordinates,
    RecommendRequest,
    RecommendResponse,
)
from gomoku_ai.common.protocol import player_to_stone
from gomoku_ai.search.minimax import find_best_move_with_score


app = FastAPI(
    title="Gomoku AI API",
    description="Backend service for Gomoku move recommendation and game analysis.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "gomoku-ai-api",
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend_move(request: RecommendRequest) -> RecommendResponse:
    player = player_to_stone(request.player)

    score, move = find_best_move_with_score(
        board=request.board,
        player=player,
        depth=request.depth,
    )

    row, col = move

    return RecommendResponse(
        move=MoveCoordinates(
            row=row,
            col=col,
        ),
        player=request.player,
        engine="minimax_alpha_beta",
        depth=request.depth,
        evaluation_score=score,
    )
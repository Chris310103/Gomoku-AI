from fastapi import FastAPI

from backend.app.schemas import MoveResponse, RecommendRequest
from gomoku_ai.common.protocol import player_to_stone
from gomoku_ai.search.minimax import find_best_move


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


@app.post("/recommend", response_model=MoveResponse)
def recommend_move(request: RecommendRequest) -> MoveResponse:
    player = player_to_stone(request.player)

    row, col = find_best_move(
        board=request.board,
        player=player,
        depth=request.depth,
    )

    return MoveResponse(
        row=row,
        col=col,
    )
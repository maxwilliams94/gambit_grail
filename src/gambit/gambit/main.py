"""
Gambit service API
"""
from collections.abc import Iterable
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from typing import Union, List

from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from pydantic import BaseSettings, BaseModel

from gambit_tree import create_gambit_boards
from gambit.board import Board
from gambit.util import cast_singleton

class Settings(BaseSettings):
    gambit_pgn_path: Path = Path(
        "/Users/max/local/dev/gambit_grail/src/gambit/gambit/gambits.pgn")
    
settings = Settings()

class PGNGame(BaseModel):
    pgn: str


router = APIRouter(
    prefix="/api/v1",
)

def is_gambit_json(is_gambit: bool, gambit_name: Union[str, None] = None, fen: Union[str, List[str], None] = None,
                   message: str = None, **kwargs) -> dict:
    _dict = {"isGambit": is_gambit}
    if gambit_name:
        _dict["gambitName"] = gambit_name
    if fen:
        _dict["gambitFen"] = fen
    if message:
        _dict["message"] = message

    if kwargs:
        _dict += kwargs
    
    return _dict
    
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    on start up tasks
    """
    logging.getLogger("gambit")
    logging.basicConfig(filename="/tmp/gambit.log", filemode="w", level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")), force=True,
                        format="%(asctime)s %(name)s::%(levelname)s::%(module)s %(message)s")
    app.gambit_boards = create_gambit_boards(settings.gambit_pgn_path)
    app.board_map = {hash(app.gambit_boards[i]): i for i in range(len(app.gambit_boards))}
    
    yield


app = FastAPI(lifespan=lifespan)


@router.get("/boards")
async def status():
    return {"boards": len(app.gambit_boards),
            "hashes": app.board_map}


@router.get("/game/position")
async def game(fen: str = None):
    if fen is None:
        return None
    try:
        board = Board.from_fen(fen)
    except IndexError:
        return is_gambit_json(False, message="Invalid FEN", invalidFEN=fen)

    _hash = hash(board)
    is_gambit = _hash in app.board_map
    logging.debug(f"Check board hash ({_hash}) is in app.board_map: {is_gambit}")
    board : Board = app.gambit_boards[app.board_map.get(_hash)] if is_gambit else None
    if board:
        return is_gambit_json(is_gambit,
                            board.get_variation_name() if is_gambit else None,
                            board.fen)
    
    return is_gambit_json(False)


@router.post("/game/pgn")
async def pgn(_pgn: PGNGame):
    positions: Iterable[Board] = Board.from_pgn(_pgn.pgn)
    gambits: Iterable[Board] = [board for board in positions if hash(board) in app.board_map]
    contains_gambit = len(gambits) > 0
    return is_gambit_json(contains_gambit,
                          cast_singleton([board.get_variation_name() for board in gambits]),
                          cast_singleton([board.fen for board in gambits]))
        

app.include_router(router)

"""
Parsing and output of PGN formats
"""
import logging
from pathlib import Path
from typing import Union, List

from chess.pgn import read_game, read_headers

from gambit.board import Board

logging.getLogger("gambit").addHandler(logging.NullHandler())


def boards_from_pgn(pgn: Union[Path, str]) -> List[Board]:
    if not isinstance(pgn, Path):
        try:
            game = read_game(pgn)
        except AttributeError:
            with open(pgn, "r") as f_pgn:
                game = read_game(pgn)
    else:
        game = read_game(pgn.open())        

    boards = []
    while game is not None:
        board = Board.from_fen(game.board())
        boards.append(board)
        game = game.next()
        
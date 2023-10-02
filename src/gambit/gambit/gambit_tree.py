"""
Create a database of Gambit board positions
"""
import logging
from pathlib import Path
from typing import List

from chess.pgn import read_game, GameNode, Game
from gambit.board import Board

logger = logging.getLogger("gambit")
logger.addHandler(logging.NullHandler())

def load_pgn(file_path: Path) -> Game:
    with open(file_path, "r") as pgn:
        return read_game(pgn)


def create_nodes(game: Game):
    nodes = []
    stack = game.variations
    while stack:
        node = stack.pop()
        while not node.is_end():
            if node.has_variation:
                stack.extend(node.variations)
                node = stack.pop()
            else:
                node = node.next()
        
        nodes.append(node)
    logger.info(f"create_nodes: {len(nodes)} nodes.")
    return nodes


def create_gambit_boards(pgn_path: Path) -> List[Board]:
    """
    Load and walk the gambit PGN tree to create each board
    """
    pgn = load_pgn(pgn_path)
    all_nodes = create_nodes(pgn)
    logging.info(f"{len(all_nodes)} nodes.")
    boards = [node.board() for node in all_nodes]
    logging.info(f"Created {len(boards)} gambit boards")

    return [Board.from_fen(board.fen()) for board in boards]


if __name__ == "__main__":
    create_gambit_boards("/Users/max/local/dev/gambit_grail/src/gambit/gambit/gambits.pgn")
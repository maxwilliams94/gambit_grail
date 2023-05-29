"""
Chess board/position functionality
"""

from enum import Enum
from re import split

import numpy as np
from numpy import int32

import gambit.fen

EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = 0
BLACK = 8

BOARD_SIZE = 8

PIECE_MAP = {
    "E": EMPTY,
    "P": PAWN,
    "p": PAWN + BLACK,
    "N": KNIGHT,
    "n": KNIGHT + BLACK,
    "B": BISHOP,
    "b": BISHOP + BLACK,
    "R": ROOK,
    "r": ROOK + BLACK,
    "Q": QUEEN,
    "q": QUEEN + BLACK,
    "K": KING,
    "k": KING + BLACK,
}


class Board:
    def __init__(self, empty=False):
        self.board = np.zeros(BOARD_SIZE ** 2, dtype=int32)
        self.turn = WHITE
        self.castling = {"K": True, "k": True, "Q": True, "q": True}
        self.en_passant_square: str = None
        self.half_moves = 0
        self.full_moves = 1

        if not empty:
            self.set_up_new_game()

    @staticmethod
    def _index(file, rank) -> int:
        return file + (BOARD_SIZE * rank)

    @staticmethod
    def index(square: str):
        """
        Index on the board from [A-z][1-8]
        """
        file, rank = (square[0].lower(), BOARD_SIZE - int(square[1]))
        file = ord(file) - ord("a")

        return Board._index(file, rank)

    
    def contents(self, square: str):
        """
        Get contents of (File, Rank) (e.g e4) of the board
        """
        try:
            return self.board[Board.index(square)]        
        except IndexError:
            return EMPTY
    
    def __hash__(self):
        multi = 1.0
        _sum = 0.0
        for i in range(self.board.shape[0]):
            _sum += self.board[i] * multi
            multi *= 2
        
        return int(_sum)
    
    def set_up_new_game(self):
        self.board = np.array(
            [BLACK + p for p in [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]] +
            [PAWN + BLACK for _ in range(BOARD_SIZE)] +
            [EMPTY for _ in range(BOARD_SIZE * 4)] +
            [PAWN for _ in range(BOARD_SIZE)] +
            [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK],
        dtype=int32)

    def parse_details(self, fen: str):
        self.turn = WHITE if gambit.fen.active_color_from_fen(fen).lower() == "w" else BLACK
        castling_rights = gambit.fen.castling_text_from_fen(fen)
        for key in self.castling:
            self.castling[key] = key in castling_rights
        en_passant_square = gambit.fen.en_passant_square_text_from_fen(fen)
        self.en_passant_square = en_passant_square if en_passant_square != "-" else None
        self.half_moves = int(gambit.fen.half_moves_for_50mr_text_from_fen(fen))
        self.full_moves = int(gambit.fen.full_move_clock_text_from_fen(fen))

    @classmethod
    def from_fen(cls, fen_txt: str):
        """
        Return a board for the pgn position
        """
        fen = gambit.fen.expand_fen(fen_txt)
        ranks = gambit.fen.position_text_from_fen(fen)
        ranks = ranks.split("/")
        board = cls(empty=True)
        board.parse_details(fen)
        for i_rank, rank in enumerate(ranks):
            for i_file, square in enumerate(rank):
                try:
                    board.board[Board._index(i_file, i_rank)] = PIECE_MAP[square]
                except IndexError as exc:
                    print(exc)
                    Board._index(i_file, i_rank)

        return board
        


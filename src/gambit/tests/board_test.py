from itertools import product
from pathlib import Path

import pytest

from gambit.board import Board, EMPTY, PAWN, WHITE, BLACK


class TestBoard:
    @pytest.fixture
    def board(self):
        return Board(empty=False)
        
    @pytest.mark.parametrize("file,rank,expected_index", [
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, 8),
        (7, 7, 63),
    ])
    def test__index(self, board, file, rank, expected_index):
        assert board._index(file, rank) == expected_index

    @pytest.mark.parametrize("square,expected_index", [
        ("a8", 0),
        ("h8", 7),
        ("a1", 56),
        ("h1", 63),
        ("e2", 52),
        ("e4", 36),
    ])
    def test_index(self, board, square, expected_index):
        assert board.index(square) == expected_index

    def test_hash(self, board):
        hash(board)

class TestBoardFromFen:
    def test_starting_position(self, test_file):
        fen = test_file("fen_start.fen").read_text()
        board = Board.from_fen(fen)

        new_board = Board()

        assert len(board.board) == len(new_board.board)
        for i in range(len(board.board)):
            assert board.board[i] == new_board.board[i]

        assert board.turn == WHITE
        assert all(board.castling.values())
        assert board.en_passant_square is None
        assert board.half_moves == 0
        assert board.full_moves == 1
        
    def test_move_1(self, test_file):
        fen = test_file("fen_move1.fen").read_text()
        board = Board.from_fen(fen)

        new_board = Board()
        new_board.board[Board.index("e2")] = EMPTY
        new_board.board[Board.index("e4")] = PAWN

        assert len(board.board) == len(new_board.board)
        for i in range(len(board.board)):
            assert board.board[i] == new_board.board[i], i

        assert board.turn == BLACK
        assert all(board.castling.values())
        assert board.en_passant_square is None
        assert board.half_moves == 0
        assert board.full_moves == 1
        

if __name__ == "__main__":
    pass
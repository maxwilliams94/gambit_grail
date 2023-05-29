from pathlib import Path

import pytest
from gambit.fen import (expand_fen,
                        position_text_from_fen,
                        detail_text_from_fen,
                        active_color_from_fen,
                        castling_text_from_fen,
                        en_passant_square_text_from_fen,
                        half_moves_for_50mr_text_from_fen,
                        full_move_clock_text_from_fen)

class TestExpandFen:
    def test_load_new_board(test, test_file):
        fen = test_file("fen_start.fen").read_text()

        expanded_fen = expand_fen(fen)

        assert "".join(8 * ["E"]) in expanded_fen
        assert " w" in expanded_fen

    def test_load_new_board(test, test_file):
        fen = test_file("fen_move1.fen").read_text()

        expanded_fen = expand_fen(fen)
        assert "".join(8 * ["E"]) in expanded_fen
        assert "EEEEPEEE" in expanded_fen
        assert " b" in expanded_fen

class TestGetFenText:
    @pytest.fixture(scope="class")
    def fen(self, test_file):
        return test_file("fen_start.fen").read_text()
    
    def test_position(self, fen):
        text = position_text_from_fen(fen)
        assert text == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    
    def test_detail(self, fen):
        text = detail_text_from_fen(fen)
        assert text == "w KQkq - 0 1"
    
    def test_active_color(self, fen):
        text = active_color_from_fen(fen)
        assert text == "w"
    
    def test_castling(self, fen):
        text = castling_text_from_fen(fen)
        assert text == "KQkq"
    
    def test_en_passant(self, fen):
        text = en_passant_square_text_from_fen(fen)
        assert text == "-"
    
    def test_half_moves(self, fen):
        text = half_moves_for_50mr_text_from_fen(fen)
        assert text == "0"
    
    def test_full_moves(self, fen):
        text = full_move_clock_text_from_fen(fen)
        assert text == "1"

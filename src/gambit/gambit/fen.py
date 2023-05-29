"""
FEN parsing
"""
import re

def expand_fen(fen_text: str) -> str:
    """
    Expand FEN text so that empty squares are explicitly represented
    """
    board_positions, the_rest = fen_text.split(" ", 1)
    empty_designations = list(set(re.findall("[1-8]", fen_text)))
    for to_replace in empty_designations:
        board_positions = board_positions.replace(to_replace, "".join(["E"] * int(to_replace)))

    
    return board_positions + " " + the_rest

    
def position_text_from_fen(fen_text: str) -> str:
    """
    Return piece position text from fen
    """
    return fen_text.split(" ", 1)[0]

    
def detail_text_from_fen(fen_text: str) -> str:
    """
    Return castling, move text from fen
    """
    return fen_text.split(" ", 1)[1]


def active_color_from_fen(fen_text: str) -> str:
    """
    Return the active move text from fen
    """
    details = detail_text_from_fen(fen_text)
    return details.split(" ")[0]


def castling_text_from_fen(fen_text: str) -> str:
    """
    Return castling rights text from fen
    """
    details = detail_text_from_fen(fen_text)
    return details.split(" ")[1]


def en_passant_square_text_from_fen(fen_text: str) -> str:
    """
    Return enpassant text from fen
    """
    details = detail_text_from_fen(fen_text)
    return details.split(" ")[2]


def half_moves_for_50mr_text_from_fen(fen_text: str) -> str:
    """
    Return half moves since last capture or pawn move
    """
    details = detail_text_from_fen(fen_text)
    return details.split(" ")[3]


def full_move_clock_text_from_fen(fen_text: str) -> str:
    """
    Return full move clock (starts at 1) and increments after blacks move
    """
    details = detail_text_from_fen(fen_text)
    return details.split(" ")[4]


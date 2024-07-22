from enum import Enum

def override(fun):
    return fun

class Const(Enum):
    fig = {"R": "Rook", "Kn": "Knight", "B": "Bishop", "Q": "Queen", "K": "King", "P": "Pawn"}
    # windows version
    #sym = {"whiteKing": "♚", "whiteQueen": "♛", "whiteRook": "♜", "whiteBishop": "♝", "whiteKnight": "♞", "whitePawn": "♟",
    #       "blackKing": "♔", "blackQueen": "♕", "blackRook": "♖", "blackBishop": "♗", "blackKnight": "♘", "blackPawn": "♙",
    #       "empty": "⛆"}
    # linux version
    sym = {"whiteKing": "♚", "whiteQueen": "♛", "whiteRook": "♜", "whiteBishop": "♝", "whiteKnight": "♞", "whitePawn": "♟",
           "blackKing": "♔", "blackQueen": "♕", "blackRook": "♖", "blackBishop": "♗", "blackKnight": "♘", "blackPawn": "♙",
           "empty": "."}
    white = "white"
    black = "black"
    length = 8
    A = ord("A")
    H = ord("H")
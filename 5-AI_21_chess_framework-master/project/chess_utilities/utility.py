from abc import ABC
import chess

"""A generic utility class"""
class Utility(ABC):

    # Determine the value of the current board position (high is good for white, low is good for black, 0 is neutral)
    def board_value(self, board: chess.Board):
        if board.is_checkmate():
            if board.turn:
                # Return very low number when check mate on our turn
                return -9999
            else:
                # return very high number when check mate on not our turn
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        # White pieces
        white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
        white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
        white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
        white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
        white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))

        # Black pieces
        black_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
        black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
        black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
        black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
        black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))

        # Define piece value for each piece
        # Source: https://en.wikipedia.org/wiki/Chess_piece_relative_value
        # Used here: AlphaZero, reason: most recent.
        pawn_value = 100
        knight_value = 305
        bishop_value = 333
        rook_value = 501
        queen_value = 880

        # Board evaluations for each piece in tables
        # Source: https://www.chessprogramming.org/index.php?title=Simplified_Evaluation_Function&mobileaction=toggle_view_desktop
        pawntable = [
            0,   0,    0,    0,   0,   0,   0,   0,
            5,  10,   10,  -20, -20,  10,  10,   5,
            5,  -5,  -10,    0,   0, -10,  -5,   5,
            0,   0,    0,   20,  20,   0,   0,   0,
            5,   5,   10,   25,  25,  10,   5,   5,
            10, 10,   20,   30,  30,  20,  10,  10,
            50, 50,   50,   50,  50,  50,  50,  50,
            0,   0,   0,     0,   0,   0,   0,  0
        ]

        knightstable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20,   0,   5,   5,   0, -20, -40,
            -30,   5,  10,  15,  15,  10,   5, -30,
            -30,   0,  15,  20,  20,  15,   0, -30,
            -30,   5,  15,  20,  20,  15,   5, -30,
            -30,   0,  10,  15,  15,  10,   0, -30,
            -40, -20,   0,   0,   0,   0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        bishopstable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10,   5,   0,   0,   0,   0,   5, -10,
            -10,  10,  10,  10,  10,  10,  10, -10,
            -10,   0,  10,  10,  10,  10,   0, -10,
            -10,   5,   5,  10,  10,   5,   5, -10,
            -10,   0,   5,  10,  10,   5,   0, -10,
            -10,   0,   0,   0,   0,   0,   0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        rookstable = [
            0,   0,   0,   5,   5,   0,   0,   0,
            -5,  0,   0,   0,   0,   0,   0,  -5,
            -5,  0,   0,   0,   0,   0,   0,  -5,
            -5,  0,   0,   0,   0,   0,   0,  -5,
            -5,  0,   0,   0,   0,   0,   0,  -5,
            -5,  0,   0,   0,   0,   0,   0,  -5,
            5,  10,  10,  10,  10,  10,  10,   5,
            0,   0,   0,   0,   0,   0,   0,   0
        ]

        queenstable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10,   0,   0,  0,  0,   0,   0, -10,
            -10,   5,   5,  5,  5,   5,   0, -10,
            0,     0,   5,  5,  5,   5,   0,  -5,
            -5,    0,   5,  5,  5,   5,   0,  -5,
            -10,   0,   5,  5,  5,   5,   0, -10,
            -10,   0,   0,  0,  0,   0,   0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        kingstable = [
            20,   30,  10,   0,   0,  10,  30,  20,
            20,   20,   0,   0,   0,   0,  20,  20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30
        ]

        # Estimate board_value by subtracting white_value by black_value and multiply by our AplhaZero value
        board_value = pawn_value * (white_pawn - black_pawn) + knight_value * (white_knight - black_knight) \
                   + bishop_value * (white_bishop - black_bishop) + rook_value * (white_rook - black_rook) \
                   + queen_value * (white_queen - black_queen)

        pawnsq = getsqwhite(board, pawntable, chess.PAWN)
        pawnsq = pawnsq + getsqblack(board, pawntable, chess.PAWN)
        knightsq = getsqwhite(board, knightstable, chess.KNIGHT)
        knightsq = knightsq + getsqblack(board, knightstable, chess.KNIGHT)
        bishopsq = getsqwhite(board, bishopstable, chess.BISHOP)
        bishopsq = bishopsq + getsqblack(board, bishopstable, chess.BISHOP)
        rooksq = getsqwhite(board, rookstable, chess.ROOK)
        rooksq = rooksq + getsqblack(board, rookstable, chess.ROOK)
        queensq = getsqwhite(board, queenstable, chess.QUEEN)
        queensq = queensq + getsqblack(board, queenstable, chess.QUEEN)
        kingsq = getsqwhite(board, kingstable, chess.KING)
        kingsq = kingsq + getsqblack(board, kingstable, chess.KING)

        value = board_value + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if board.turn:
            return value
        else:
            return -value

def getsqwhite(board: chess.Board, table, chesspiece):
    return sum([table[i] for i in board.pieces(chesspiece, chess.WHITE)])


def getsqblack(board: chess.Board, table, chesspiece):
    return sum([-table[chess.square_mirror(i)] for i in board.pieces(chesspiece, chess.BLACK)])


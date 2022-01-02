from abc import ABC
import chess
import time
import chess.polyglot
from project.chess_utilities.utility import Utility
from project.chess_utilities.tables import *

"""A generic agent class"""


class Agent(ABC):

    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        """Setup the Search Agent"""
        self.utility = utility
        self.time_limit_move = time_limit_move

    piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
    piecevalues = [100, 320, 330, 500, 900]

    def update_eval(self,board:chess.Board, mov, side):
        global boardvalue
        boardvalue = Utility.init_evaluate_board(self,board)

        # update piecequares
        movingpiece = board.piece_type_at(mov.from_square)
        if side:
            boardvalue = boardvalue - self.tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                boardvalue = boardvalue - rookstable[chess.H1]
                boardvalue = boardvalue + rookstable[chess.F1]
            elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                boardvalue = boardvalue - rookstable[chess.A1]
                boardvalue = boardvalue + rookstable[chess.D1]
        else:
            boardvalue = boardvalue + self.tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                boardvalue = boardvalue + rookstable[chess.H8]
                boardvalue = boardvalue - rookstable[chess.F8]
            elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                boardvalue = boardvalue + rookstable[chess.A8]
                boardvalue = boardvalue - rookstable[chess.D8]

        if side:
            boardvalue = boardvalue + self.tables[movingpiece - 1][mov.to_square]
        else:
            boardvalue = boardvalue - self.tables[movingpiece - 1][mov.to_square]

        # update material
        if mov.drop != None:
            if side:
                boardvalue = boardvalue + self.piecevalues[mov.drop - 1]
            else:
                boardvalue = boardvalue - self.piecevalues[mov.drop - 1]

        # update promotion
        if mov.promotion != None:
            if side:
                boardvalue = boardvalue + self.piecevalues[mov.promotion - 1] - self.piecevalues[movingpiece - 1]
                boardvalue = boardvalue - self.tables[movingpiece - 1][mov.to_square] \
                             + self.tables[mov.promotion - 1][mov.to_square]
            else:
                boardvalue = boardvalue - self.piecevalues[mov.promotion - 1] + self.piecevalues[movingpiece - 1]
                boardvalue = boardvalue + self.tables[movingpiece - 1][mov.to_square] \
                             - self.tables[mov.promotion - 1][mov.to_square]

        return mov

    def make_move(self, board:chess.Board, mov):
        self.update_eval(board, mov, board.turn)
        board.push(mov)

        return mov

    def unmake_move(self, board:chess.Board):
        mov = board.pop()
        self.update_eval(board, mov, not board.turn)

        return mov

    def quiesce(self, board:chess.Board, alpha, beta):
        stand_pat = Utility.evaluate_board(self,board)
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                self.make_move(board, move)
                score = -self.quiesce(board, -beta, -alpha)
                self.unmake_move(board)

                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def alphabeta(self, board:chess.Board, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(board, alpha, beta)
        for move in board.legal_moves:
            self.make_move(board, move)
            score = -self.alphabeta(board, -beta, -alpha, depthleft - 1)
            self.unmake_move(board)
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    import chess.polyglot

    def calculate_move(self, board:chess.Board, depth):
        print("SIGMA AI IS THINKING HARD...")

        try:
            move = chess.polyglot.MemoryMappedReader("C:/Users/arafa/OneDrive/Bureaublad/human.bin").weighted_choice(board).move
            return move

        except:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
            for move in board.legal_moves:
                board.push(move)
                boardValue = -self.alphabeta(board, -beta, -alpha, depth - 1)
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move
                if (boardValue > alpha):
                    alpha = boardValue
                board.pop()
            return bestMove
from abc import ABC
import chess
import time
from project.chess_utilities.utility import Utility

"""A generic agent class"""


class Agent(ABC):

    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        """Setup the Search Agent"""
        self.utility = utility
        self.time_limit_move = time_limit_move

    def calculate_move(self, board: chess.Board, depth=3):
        start_time = time.time()
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            if time.time() - start_time > self.time_limit_move:
                break
            board.push(move)
            boardValue = -self.alphabeta(board, -beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue;
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove

    def alphabeta(self, board: chess.Board, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(board, alpha, beta)
        for move in board.legal_moves:
            board.push(move)
            score = -self.alphabeta(board, -beta, -alpha, depthleft - 1)
            board.pop()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    def quiesce(self, board: chess.Board, alpha, beta):
        stand_pat = Utility.board_value(self, board)
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -self.quiesce(board, -beta, -alpha)
                board.pop()

                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha
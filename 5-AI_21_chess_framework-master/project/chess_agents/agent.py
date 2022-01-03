from abc import ABC
from sys import flags

import chess
import time
import os
import chess.polyglot
import chess.syzygy
from project.chess_utilities.utility import Utility
import re


"""A generic agent class"""


class Agent(ABC):

    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        """Setup the Search Agent"""
        self.utility = utility
        self.time_limit_move = time_limit_move

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

    def calculate_move(self, board: chess.Board, depth=2):
        start_time = time.time()
        try:
            dirpath = os.path.dirname(__file__).split("\project")[0] + "\\humans\\elo-3300.bin"
            move = chess.polyglot.MemoryMappedReader(dirpath).weighted_choice(board).move
            print("OPENING BOOOK..................")
            return move
        except:
                if(self.checkCurrentPieceCount(board) <= 5):
                    try:
                        with chess.syzygy.open_tablebase("data/syzygy") as tablebase:
                            board = chess.Board("8/2K5/4B3/3N4/8/8/4k3/8 b - - 0 1")
                            print("END TABLE BASE........")
                            bestMove = chess.Move.null()
                            bestValue = -99999
                            alpha = -100000
                            beta = 100000

                            # print(tablebase.probe_wdl(board))
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
                    except:
                        bestMove = chess.Move.null()
                        bestValue = -99999
                        alpha = -100000
                        beta = 100000

                        # print(tablebase.probe_wdl(board))
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



    def checkCurrentPieceCount(self,board:chess.Board):
        boardNew = str(board)
        alphabets = 0

        for i in range(len(boardNew)):
            if (boardNew[i].isalpha()):
                alphabets = alphabets + 1

        return alphabets

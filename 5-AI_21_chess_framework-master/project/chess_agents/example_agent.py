from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time
import random

"""An example search agent with two implemented methods to determine the next move"""
class ExampleAgent(Agent):

    # Initialize your agent with whatever parameters you want
    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Example search agent"
        self.author = "J. Duym & A. Troch"












from iterative_deepening import IterativeDeepening
# from minimax_agent import MinimaxAgent
from agent import Agent

class IDMinimaxEditAgent(IterativeDeepening):
    def __init__(self):
        super().__init__(AgentClass=Agent)
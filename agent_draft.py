"""
# what I did?
    rewrite a new heuristics function based on original minimax_agent.py file

# How is the test result?
    We played 5 matches, each consisting of 2 rounds. 
    So we have 5 * 2 = 10 games in total.
    Here, the compariation between this agent and original agents (minimax_agent, markov_agent) is as follows:
    
    #### compared with baseline minimax_agent: 
        this agent : minimax_agent : tied = 10 : 0 : 0  
    
    #### compared with baseline markov_agent:
        this agent : markov_agent : tied = 7 : 1 : 2 
        
"""
import random
from agent_interface import AgentInterface
from envs.konquest import Universe, ID


class Agent(AgentInterface):
    """
    An agent who plays the Konquest game using Minimax algorithm
    """

    def __init__(self, depth: int = 4):
        self.depth = depth
        self.__player = None

    def info(self):
        return {"agent name": f"edit Minimax-simple"}

    def heuristic(self, state: Universe):
        id = state.current_player_id

        my_ships = sum(p.ships for p in state.planets if p.owner == id)
        my_ships += sum(f.ships for f in state.fleets if f.owner == id)

        opp_ships = sum(p.ships for p in state.planets if p.owner != id)
        opp_ships += sum(f.ships for f in state.fleets if f.owner != id)

        my_production = sum(p.info.production for p in state.planets if p.owner == id)
        opp_production = sum(p.info.production for p in state.planets if p.owner != id)

        my_capacity = sum(p.info.capacity for p in state.planets if p.owner == id)
        opp_capacity = sum(p.info.capacity for p in state.planets if p.owner != id)

        my_planets = sum(1 for p in state.planets if p.owner == id)
        opp_planets = sum(1 for p in state.planets if p.owner != id)

        my_score = my_ships + my_production + my_capacity/10 + my_planets
        opp_score =  opp_ships + opp_production + opp_capacity/10 + opp_planets

        return my_score - opp_score

    def decide(self, state: Universe):
        successors = state.successors()
        random.shuffle(successors)
        best_action, _ = successors[0]
        max_value = float('-inf')
        for action, next_state in successors:
            action_value = self.min_value(next_state, self.depth - 1)
            if action_value > max_value:
                max_value = action_value
                best_action = action
        yield best_action

    def max_value(self, state: Universe, depth: int):
        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('inf')
        if depth == 0:
            return self.heuristic(state)

        # If it is not terminated
        successors = state.successors()
        value = float('-inf')
        for _, next_state in successors:
            value = max(value, self.min_value(next_state, depth - 1))
        return value

    def min_value(self, state: Universe, depth):

        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('-inf')
        if depth == 0:
            return -1 * self.heuristic(state)

        # If it is not terminated
        successors = state.successors()
        value = float('inf')
        for _, next_state in successors:
            value = min(value, self.max_value(next_state, depth - 1))
        return value

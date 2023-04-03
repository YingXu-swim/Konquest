import random
from envs.konquest import Universe
from agent_interface import AgentInterface
from envs.konquest import Universe, ID

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

class Agent(AgentInterface):
    """
    An agent who plays the Konquest game

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """
    def __init__(self, depth: int = 4):
        self.depth = depth
        self.__player = None

    @staticmethod
    def info():
        """
        Return the agent's information

        Returns
        -------
        Dict[str, str]
            `agent name` is the agent's name
            `student name` is the list team members' names
            `student number` is the list of student numbers of the team members
        """
        # -------- Task 1 -------------------------
        # Please complete the following information
        # NOTE: Please try to pick a unique name for you agent. If there are
        #       some duplicate names, we have to change them.

        return {"agent name": "edit Minimax",  # COMPLETE HERE
                "student name": ["Ying Xu"],  # COMPLETE HERE
                "student number": ["100863736"]}  # COMPLETE HERE

    def decide(self, state: Universe):
        """
        Generate a sequence of increasingly preferable actions

        Given the current `state`, this function should choose the action that
        leads to the agent's victory.
        However, since there is a time limit for the execution of this function,
        it is possible to choose a sequence of increasing preferable actions.
        Therefore, this function is designed as a generator; it means it should
        have no return statement, but it should `yield` a sequence of increasing
        good actions.

        IMPORTANT: If no action is yielded within the time limit, the game will
        choose a random action for the player.

        NOTE: You can find the possible actions and next states by using
              the `successors()` method of the `state`. In other words,
              `state.successors()` return a list of pairs of `action` and its
              corresponding next state.

        Parameters
        ----------
        state: Universe
            Current state of the game

        Yields
        ------
        action
            the chosen `action`
        """

        # -------- TASK 2 ------------------------------------------------------
        # Your task is to implement an algorithm to choose an action form the
        # possible `actions` in the `state.successors()`. You can implement any
        # algorithm you want.
        # However, you should keep in mind that the execution time of this
        # function is limited. So, instead of choosing just one action, you can
        # generate a sequence of increasing good action.
        # This function is a generator. So, you should use `yield` statement
        # rather than `return` statement. To find more information about
        # generator functions, you can take a look at:
        # https://www.geeksforgeeks.org/generators-in-python/
        #
        # If you generate multiple actions, the last action will be used in the
        # game.
        #
        #
        # Tips
        # ====
        # 0. You can improve the `MinimaxAgent` to implement the Alpha-beta
        #    pruning approach.
        #    Also, By using `IterativeDeepening` class you can simply add
        #    the iterative deepening feature to your Alpha-beta agent.
        #    You can find an example of this in `id_minimax_agent.py` file.
        # 
        # 1. You can improve the heuristic function of `MinimaxAgent`.
        #
        # 2. If you need to simulate a game from a specific state to find the
        #    the winner, you can use the following pattern:
        #    ```
        #    simulator = Game(FirstAgent(), SecondAgent())
        #    winner = simulator.play(starting_state=specified_state)
        #    ```
        #    The `Markov` has illustrated a concrete example of this
        #    pattern.
        #
        #
        #
        # GL HF :)
        # ----------------------------------------------------------------------

        # Replace the following lines with your algorithm
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


    def heuristic(self, state: Universe):
        """
        a heuristics function considering the number of ships, production, capacity and planets.
        return the difference between our score and the opponent's score 
        (Our score is bigger the better, and the opponent's score is smaller the better)
        """
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
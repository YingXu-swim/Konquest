
### What is Konquest

This game is based on the Konquest game in KDE/Ubuntu. The game starts with some
planets scattered in space and two players. Each planet can produce some ships.
Using ships, players can attack other planets to conquer them. The goal is to
build a unified interstellar empire by eliminating the other player.

In the beginning, each player owns one planet. The other planets are neutral.
A planet can be described by the following properties:
    * Name
    * Owner: its owner, or it might be neutral if it belongs to nobody
    * Position: its position in 2D space
    * Ships: number of ships currently located on the planet
    * Capacity: maximum number of ships that can be stationed on the planet
    * Production: the rate of producing ship

In each turn, players can send some ships from one of their planets to any
other planet. The source planet should be owned by the current player, and it
must contain at least the specified number of ships in the order. Depending on
the distance between the source and the destination it takes some turns for the
fleet to reach the destination. The fleet size can be 2, 4, or 8 ships. At the
time of arrival, if the destination and the fleet are owned by the same
player, then the fleet reinforces the planet.  Otherwise, it attacks the
destination. The kill rate in an attack is 70 percent. For example, if a fleet
with 2 ships attacks some planet, it can destroy 1.4 ships of the defender. If
the attacker defeats the defender, the ownership of the planet will change to
the owner.

Players have a specified amount of time to make a decision (e.g., 5 seconds).
This time limit may be varied at different stages of the game. As it would be 
difficult to adjust to any given time-bound, each player can generate a sequence
of increasing good actions in each turn, and the last action within the time
limit will be considered as the chosen action for that turn. If a player does
not choose any action within the time limit or chooses an invalid move, a random
action will be selected for the player. When all players make their decisions,
the simulation for that turn begins in the following order:
    1. fleets depart from their source planets
    2. planets produce new ships based on their production rate
    3. If there is any combat, it begins after the production.

Ultimately, the game ends when:
    1. A player loses all of its planets and ships to the winner of the game
    2. Both players can survive for 200 turns; in this case, the winner is the
       player who has the most ships in the game. If they have the same amount
       of ships, the game ends with a draw.


This game is a modified version of the Konquest game in KDE/Ubuntu. You can
play the original version from here:
    * https://apps.kde.org/konquest/


### Requirements
To run this program, we need to install `Pillow==9.4.0` and `numpy==1.24.2`.
You can install these dependencies by using the following command:
`pip3 install -r requirements.txt`

NOTE: We use `python3.9` for the tournament (more precisely, we disable the
      visualization and use `pypy` compatible with `python3.9` to improve the
      performance).


### Instructions
You can watch the game by running the following command:
   `python3 main.py`
   You can compare the performance of different agents, by choosing them as the
   players. To specify the type of players, you can modify the `players`
   variable in the `main.py`.
![image](https://github.com/rrrimp/Konquest/blob/main/images/gamepage.png)
This demo includes the following agents:
* the `RandomAgent` in `random_agent.py`,
* the `MarkovAgent` in `markov_agent.py`,
* the `MinimaxAgent` in `minimax_agent.py`,
* the `IterativeDeepening` in `iterative_deepening.py`, and,
* the `IDMinimaxAgent` in `id_minimax_agent.py`.
* the `IDMinimaxEditAgent` in `id_minimax_edit_agent.py` with modified heuristics function.


"""
这是一个实现 Markov 决策过程的智能体代码。
Markov 决策过程是一种使用随机性进行决策的决策过程，其结果是一组动作的概率分布。
该智能体在给定当前游戏状态时，通过使用模拟游戏来评估每个可能的动作，选择具有最大胜率的动作。

具体来说，这个代码中的 MarkovAgent 类实现了 AgentInterface 接口，
该接口包含一个 decide 方法，用于根据当前游戏状态选择一个动作。
在 __init__ 方法中，我们创建了一个 Game 对象，该对象包含两个随机智能体，用于在模拟游戏中执行动作。

在 decide 方法中，我们首先使用 state.successors() 方法获取当前游戏状态的所有后继状态，并将其打乱顺序。
然后我们使用一个 while 循环，对每个后继状态执行模拟游戏，并将胜利次数记录在列表 win_counter 中。
模拟游戏使用 self.__simulator.play 方法，该方法接受起始状态 next_state 和一个布尔值 output，
指示是否输出模拟游戏的每一步。如果 result 等于 [state.current_player]，则表示当前智能体赢得了该模拟游戏。

接下来，我们使用 win_counter.index(max(win_counter)) 查找 win_counter 列表中胜利次数最多的后继状态，并返回该状态的动作。
我们使用 yield 关键字返回动作，以便可以在循环中暂停并稍后恢复执行，以继续执行更多的模拟游戏。
如果在循环中没有找到最优动作，则该循环将一直执行下去，直到外部调用方停止。
"""

from random import shuffle
from agent_interface import AgentInterface
from envs.konquest import Universe
from random_agent import RandomAgent
from game import Game


class MarkovAgent(AgentInterface):
    """
    这是一个实现 Markov 决策过程的智能体代码。
    Markov 决策过程是一种使用随机性进行决策的决策过程，其结果是一组动作的概率分布。
    该智能体在给定当前游戏状态时，通过使用模拟游戏来评估每个可能的动作，选择具有最大胜率的动作。
    """
    def __init__(self):
        self.__simulator = Game([RandomAgent(), RandomAgent()]) # 我们创建了一个 Game 对象，该对象包含两个随机智能体，用于在模拟游戏中执行动作。

    def info(self):
        return {"agent name": "Markov"}

    def decide(self, state: Universe):
        # 首先使用 state.successors() 方法获取当前游戏状态的所有后继状态，并将其打乱顺序。
        successors = state.successors()
        shuffle(successors)
        win_counter = [0] * len(successors)

        # 使用一个 while 循环，对每个后继状态执行模拟游戏，并将胜利次数记录在列表 win_counter 中。
        while True:
            for i, (_, next_state) in enumerate(successors):
                result = self.__simulator.play(output=False, 
                                               starting_state=next_state) # 模拟游戏
                
                # 如果 result 等于 [state.current_player]，则表示当前智能体赢得了该模拟游戏。
                win_counter[i] += 1 if result == [state.current_player] else 0 
            # 使用 win_counter.index(max(win_counter)) 查找 win_counter 列表中胜利次数最多的后继状态
            yield successors[win_counter.index(max(win_counter))][0]
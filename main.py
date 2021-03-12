from random import *
from abc import *
from enum import *
from timeit import *


class Agent(metaclass=ABCMeta):
    __counter = 0

    def __init__(self, location=None, score=100):
        self.location = location
        self.score = score
        self.ID = Agent.__counter
        Agent.__counter += 1

    def percept(self, environment):
        pass

    def program(self):
        pass

    def action(self):
        pass


class Room:
    def __init__(self, dirty=False, dust_count=0):
        self.dirty = dirty
        self.dust_count = dust_count

    def randomize(self):
        self.dirty = choice([True, False])
        self.dust_count = randint(1, 100) if self.dirty else 0

        return self


class Location(IntEnum):
    LEFT = auto()
    RIGHT = auto()


class Environment:
    def __init__(self, left_room=Room(), right_room=Room(), left_agents=[], right_agents=[]):
        self.left_room = left_room
        self.right_room = right_room
        self.left_agents = {agent.ID: agent for agent in left_agents}
        self.right_agents = {agent.ID: agent for agent in right_agents}

    def randomize(self):
        self.left_room.randomize()
        self.right_room.randomize()

        agents = [v for _, v in self.left_agents.items()] + [v for _, v in self.left_agents.items()]

        self.left_agents.clear()
        self.right_agents.clear()

        for agent in agents:
            if choice([True, False]):
                agent.location = Location.RIGHT
                self.right_agents[agent.ID] = agent
            else:
                agent.location = Location.LEFT
                self.left_agents[agent.ID] = agent

    def score(self, agent):
        agent.score -= 1


class Simulator:
    def __init__(self, environment, agents):
        self.__environment = environment
        self.__agents = agents

    def run(self, iteration=100, randomize=True, verbose=True):
        if verbose:
            print('### VACUUM WORLD SIMULATOR ###')

        if randomize:
            self.__environment.randomize()

        if verbose:
            print('[CONFIGURATIONS]')
            print('  @Left room')
            print(f'    @# of dust  : {self.__environment.left_room.dust_count}')
            print(f'    @# of agents: {len(self.__environment.left_agents)}')
            print('  @Right room')
            print(f'    @# of dust  : {self.__environment.right_room.dust_count}')
            print(f'    @# of agents: {len(self.__environment.right_agents)}')
            print('  @Total')
            print(f'    @iterations : {iteration}')
            print(f'    @# of agents: {len(self.__agents)}')
            print()
            print('[INITIATE]')

            start = default_timer()

        for i in range(iteration):
            if verbose:
                print(f'  @iter {i}')
                print(f'  @action logs')

            for agent in self.__agents:
                agent.percept(self.__environment)
                agent.program()
                agent.action()(self.__environment)
                self.__environment.score(agent)

                if verbose:
                    print(f'    @{agent.description}')

            if verbose:
                print('  @Left room')
                print(f'    @# of dust  : {self.__environment.left_room.dust_count}')
                print(f'    @# of agents: {len(self.__environment.left_agents)}')
                print('  @Right room')
                print(f'    @# of dust  : {self.__environment.right_room.dust_count}')
                print(f'    @# of agents: {len(self.__environment.right_agents)}')
                print('  @Scores')

                for agent in self.__agents:
                    print(f'    @agent {agent.ID}: {agent.score}')

                print()

            if not self.__environment.left_room.dirty and not self.__environment.right_room.dirty:
                if verbose:
                    end = default_timer()

                    print('[TERMINATE]')
                    print('  @cause     : Early termination condition is met.')
                    print(f'  @iterations: {i}')
                    print(f'  @elapsed   : {round((end - start) * 1000, 4)}ms')

                return

        if verbose:
            end = default_timer()

            print('[TERMINATE]')
            print('  @cause     : Maximum iteration is reached.')
            print(f'  @iterations: {iteration}')
            print(f'  @elapsed   : {round((end - start) * 1000, 4)}ms')


class ReflexAgent(Agent):
    def __init__(self):
        super(ReflexAgent, self).__init__()
        self.__state = None
        self.__action = None
        self.description = None

    def percept(self, environment):
        if self.location == Location.LEFT:
            self.__state = environment.left_room
        else:
            self.__state = environment.right_room

    def program(self):
        if self.__state.dirty:
            if self.location == Location.LEFT:
                self.__action = lambda x: ReflexAgent.suck(x.left_room)
                self.description = f'Agent {self.ID} sucked a dust at the left room.'
            else:
                self.__action = lambda x: ReflexAgent.suck(x.right_room)
                self.description = f'Agent {self.ID} sucked a dust at the right room.'
        else:
            if self.location == Location.LEFT:
                self.location = Location.RIGHT
                self.__action = lambda x: ReflexAgent.move_right(x, self.ID)
                self.description = f'Agent {self.ID} moved to the right room.'
            else:
                self.location = Location.LEFT
                self.__action = lambda x: ReflexAgent.move_left(x, self.ID)
                self.description = f'Agent {self.ID} moved to the left room.'

    def action(self):
        return self.__action

    @staticmethod
    def suck(room):
        room.dust_count -= 1
        room.dirty = room.dust_count != 0

    @staticmethod
    def move_right(environment, ID):
        environment.right_agents[ID] = environment.left_agents[ID]
        environment.left_agents.pop(ID)

    @staticmethod
    def move_left(environment, ID):
        environment.left_agents[ID] = environment.right_agents[ID]
        environment.right_agents.pop(ID)


if __name__ == '__main__':
    agents = [ReflexAgent() for i in range(100)]
    simulator = Simulator(Environment(left_agents=agents), agents)
    simulator.run()

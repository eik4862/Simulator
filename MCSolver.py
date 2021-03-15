from queue import *
from timeit import *


class State:
    def __init__(self, missionaries, cannibals):
        self.missionaries = missionaries
        self.cannibals = cannibals


class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent

    def __eq__(self, other):
        return self.state == other.state


class MCSolver:
    def __init__(self):
        self.__frontier = Queue()
        self.__explored = []
        self.__missionaries = 0
        self.__cannibals = 0
        self.__capacity = 0
        self.__candidates = []

    def __actions(self, state):
        valid_actions = []

        for dm, dc in self.__candidates:
            if 0 <= state.cannibals + dc <= state.missionaries + dm <= self.__missionaries and \
                    state.cannibals + dc <= self.__cannibals and \
                    state.missionaries + dm - state.cannibals - dc <= self.__missionaries - self.__cannibals:
                valid_actions.append((dm, dc))

        return valid_actions

    def __goal_test(self, state):
        return state.cannibals == state.missionaries == 0

    def __solution(self, node):
        return [] if node.parent is None else self.__solution(node.parent) + [node.action]

    def solve(self, missionaries, cannibals, capacity, verbose=False):
        self.__frontier.queue.clear()
        self.__missionaries = missionaries
        self.__cannibals = cannibals
        self.__capacity = capacity
        self.__candidates.clear()

        for i in range(capacity):
            self.__candidates += [(j, i - j + 1) for j in range(i + 2)] + [(-j, j - i - 1) for j in range(i + 2)]

        if verbose:
            node_counter = 1
            start = default_timer()

            print('### MISSIONARY & CANNIBAL PROBLEM SOLVER ###')
            print('[PROBLEM DESCRIPTION]')
            print(f'  @missionaries : {self.__missionaries}')
            print(f'  @cannibals    : {self.__cannibals}')
            print(f'  @boat capacity: {self.__capacity}')
            print()

        node = Node(State(self.__missionaries, self.__cannibals))

        if self.__goal_test(node.state):
            if verbose:
                print('[TERMINATE SEARCH]')
                print('  @cause     : Solution is found.')
                print(f'  @# of nodes: {node_counter}')
                print(f'  @elapsed   : {round((default_timer() - start) * 1000, 4)}ms')

            return self.__solution(node)

        self.__frontier.put(node)

        while True:
            if self.__frontier.empty():
                if verbose:
                    print('[TERMINATE SEARCH]')
                    print('  @cause     : Failed to find solution.')
                    print(f'  @# of nodes: {node_counter}')
                    print(f'  @elapsed   : {round((default_timer() - start) * 1000, 4)}ms')

                return None

            node = self.__frontier.get()

            if self.__goal_test(node.state):
                if verbose:
                    print('[TERMINATE SEARCH]')
                    print('  @cause     : Solution is found.')
                    print(f'  @# of nodes: {node_counter}')
                    print(f'  @elapsed   : {round((default_timer() - start) * 1000, 4)}ms')

                return self.__solution(node)

            self.__explored.append(node)

            for dm, dc in self.__actions(node.state):
                if verbose:
                    node_counter += 1

                child = Node(State(node.state.missionaries + dm, node.state.cannibals + dc), (dm, dc), node)

                if child not in self.__explored:
                    self.__frontier.put(child)


if __name__ == '__main__':
    solver = MCSolver()
    solution = solver.solve(6, 4, 2, True)
    print(solution)


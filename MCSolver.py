from queue import *
from timeit import *


class State:
    def __init__(self, missionaries, cannibals):
        self.missionaries = missionaries
        self.cannibals = cannibals

    def move(self, dm, dc):
        return State(self.missionaries + dm, self.cannibals + dc)

    def __eq__(self, other):
        return self.missionaries == other.missionaries and self.cannibals == other.cannibals


class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent

    def __eq__(self, other):
        return self.state == other.state


class MCSolver:
    def __actions(self, state):
        valid_actions = []

        for dm, dc in [(-2, 0), (-1, -1), (0, -2), (-1, 0), (0, -1), (2, 0), (1, 1), (0, 2), (1, 0), (0, 1)]:
            if 0 <= state.cannibals + dc == state.missionaries + dm <= 3:
                valid_actions.append((dm, dc))

        return valid_actions

    def __goal_test(self, state):
        return state.cannibals == state.missionaries == 0

    def __solution(self, node):
        return [] if node.parent is None else self.__solution(node.parent) + [node.action]

    def solve(self, verbose=False):
        frontier = Queue()
        explored = []
        visited_node = queue_size = 0

        if verbose:
            start = default_timer()

            print('### MISSIONARY & CANNIBAL PROBLEM SOLVER ###')

        node = Node(State(3, 3))
        visited_node += 1

        if self.__goal_test(node.state):
            solution = self.__solution(node)

            if verbose:
                print('[SEARCH FINISHED]')
                print('  @cause        : Solution is found.')
                print(f'  @visited nodes: {visited_node}')
                print(f'  @memory use   : {queue_size + len(explored)}')
                print(f'  @elapsed      : {round((default_timer() - start) * 1000, 4)}ms')
                print()
                print('[SOLUTION]')
                print(f'  @move 1: {solution[0]}')

            return solution

        frontier.put(node)
        queue_size = max(queue_size, frontier.qsize())

        while True:
            if frontier.empty():
                if verbose:
                    print('[SEARCH FINISHED]')
                    print('  @cause        : Failed to find solution.')
                    print(f'  @visited nodes: {visited_node}')
                    print(f'  @memory use   : {queue_size + len(explored)}')
                    print(f'  @elapsed      : {round((default_timer() - start) * 1000, 4)}ms')

                return None

            node = frontier.get()
            queue_size = max(queue_size, frontier.qsize())

            if self.__goal_test(node.state):
                solution = self.__solution(node)

                if verbose:
                    print('[SEARCH FINISHED]')
                    print('  @cause        : Solution is found.')
                    print(f'  @visited nodes: {visited_node}')
                    print(f'  @memory use   : {queue_size + len(explored)}')
                    print(f'  @elapsed      : {round((default_timer() - start) * 1000, 4)}ms')
                    print()
                    print('[SOLUTION]')

                    for i in range(len(solution)):
                        print(f'  @move {i + 1}: {solution[i]}')

                return solution

            explored.append(node)

            for dm, dc in self.__actions(node.state):
                child = Node(node.state.move(dm, dc), (dm, dc), node)
                visited_node += 1

                if child not in explored:
                    frontier.put(child)
                    queue_size = max(queue_size, frontier.qsize())


if __name__ == '__main__':
    solver = MCSolver()
    solution = solver.solve(True)

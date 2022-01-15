import copy
import heapq

from typing import List


class Node:
    def __init__(self, info: list, parent, cost=0, h=0):
        self.info = info
        self.parent = parent
        self.cost = cost
        self.h = h
        self.f = self.cost + self.h

    def get_path(self):
        path = [self]
        node = self
        while node.parent is not None:
            path.insert(0, node.parent)
            node = node.parent
        return path

    def print_path(self, print_cost=False, print_path=False):
        path = self.get_path()
        for node in path:
            print(node)
        if print_cost:
            print(f'Node cost {self.cost}')
        if print_path:
            print(f'Length: {len(path)}')

    def is_contained_in_path(self, info_new_node):
        node = self
        while node is not None:
            if info_new_node == node.info:
                return True
            node = node.parent
        return False

    def __repr__(self):
        return str(self.info)

    def __str__(self):
        s = ''
        for line in self.info:
            s += ' '.join([str(element) for element in line]) + '\n'
        return s

    def __lt__(self, other):
        return self.f < other.f


class Graph:
    def __init__(self, file_name: str):
        with open(file_name, 'r') as handler:
            file_content = handler.read()
            l_list = file_content.strip().split('\n')
            self.start = []
            for line in l_list:
                self.start.append([int(x) for x in line.strip().split(' ')])
            print(f'Start state: {self.start}')
            # integrity check
            self.scopes = [[[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
            print(f'Scopes: {self.scopes}')

    def get_scope_status(self, node: Node) -> bool:
        return node.info in self.scopes

    def get_successors(self, node: Node, h_type='euristica banala') -> List[Node]:
        s_list = []
        for l_empty in range(len(node.info)):
            try:
                c_empty = node.info[l_empty].index(0)
                break
            except ValueError as exception:
                pass
                # 0 as a *wildcard has not been found on
                # the line with the index l_empty
                #print(f'Index exception occurred!: {str(exception)}')
        directions = [[l_empty, c_empty - 1],
                      [l_empty, c_empty + 1],
                      [l_empty - 1, c_empty],
                      [l_empty + 1, c_empty]]
        for l_move, c_move in directions:
            if 0 <= l_move < 3 and 0 <= c_move < 3:
                matrix_copy = copy.deepcopy(node.info)
                matrix_copy[l_empty][c_empty] = matrix_copy[l_move][c_move]
                matrix_copy[l_move][c_move] = 0
                if not node.is_contained_in_path(matrix_copy):
                    arc_cost = 1
                    new_node_g = node.cost + arc_cost
                    new_node_h = self.compute_h(matrix_copy, h_type)
                    new_node = Node(matrix_copy, node, new_node_g, new_node_h)
                    s_list.append(new_node)
        return s_list

    def compute_h(self, info_node: list, h_type='euristica banala') -> int:
        if info_node in self.scopes:
            return 0
        if h_type == 'euristica banala':
            return 1
        else:
            h = 0
            for l_move in range(len(info_node)):
                for c_move in range(len(info_node[0])):
                    if info_node[l_move][c_move] != 0:
                        move = info_node[l_move][c_move]
                        l_move_f = (move - 1)//len(info_node[0])
                        c_move_f = (move - 1)%len(info_node[0])
                        h += abs(l_move_f - l_move) + abs(c_move_f - c_move)
            return h

    def __repr__(self):
        s = ''
        for (k, v) in self.__dict__.items():
            s += f'{k} = {v}'
        return s

    @staticmethod
    def there_are_no_solutions(info_node) -> int:
        matrix_list = sum(info_node, [])
        no_inversions = 0
        for i in range(len(matrix_list)):
            if matrix_list[i] != 0:
                for j in range(i + 1, len(matrix_list)):
                    if matrix_list[j] != 0:
                        if matrix_list[i] > matrix_list[j]:
                            no_inversions += 1
        return no_inversions % 2 == 1


def breadth_first(graph: Graph, n: int = 1):
    start = Node(graph.start, None)
    open_list = [start]

    while len(open_list):
        current_node = open_list.pop(0)

        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path(print_cost=True, print_path=True)
            print('----------------------\n')
            input()
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node)
        open_list.extend(s_list)


def uniform_cost(graph: Graph, n: int):
    start = Node(graph.start, None, 0, graph.compute_h(graph.start))
    open_list = [start]

    while len(open_list) > 0:
        print(f'Current queue: {str(open_list)}')
        input()
        current_node = heapq.heappop(open_list)

        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path()
            print('----------------------\n')
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node)
        for s in s_list:
            heapq.heappush(open_list, s)


def a_star(graph: Graph, n: int, h_type: str = 'euristica banala'):
    if graph.there_are_no_solutions(graph.start):
        print('There are no solutions!')
        return

    start = Node(graph.start, None, 0, graph.compute_h(graph.start))
    open_list = [start]
    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path(print_cost=True, print_path=True)
            print('---------------------------\n')
            input()
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node, h_type=h_type)
        for s in s_list:
            heapq.heappush(open_list, s)


if __name__ == '__main__':
    graph = Graph('resources/8-puzzle.txt')
    # a_star(graph, n=1)
    breadth_first(graph)


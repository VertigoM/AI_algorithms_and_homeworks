import copy
import heapq
import os
import time

from typing import List


class Node:
    '''
        @ :param info   := the list of lists associated with the grid
        @ :param parent := the parent node of the current node
        @ :param cost   := parent.cost + 1
        @ :param h      := computed heuristic value
    '''

    def __init__(self, info: List, parent, cost=0, h=0):
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
            # dimension of the grid read from the file
            self.n = len(self.start)
            print(f'Start state: {self.start}')

    # function which determines if the current state of the puzzle
    # is the desired final state
    def get_scope_status(self, info: List[List[int]]) -> bool:
        for l_index in range(len(info)):
            # compare the two halves and return False if they are not symmetrical
            if info[l_index][:self.n // 2] != info[l_index][self.n // 2 + (self.n & 1):][::-1]:
                return False
        return True

    def get_successors(self, node: Node, h_type='heuristic_1', debug: bool = False) -> List[Node]:
        # empty list of successors
        s_list = []
        # for every line of the grid
        for l_empty in range(len(node.info)):
            try:
                # try to determine if the wildcard is on the
                # line of index l_empty
                c_empty = node.info[l_empty].index(0)
                break
            except ValueError as exception:
                pass
                # 0 as a *wildcard has not been found on
                # the line with the index l_empty
        # the ways a wildcard can travel
        directions = Graph.get_directions(l_empty, c_empty)
        # for every possible move
        for l_move, c_move in directions:
            # check if the indices are valid or not
            if self.get_move_validity(node.info, l_empty, c_empty, l_move, c_move):
                # get a deep copy of the current grid state
                matrix_copy = copy.deepcopy(node.info)
                # switch values between the wildcard and value at indices (l_move, c_move)
                matrix_copy[l_empty][c_empty], matrix_copy[l_move][c_move] = matrix_copy[l_move][c_move], \
                                                                             matrix_copy[l_empty][c_empty]
                # if the new configuration has not been tried yet
                # compute it as a new node and add it to the successors list
                if not node.is_contained_in_path(matrix_copy):
                    # compute the cost of the move as the sum
                    # of the line of which the value is moved
                    # and the value itself
                    arc_cost = l_empty + node.info[l_move][c_move]
                    new_node_g = node.cost + arc_cost
                    new_node_h = self.compute_h(matrix_copy, h_type)
                    new_node = Node(matrix_copy, node, new_node_g, new_node_h)
                    if debug:
                        print(
                            f'[DEBUG] Valid successor found:\n{new_node}\nPATH:\n{new_node.print_path(print_path=True)}')
                    s_list.append(new_node)
        return s_list

    def compute_h(self, info_node: List, h_type='heuristic_1') -> int:
        # if the new node represents a desired final state then return 0
        if self.get_scope_status(info_node):
            return 0
        # compute the number of values which are different
        # from their counterpart
        if h_type == 'heuristic_1':
            # the minimal cost of a move
            return 1
        elif h_type == 'heuristic_2':
            h = 0
            for line_index in range(self.n):
                first_half = info_node[line_index][:self.n // 2]
                second_half = info_node[line_index][self.n // 2 + (self.n & 1):][::-1]
                h += sum([1 if e1 == e2 else 0 for e1, e2 in zip(first_half, second_half)])
            return h
        elif h_type == 'heuristic_3':
            h = 0
            for line_index in range(self.n):
                # search only on the left side of the grid
                for column_index in range(self.n // 2):
                    x, y = self.get_value_coordinates(info_node, line_index, column_index)
                    print(x, y)
                    req_x, req_y = line_index, self.n - column_index - 1
                    # compute the manhattan distance between
                    # the current position of the pair element
                    # and the required position

                    # how many lines the element has to be moved
                    req_moves_x = abs(x - req_x)

                    # how many columns the element has to be moved
                    req_moves_y = abs(y - req_y)
                    h += (req_moves_x + req_moves_y)
            return h

    def get_value_coordinates(self, info_node: List[List[int]], line_index: int, column_index: int) -> (int, int):
        searched_value = info_node[line_index][column_index]
        for x in range(self.n):
            try:
                y = info_node[x].index(searched_value)
                if x != line_index or y != column_index:
                    break
            except ValueError as exception:
                pass
        return x, y

    '''
    @ :param l_empty, c_empty   := current coordinates of the wildcard
    @ :param l_move, c_move     := coordinates at which wildcard is moved to
    '''

    def get_move_validity(self, matrix: List[List[int]], l_empty: int, c_empty: int, l_move: int, c_move: int,
                          debug: bool = False) -> bool:
        if not (0 <= l_move < self.n and 0 <= c_move < self.n):
            return False
        moved_value = matrix[l_move][c_move]
        # check whether the current move is valid or not
        # count the neighbor values with different parities
        neighbors = Graph.get_directions(l_empty, c_empty)
        # coordinates of the neighbors
        parity = 0
        for x_move, y_move in neighbors:
            if debug:
                print(f'[DEBUG] Testing for coordinates: {x_move} {y_move}')
            # check for the coordinates to be valid
            if 0 <= x_move < self.n and 0 <= y_move < self.n and (x_move != l_move or y_move != c_move):
                # if value is not the wildcard
                if debug:
                    print(f'[DEBUG] Matrix: {matrix}')
                if matrix[x_move][y_move] != 0:
                    # decrement parity if neighbor is odd else increment
                    parity += -1 if (matrix[x_move][y_move] & 1) else 1
        if debug:
            print(f'[DEBUG] Parity: {parity}')
        if (parity < 0) != ((-1 if (moved_value & 1) else 1) < 0):
            # check the above line neighbors for a bigger value of opposite parity
            above_line = l_empty - 1
            if above_line >= 0:
                for value in matrix[above_line][(0 if (c_empty - 1) < 0 else (c_empty - 1)):(c_empty + 3)]:
                    if (value > moved_value) and ((value & 1) != (moved_value & 1)):
                        if debug:
                            print(f'[DEBUG] Invalid move! {(l_empty, c_empty)} to {(l_move, c_move)}')
                        return False
        return True

    @staticmethod
    def get_directions(x: int, y: int) -> List[List[int]]:
        directions = [[x, y + 1],       # -> (0, 1)
                      [x - 1, y + 1],   # -> (-1, 1)
                      [x - 1, y],       # -> (-1, 0)
                      [x - 1, y - 1],   # -> (-1, -1)
                      [x, y - 1],       # -> (0, -1)
                      [x + 1, y - 1],   # -> (1, -1)
                      [x + 1, y],       # -> (0, -1)
                      [x + 1, y + 1]]   # -> (1, 1)
        return directions

    def __repr__(self):
        s = ''
        for (k, v) in self.__dict__.items():
            s += f'{k} = {v}'
        return s

    @staticmethod
    def there_are_no_solutions(info_node) -> int:
        # TODO: implement a way to find out whether a grid has a solution or not
        return False


class PuzzleSolver:
    def __init__(self, input_path: str, output_path: str, no_required_solutions: int, timeout_value: int):
        self.input_path = input_path
        self.output_path = output_path
        self.graph = Graph('dir_in/8-puzzle.txt')
        self.no_requierd_solutions = no_required_solutions
        self.timeout_value = timeout_value

    def breadth_first(self):
        start = Node(self.graph.start, None)
        if Graph.there_are_no_solutions(start.info):
            print('There are no solutions!')
            return
        open_list = [start]

        n = self.no_requierd_solutions
        while len(open_list):
            current_node = open_list.pop(0)

            if self.graph.get_scope_status(current_node.info):
                print('Solution found! Printing path...')
                current_node.print_path(print_cost=True, print_path=True)
                print('----------------------\n')
                input()
                n -= 1
                if n == 0:
                    return
            s_list = self.graph.get_successors(current_node)
            open_list.extend(s_list)

    def uniform_cost(self):
        start = Node(self.graph.start, None, 0, self.graph.compute_h(self.graph.start))
        open_list = [start]

        n = self.no_requierd_solutions
        while len(open_list) > 0:
            current_node = heapq.heappop(open_list)

            if self.graph.get_scope_status(current_node.info):
                print('Solution: ')
                current_node.print_path()
                print('----------------------\n')
                n -= 1
                if n == 0:
                    return
            s_list = self.graph.get_successors(current_node)
            for s in s_list:
                heapq.heappush(open_list, s)

    def a_star(self, h_type: str = 'heuristic_1'):
        graph = self.graph
        no_required_solutions = self.no_requierd_solutions

        if graph.there_are_no_solutions(graph.start):
            print('There are no solutions!')
            return

        start = Node(graph.start, None, 0, graph.compute_h(graph.start))
        # initialize the open list with the start node
        open_list = [start]
        # while open list is not empty

        n = no_required_solutions
        while open_list:
            # get the head of the list which will always be
            # the node with the smallest f score
            current_node = heapq.heappop(open_list)
            if graph.get_scope_status(current_node.info):
                print('Solution: ')
                current_node.print_path(print_cost=True, print_path=True)
                filepath = f'{self.output_path}/solution_{no_required_solutions - n + 1}.txt'

                # check if the file already exists at the
                # destination directory
                if os.path.exists(filepath):
                    print('File already exists;\nReplacing...')
                    os.remove(filepath)

                with open(filepath, 'w') as handler:
                    handler.write('Solution obtained using A*\n')
                    for node in current_node.get_path():
                        handler.write(str(node))
                        handler.write('\n')

                print('---------------------------\n')
                input()
                # decrement the number of desired solutions
                n -= 1
                if n == 0:
                    return
            # get the child nodes of the current node
            s_list = graph.get_successors(current_node, h_type=h_type)
            for s in s_list:
                # used as seen @ https://docs.python.org/3.8/library/heapq.html
                heapq.heappush(open_list, s)

    # throws RecursionError: maximum recursion depth exceeded
    # while calling a Pyhton object
    def depth_first(self):
        start = Node(self.graph.start, None)
        n = self.no_requierd_solutions
        try:
            self.df(start, n)
        except RecursionError as exception:
            print(str(exception))

    def df(self, node: Node, n: int):
        if n <= 0:
            return n
        if self.graph.get_scope_status(node.info):
            print('Solution: ')
            node.print_path()
            print('------------------------\n')
            input()
            n -= 1
            if n == 0:
                return n
        s_list = self.graph.get_successors(node)
        for s in s_list:
            if n != 0:
                n = self.df(s, n)
        return n

    def optimized_a_star(self):
        graph = self.graph
        no_required_solutions = self.no_requierd_solutions
        n = self.no_requierd_solutions

        start = Node(graph.start, None, 0, graph.compute_h(graph.start))
        open_list = [start]
        closed_list = []
        while open_list:
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)
            if graph.get_scope_status(current_node.info):
                print('Solution: ')
                current_node.print_path(print_cost=True, print_path=True)
                filepath = f'{self.output_path}/solution_{no_required_solutions - n + 1}.txt'

                # check if the file already exists at the
                # destination directory
                if os.path.exists(filepath):
                    print('File already exists;\nReplacing...')
                    os.remove(filepath)

                with open(filepath, 'w') as handler:
                    handler.write('Solution obtained using optimized A*\n')
                    for node in current_node.get_path():
                        handler.write(str(node))
                        handler.write('\n')

                print('----------------------\n')
                input()
                n -= 1
                if n == 0:
                    return
            s_list = graph.get_successors(current_node)
            # can be re-written better with closed list as a min-heap
            # heapq implementation - see A* algorithm
            for s in s_list:
                found = False
                for node in open_list:
                    if s.info == node.info:
                        found = True
                        if s.f >= node.f:
                            s_list.remove(s)
                        else:
                            open_list.remove(node)
                        # break because a node cannot appear twice inside open list
                        break
                if not found:
                    for node in closed_list:
                        if s.info == node.info:
                            if s.f >= node.f:
                                s_list.remove(s)
                            else:
                                closed_list.remove(node)
                            break

            for child_node in s_list:
                heapq.heappush(open_list, child_node)

    # implemented as seen @ https://en.wikipedia.org/wiki/Iterative_deepening_A*
    def ida_star(self):
        graph = self.graph
        no_required_solutions = self.no_requierd_solutions
        n = self.no_requierd_solutions

        start = Node(graph.start, None, 0, graph.compute_h(graph.start))
        bound = start.f
        while True:
            print(f'Starting BOUND: {bound}')
            n, result = self.build_path(start, bound, n)
            if result == 'Done':
                break
            if result == float('inf'):
                print('No more solutions')
                break
            bound = result
            print(f'New BOUND: {bound}')

    def build_path(self, current_node: Node, bound: int, n: int):
        if current_node.f > bound:
            return n, current_node.f
        if self.graph.get_scope_status(current_node.info) and current_node.f == bound:
            print('Solution: ')
            current_node.print_path()
            filepath = f'{self.output_path}/solution_{self.no_requierd_solutions - n + 1}.txt'

            # check if the file already exists at the
            # destination directory
            if os.path.exists(filepath):
                print('File already exists;\nReplacing...')
                os.remove(filepath)

            with open(filepath, 'w') as handler:
                handler.write('Solution obtained using IDA*\n')
                for node in current_node.get_path():
                    handler.write(str(node))
                    handler.write('\n')
            print(bound)
            print('------------------------------\n')
            n -= 1
            if n == 0:
                return 0, 'Done'
        # get the list of successors of the current node
        # i.e. for the node of this function call
        s_list = self.graph.get_successors(current_node)
        # minim is initialised with infinity
        mi = float('inf')
        # for every node in the list of successors
        for s in s_list:
            # recursive call with the successor node
            # function will return when a node is either solution
            # or the node has no more successors i.e. it is a
            # leaf in the searching tree
            n, result = self.build_path(s, bound, n)
            # the stack starts to empty
            if result == 'Done':
                return 0, 'Done'
            if result < mi:
                mi = result
        return n, mi


def read_from_dir(read_dir: str = '.'):
    l_input = []
    if os.path.exists(read_dir):
        l_input.extend(os.listdir(read_dir))
    else:
        raise Exception('Required path does not exist on the system! Enter a new valid path!')


if __name__ == '__main__':
    input_path = input('Enter input path: ')
    input_files = read_from_dir(input_path)
    output_path = input('Enter output path: ')

    # check against FileExistsError
    if not os.path.exists(output_path):
        print('Output directory doesn\'t exist! Creating...')
        os.mkdir(path=output_path)
        print(f'Directory {output_path} created!')

    # the number of required solutions
    n = int(input('Enter the number of required solutions: '))
    # the no of seconds after the program halts
    # even if a solution has not been found
    timeout = int(input('Enter the number of seconds after which the program will timeout: '))

    puzzle_solver = PuzzleSolver(input_path, output_path, n, timeout)
    start_time = time.time()
    #puzzle_solver.a_star(h_type='heuristic_1')
    #puzzle_solver.uniform_cost()
    #puzzle_solver.depth_first()
    #puzzle_solver.optimized_a_star()
    puzzle_solver.ida_star()
    print("--- %s seconds---" % (time.time() - start_time))
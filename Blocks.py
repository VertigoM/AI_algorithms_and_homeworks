import copy
import heapq


class Node:
    def __init__(self, info, parent, cost=0, h=0):
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
        max_height = max([len(stack) for stack in self.info])
        for height in range(max_height, 0, -1):
            for stack in self.info:
                if len(stack) < height:
                    s += ' '
                else:
                    s += stack[height - 1] + ' '
            s += '\n'
        s += '-'*(2 * len(self.info) - 1)
        return s

    def __lt__(self, other):
        return self.f < other.f


class Graph:
    def __init__(self, file_name: str):
        with open(file_name, 'r') as handler:
            file_content = handler.read()
            states = file_content.split('stari_finale')
            self.start = Graph.get_stacks(states[0])
            self.scopes = []
            final_states = states[1].strip().split('---')
            for scope in final_states:
                self.scopes.append(Graph.get_stacks(scope))
            print(f'Initial state: {self.start}')
            print(f'Possible states: {self.scopes}')
            input()

    def get_scope_status(self, node):
        return node.info in self.scopes

    def get_successors(self, node: Node, h_type='euristica banala'):
        s_list = []
        # stacks inside the current node
        current_stacks = node.info
        # index of the stack which is going to be modified
        # i.e. a node is removed
        for index in range(len(current_stacks)):
            if len(current_stacks[index]) == 0:
                continue
            intern_copy = copy.deepcopy(current_stacks)
            block = intern_copy[index].pop()
            # index of the stack which is going to receive a new block
            for j in range(len(current_stacks)):
                # a block cannot be placed from the same stack
                # from which it has been removed
                if index == j:
                    continue
                # the new list of stacks
                new_stacks = copy.deepcopy(intern_copy)
                # the block is placed on the stack
                # of the new list of stacks
                new_stacks[j].append(block)
                move_block_cost = 1 + ord(block) - ord('a')
                if not node.is_contained_in_path(new_stacks):
                    cost = node.cost + move_block_cost
                    h = self.compute_h(new_stacks, h_type)
                    new_node = Node(new_stacks, node, cost, h)
                    s_list.append(new_node)
        return s_list

    def compute_h(self, info_node, h_type='euristica banala'):
        if h_type == 'euristica banala':
            if info_node in self.scopes:
                # minimal cost of a move
                return 1
            return 0
        elif h_type == 'euristica admisibila 1':
            # it is computed how many blocks are on different
            # positions other than those from the scope states
            h_list = []
            for (i_scope, scope) in enumerate(self.scopes):
                h = 0
                for i_stack, stack in enumerate(info_node):
                    for i_element, element in enumerate(stack):
                        try:
                            # i_element exists but the element on that
                            # position is not equal with the desired element
                            if element != scope[i_stack][i_element]:
                                # adding the minimal cost of a move
                                h += 1
                        except IndexError:
                            # i_element doesn't exist for scope[i_stack]
                            h += 1
                h_list.append(h)
            return min(h_list)
        elif h_type == 'euristica admisibila 2':
            # it is computed how many blocks are on different
            # positions other than those from teh scope states
            h_list = []
            for (i_scope, scope) in enumerate(self.scopes):
                h = 0
                for i_stack, stack in enumerate(info_node):
                    for i_element, element in enumerate(stack):
                        try:
                            # i_element exists but the element on that
                            # position is not equal with the desired element
                            if element != scope[i_stack][i_element]:
                                h += 1
                            else:
                                # element is equal with the desired element on that position
                                # but the blocks underneath are not

                                # at least two moves are necessary to move each block
                                # to another stack and than move them back on the original
                                # stack, thus the estimation is incremented by two
                                if stack[:i_element] != scope[i_stack][:i_element]:
                                    h += 2
                        except IndexError:
                            # i_element doesn't exist for scope[i_stack]
                            h += 1
                h_list.append(h)
            return min(h_list)
        # h_type == 'euristica inadmisibila'
        else:
            h_list = []
            for (i_scope, scope) in enumerate(self.scopes):
                h = 0
                for i_stack, stack in enumerate(info_node):
                    for i_element, element in enumerate(stack):
                        try:
                            if element != scope[i_stack][i_element]:
                                h += 3
                            else:
                                if stack[:i_element] != scope[i_stack][:i_element]:
                                    h += 2
                        except IndexError:
                            h += 3
                h_list.append(h)
            return max(h_list)

    def __repr__(self):
        s = ''
        for (k, v) in self.__dict__.items():
            s += f'{k} = {v}'
        return s

    @staticmethod
    def get_stacks(text: str) -> list:
        s = text.strip().split('\n')
        s_list = [stack.strip().split() if stack != '#' else [] for stack in s]
        return s_list


def breadth_first(graph: Graph, n: int):
    start_node = Node(graph.start, None)
    open_list = [start_node]

    while len(open_list):
        current_node = open_list.pop(0)

        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path(print_cost=True, print_path=True)
            print('---------------------\n')
            input()
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node)
        open_list.extend(s_list)


# non-optimised A*
def a_star(graph: Graph, n: int, h_type: str):
    start_node = Node(graph.start, None)
    open_list = [start_node]

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path(print_cost=True, print_path=True)
            print('------------------------------\n')
            input()
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node, h_type=h_type)
        for s in s_list:
            heapq.heappush(open_list, s)


if __name__ == '__main__':
    graph = Graph('resources/blocks_input.txt')
    a_star(graph, n=1, h_type='euristica admisibila 1')

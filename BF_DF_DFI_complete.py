class Node:
    def __init__(self, x: int, info: chr, parent):
        self.x = x
        self.info = info
        self.parent = parent

    def get_path(self):
        path = [self.info]
        node = self
        while node.parent is not None:
            path.insert(0, node.parent.info)
            node = node.parent
        return path

    def print_path(self):
        path = self.get_path()
        print('->'.join(path))
        return len(path)

    def is_contained_in_path(self, info_new_node):
        node = self
        while node is not None:
            if info_new_node == node.info:
                return True
            node = node.parent
        return False

    def __repr__(self):
        return f"{self.info}(id = {self.x} path = {'->'.join(self.get_path())})"


class Graph:
    def __init__(self, node_list, adj_matrix, start, graph_scope):
        self.node_list = node_list
        self.adj_matrix = adj_matrix
        self.start = start
        self.scope = graph_scope

    def get_node_index(self, node):
        return self.node_list.index(node)

    def get_scope_status(self, node):
        return node.info in self.scope

    def get_successors(self, node):
        s_list = []
        for i in range(len(self.node_list)):
            if self.adj_matrix[node.x][i] == 1 and not node.is_contained_in_path(self.node_list[i]):
                new_node = Node(i, self.node_list[i], node)
                s_list.append(new_node)
        return s_list

    # see explanation @ https://docs.python.org/3/reference/datamodel.html
    def __repr__(self):
        s = ''
        for (k, v) in self.__dict__.items():
            s += f'{k} = {v}'
        return s


# all implemented algorithms use the same data structure
# for convenience reasons
def breadth_first(graph: Graph, n=1):
    start = Node(graph.get_node_index(graph.start), graph.start, None)
    open_list = [start]

    while len(open_list) > 0:
        print(f'Current path: {open_list}')
        input()
        current_node = open_list.pop()

        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path()
            print('-----------------------\n')
            input()
            n -= 1
            if n == 0:
                return
        # add every child of the node to the list
        s_list = graph.get_successors(current_node)
        open_list.extend(s_list)


def depth_first(graph: Graph, n: int):
    start = Node(graph.get_node_index(graph.start), graph.start, None)
    df(start, n=1)


def df(node: Node, n: int):
    if n <= 0:
        return n
    print(f'Current stack: {"->".join(node.get_path())}')
    input()
    if graph.get_scope_status(node):
        print('Solution: ')
        node.print_path()
        print('------------------------\n')
        input()
        n -= 1
        if n == 0:
            return n
    s_list = graph.get_successors(node)
    for s in s_list:
        if n != 0:
            n = df(s, n)
    return n


def dfi(node: Node, depth: int, n: int):
    print(f'Current stack: {"->".join(node.get_path())}')
    input()
    if depth == 1 and graph.get_scope_status(node):
        print('Solution: ')
        node.print_path()
        print('----------------------\n')
        input()
        n -= 1
        if n == 0:
            return n
    if depth > 1:
        s_list = graph.get_successors(node)
        for s in s_list:
            if n != 0:
                n = dfi(s, depth - 1, n)
    return n


def iterative_depth_first(graph: Graph, n=1):
    start = Node(graph.get_node_index(graph.start), graph.start, None)
    for i in range(1, len(graph.node_list)):
        if n == 0:
            return
        print(f'*************\nMaximum depth: {i}')
        n = dfi(start, i, n)


m = [
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

start_node = 'a'
scope = ['f']
nodes = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]


if __name__ == '__main__':
    graph = Graph(nodes, m, start_node, scope)
    #breadth_first(graph, n=1)
    #depth_first(graph, n=1)
    iterative_depth_first(graph, n=1)

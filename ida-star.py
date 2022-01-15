from Node import Node
from Graph import Graph

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

mp = [
    [0, 3, 9, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 10, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 1, 0, 0, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 7, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start_node = 'a'
scope = ['f']
h_list = [0, 10, 3, 7, 8, 0, 14, 3, 1, 2]
nodes = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]


# implemented as seen @ https://en.wikipedia.org/wiki/Iterative_deepening_A*
def ida_star(graph: Graph, n: int):
    start = Node(graph.get_node_index(graph.start), graph.start, None, 0, graph.compute_h(graph.start))
    bound = start.f
    while True:
        print(f'Starting BOUND: {bound}')
        n, result = build_path(graph, start, bound, n)
        if result == 'Done':
            break
        if result == float('inf'):
            print('No more solutions')
            break
        bound = result
        print(f'New BOUND: {bound}')


def build_path(graph: Graph, node: Node, bound: int, n: int):
    print(f'Current node: {node}')
    if node.f > bound:
        return n, node.f
    if graph.get_scope_status(node) and node.f == bound:
        print('Solution: ')
        node.print_path()
        print(bound)
        print('------------------------------\n')
        n -= 1
        if n == 0:
            return 0, 'Done'
    # get the list of successors of the current node
    # i.e. for the node of this function call
    s_list = graph.get_successors(node)
    # minim is initialised with infinity
    mi = float('inf')
    # for every node in the list of successors
    for s in s_list:
        # recursive call with the successor node
        # function will return when a node is either solution
        # or the node has no more successors i.e. it is a
        # leaf in the searching tree
        n, result = build_path(graph, s, bound, n)
        # the stack starts to empty
        if result == 'Done':
            return 0, 'Done'
        print(f'Compare {result} with {mi}:')
        if result < mi:
            mi = result
            print(f'New minim: {mi}')
    return n, mi


if __name__ == '__main__':
    graph = Graph(nodes, m, mp, start_node, scope, h_list)
    ida_star(graph, n=1)

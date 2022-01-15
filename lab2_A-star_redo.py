from Node import Node
from Graph import Graph
import heapq

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


# n := the number of desired solutions
def a_star(graph: Graph, n: int):
    start = Node(graph.get_node_index(graph.start), graph.start, None, 0, graph.compute_h(graph.start))
    # Initialize open list with the start node
    open_list = [start]
    # while open list is not empty
    while open_list:
        print('Current open list: ' + str(open_list))
        # pause between iterations
        input()
        # get the head of the list which will always be
        # the node with the least f score
        current_node = heapq.heappop(open_list)
        # if the current node is amongst the searched
        # nodes, we have found a solution
        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path()
            input()
            # decrement the number of desired solutions
            n -= 1
            if n == 0:
                return
        # get the child nodes of the current node
        s_list = graph.get_successors(current_node)
        for child_node in s_list:
            # used as seen @ https://docs.python.org/3.8/library/heapq.html
            heapq.heappush(open_list, child_node)


def optimized_a_star(graph: Graph, n: int):
    start = Node(graph.get_node_index(graph.start), graph.start, None, 0, graph.compute_h(graph.start))
    open_list = [start]
    closed_list = []
    while open_list:
        print('Current open list: ' + str(open_list))
        input()
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        if graph.get_scope_status(current_node):
            print('Solution: ')
            current_node.print_path()
            input()
            n -= 1
            if n == 0:
                return
        s_list = graph.get_successors(current_node)
        # can be re-written better with closed list as a min-heap
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


if __name__ == '__main__':
    graph = Graph(nodes, m, mp, start_node, scope, h_list)
    #a_star(graph, n=1)
    optimized_a_star(graph, n=1)

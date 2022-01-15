from Node import Node


class Graph:
    def __init__(self, node_list, adj_matrix, w_matrix, start, scope, h_list):
        self.node_list = node_list
        self.adj_matrix = adj_matrix
        self.w_matrix = w_matrix
        self.start = start
        self.scope = scope
        self.h_list = h_list

    def get_node_index(self, node):
        return self.node_list.index(node)

    def get_scope_status(self, node):
        return node.info in self.scope

    def compute_h(self, info_node):
        return self.h_list[self.get_node_index(info_node)]

    def get_successors(self, node):
        s_list = []
        for i in range(len(self.node_list)):
            if self.adj_matrix[node.x][i] == 1 and not node.is_contained_in_path(self.node_list[i]):
                new_node_g = node.g + self.w_matrix[node.x][i]
                new_node_h = self.compute_h(self.node_list[i])
                new_node = Node(i, self.node_list[i], node, new_node_g, new_node_h)
                s_list.append(new_node)
        return s_list

    # see explanation @ https://docs.python.org/3/reference/datamodel.html
    def __repr__(self):
        s = ''
        for (k, v) in self.__dict__.items():
            s += f'{k} = {v}'
        return s

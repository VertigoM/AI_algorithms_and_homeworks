class Node:
    def __init__(self, x, info, parent, g, h):
        self.x = x
        self.info = info
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h

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
        print('Cost: ', self.g)
        return len(path)

    def is_contained_in_path(self, info_new_node):
        node = self
        while node is not None:
            if info_new_node == node.info:
                return True
            node = node.parent
        return False

    def __repr__(self):
        return f"{self.info}(id = {self.x} path = {'->'.join(self.get_path())} g={self.g} h={self.h} f={self.f})"

    # less than function - used for heap sorting
    def __lt__(self, other):
        return self.f < other.f

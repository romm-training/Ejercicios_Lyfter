class Node:
    data : str

    def __init__(self, data, left_child=None, right_child=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child

class binary_tree():
    root : Node

    def __init__(self, root):
        self.root = root

    def _print_children(self, node):
        print(node.data)
        if node.left_child != None:
            self._print_children(node.left_child)
        if node.right_child != None:
            self._print_children(node.right_child)

    def print_structure(self):
        self._print_children(self.root)    

def main():
    node_j = Node("NodeJ")
    node_i = Node("NodeI")
    node_h = Node("NodeH")
    node_g = Node("NodeG")
    node_f = Node("NodeF")
    node_e = Node("NodeE", node_j)
    node_d = Node("NodeD", node_h, node_i)
    node_c = Node("NodeC", node_f, node_g)
    node_b = Node("NodeB", node_d, node_e)
    node_a = Node("NodeA", node_b, node_c)

    bin_tree = binary_tree(node_a)

    bin_tree.print_structure()

if __name__ == "__main__":
    main()
class LinkedList:
    head: None

    def __init__(self, head, next=None):
        self.head = head

    def print_structure(self):
        current_node = self.head

        while (current_node is not None):
            print(current_node.data)
            current_node = current_node.next

class Node:
    data: str
    next: "Node"
    
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

third_node = Node("Tercer nodo")
second_node = Node("Segundo nodo",third_node)
first_node = Node("Primer nodo", second_node)

linkedList = LinkedList(first_node)
linkedList.print_structure()
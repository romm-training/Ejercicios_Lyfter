class Node:
    data: str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    head: Node

    def __init__(self, head):
        self.head = head

    def print_structure(self):
        current_node = self.head
        while current_node != None:
            print(current_node.data)
            current_node = current_node.next

class Queue(LinkedList):
    def enqueue(self, new_node):
        current_node = self.head
        next_node = current_node.next

        while (next_node is not None):
            current_node = next_node
            next_node = current_node.next

        current_node.next = new_node
        
    def dequeue(self):
        self.head = self.head.next


node3 = Node("Node3")
node2 = Node("Nodo2", node3)
node1 = Node("Nodo1", node2)

my_queue = Queue(node1)

my_queue.print_structure()
print("")

my_queue.enqueue(Node("Nodo4"))
my_queue.enqueue(Node("Nodo5"))

my_queue.print_structure()
print("")
my_queue.dequeue()


print("")
my_queue.print_structure()
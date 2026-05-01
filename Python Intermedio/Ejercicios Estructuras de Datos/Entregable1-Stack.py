class Node:
    data : str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    head : Node

    def __init__(self, head):
        self.head = head

    def print_structure(self):
        current_node = self.head

        while current_node != None:
            print(current_node.data)
            current_node = current_node.next

class Stack(LinkedList):
    def push(self, node):
        current_node = self.head
        self.head = node
        self.head.next = current_node

    def pop(self):
        self.head = self.head.next

print("Agregando nodo")
node1 = Node("Nodo1")
my_stack = Stack(node1)
my_stack.print_structure()
print("")

print("Agregando nodo")
node2 = Node("Node2")
my_stack.push(node2)
my_stack.print_structure()
print("")

print("Agregando nodo")
node3 = Node("Node3")
my_stack.push(node3)
my_stack.print_structure()
print("")

print("Agregando nodo")
node4 = Node("Node4")
my_stack.push(node4)
my_stack.print_structure()
print("")

print("Agregando nodo")
node5 = Node("Node5")
my_stack.push(node5)
my_stack.print_structure()
print("")

print("Quitando nodo")
my_stack.pop()
my_stack.print_structure()
print("")

print("Quitando nodo")
my_stack.pop()
my_stack.print_structure()
print("")

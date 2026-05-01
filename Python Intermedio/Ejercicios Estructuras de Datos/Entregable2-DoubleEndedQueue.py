class Node:
    data : str

    def __init__(self, data, next=None, previous=None):
        self.data = data
        self.next = next
        self.previous = previous

class LinkedList:
    head : Node

    def __init__(self, head):
        self.head = head

    def print_structure(self):
        current_node = self.head

        if current_node == None:
            print("La estructura esta vacia.")
            return
        
        while current_node != None:
            print(current_node.data)
            current_node = current_node.next

class DoubleEndedQueue(LinkedList):
    tail : Node

    def __init__(self, head=None):
        super().__init__(head)
        self.head = head
        self.tail = None

    def push_left(self, node):
        current_node = self.head
        if self.tail == None:
            self.tail = self.head
            self.tail.previous = node
            self.head = node
            self.head.next = self.tail
        else:
            self.head = node
            current_node.previous = node
            self.head.next = current_node

    def push_right(self, node):
        if self.tail == None:
            self.tail = node

            if self.head == None:
                self.head = node
        else:
            node.previous = self.tail
            self.tail.next = node
            self.tail = node

    def pop_left(self):
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return
        
        self.head = self.head.next
        self.head.previous = None

    def pop_right(self):
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return
        
        new_tail = self.tail.previous
        new_tail.next = None
        self.tail = new_tail
    
    def is_empty(self):
        return self.head == None and self.tail == None

def main():
    double_ended_queue = DoubleEndedQueue()

    while True:
        opt = input("Ingrese la opcion: I-Insertar Nodo E-Eliminar Nodo: ").lower()
        side = input("Ingrese el lado: I-Izquierdo D-Derecho: ").lower()
        if opt == "i":
            str = input("Ingrese el nombre del Nodo: ")
            node = Node(str)
            if side == "i":
                double_ended_queue.push_left(node)
            else:
                double_ended_queue.push_right(node)
        elif opt == "e":
            if double_ended_queue.is_empty():
                print("La cola esta vacia, no se puede eliminar nodos.")
                continue
            if side == "i":
                double_ended_queue.pop_left()
            else:
                double_ended_queue.pop_right()
        else:
            print("Opcion inválida.")
            continue

        double_ended_queue.print_structure()
        print("")

        flow_control = input("Desea continuar? S=SI  N=NO: ").lower()
        if flow_control == "n":
            break

if __name__ == "__main__":
    main()

#node1 = Node("Nodo1")
#double_ended_queue = DoubleEndedQueue(node1)
#double_ended_queue.print_structure()
#print("")
#
#node2 = Node("Node2")
#double_ended_queue.push_left(node2)
#double_ended_queue.print_structure()
#print("")
#
#node3 = Node("Node3")
#double_ended_queue.push_left(node3)
#double_ended_queue.print_structure()
#print("")
#
#node4 = Node("Node4")
#double_ended_queue.push_right(node4)
#double_ended_queue.print_structure()
#print("")
#
#node5 = Node("Node5")
#double_ended_queue.push_right(node5)
#double_ended_queue.print_structure()
#print("")
#
#node6 = Node("Node6")
#double_ended_queue.push_right(node6)
#double_ended_queue.print_structure()
#print("")
#
#node7 = Node("Node7")
#double_ended_queue.push_right(node7)
#double_ended_queue.print_structure()
#print("")
#
#node8 = Node("Node8")
#double_ended_queue.push_left(node8)
#double_ended_queue.print_structure()
#print("")
#
#node9 = Node("Node9")
#double_ended_queue.push_right(node9)
#double_ended_queue.print_structure()
#print("")
#
#
#node10 = Node("Node10")
#double_ended_queue.push_left(node10)
#double_ended_queue.print_structure()
#print("")
#
#double_ended_queue.pop_left()
#double_ended_queue.print_structure()
#print("")
#
#double_ended_queue.pop_right()
#double_ended_queue.print_structure()
#print("")
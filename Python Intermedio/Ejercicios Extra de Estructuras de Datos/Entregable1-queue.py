class Node:
    data : str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Queue:
    head : Node

    def __init__(self, head):
        self.head = head
    
    def enqueue(self, data):
        current_node = self.head

        while current_node.next != None:
            current_node = current_node.next

        current_node.next = Node(data)

    def dequeue(self):
        self.head = self.head.next
        return self.head

    def print_all(self):
        current_node = self.head

        while current_node != None:
            print(current_node.data)
            current_node = current_node.next

def main():
    node1 = Node("Nodo1")

    my_queue = Queue(node1)

    my_queue.enqueue("Nodo2")
    my_queue.enqueue("Nodo3")
    my_queue.enqueue("Nodo4")
    my_queue.enqueue("Nodo5")

    my_queue.print_all()
    print("Cola despues de enqueues")

    print(my_queue.dequeue().data)
    print(my_queue.dequeue().data)
    print(my_queue.dequeue().data)

    print("Cola despues de dequeues")
    my_queue.print_all()

if __name__ == "__main__":
    main()


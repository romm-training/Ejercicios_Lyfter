import subprocess

def clear_screen():
    subprocess.run("cls",shell=True)

class Node:
    data : str

    def __init__(self, data, previous=None, next=None):
        self.data = data
        self.previous = previous
        self.next = next

class Doubly_Linked_List:
    head : Node
    tail : Node

    def __init__(self):
        self.head = None
        self.tail = None

    def _add_first_node(self,data):
        new_node = Node(data)
        self.head = new_node
        self.tail = new_node
    
    def append(self, data):
        if self.is_empty_list():
            self._add_first_node(data)
            return
        current_node = self.tail
        self.tail = Node(data)
        current_node.next = self.tail
        self.tail.previous = current_node


    def prepend(self,data):
        if self.is_empty_list():
            self._add_first_node(data)
            return
        
        current_node = self.head
        self.head = Node(data)
        current_node.previous = self.head
        self.head.next = current_node

    def are_head_and_tail_equal(self):
        return self.head == self.tail
    
    def is_empty_list(self):
        return self.head == None and self.tail == None

    def print_forward(self):
        if self.is_empty_list():
            print("La lista esta vacia. No se puede imprimir.")
            return
        
        if self.are_head_and_tail_equal():
            print(self.head.data)
            return

        current_node = self.head

        result = ""

        while True:
            result += current_node.data
            current_node = current_node.next
            if current_node == None:
                break
            result += " -> "

        print(result)


    def print_backward(self):
        if self.is_empty_list():
            print("La lista esta vacia. No se puede imprimir.")
            return

        if self.are_head_and_tail_equal():
            print(self.head.data)
            return
        
        current_node = self.tail

        result = ""

        while True:
            result += current_node.data
            current_node = current_node.previous
            if current_node == None:
                break
            result += " >- "

        print(result)

    def delete(self,data):
        if self.is_empty_list():
            print("La lista esta vacia. No se puede eliminar.")
            return
        
        if self.are_head_and_tail_equal():
            self.head = None
            self.tail = None
            return
        
        #Si el head es igual que data, debe eliminarse, por lo que el nuevo head es el head.next y head.next.previous es None
        if self.head.data == data:
            current_node = self.head.next
            self.head == current_node
            self.head.previous = None
            return
        
        if self.tail.data == data:
            current_node = self.tail.previous
            current_node.next = None
            self.tail = current_node
            return
        
        #Si el head es diferente que data, se asigna el next a current_node para continuar buscando
        current_node = self.head.next

        #Si el current_node es el tail, quiere decir que la lista solo tiene dos nodos, por lo que se hace un manejo especial
        #Si tail es igual que data, se debe eliminar el tail, por lo que el nuevo tail es el head
        #if current_node == self.tail:
        #    if self.tail.data == data:
        #        self.tail = self.head
        #        self.tail.previous = self.head
        #        self.head.next = self.tail
        #        self.head.previous = None
        #        return

        while True:
            if current_node.data == data:
                current_node.previous.next = current_node.next
                current_node.next.previous = current_node.previous
                return
            
            if current_node.next == None:
                break
            
            current_node = current_node.next

def input_value():
    return input("Ingrese el dato del nodo: ")

def main():

    doubly_linked_list = Doubly_Linked_List()

    while True:
        clear_screen()
        opt = input(
"""
----- Menú de Opciones -----
----------------------------
F=Agregar al final
I=Agregar al inicio
D=Imprimir de izquierda a derecha
Z=Imprimir derecha a izquierda
X=Eliminar
S=Salir
----------------------------
Ingrese la opcion: """).upper()

        match opt:
            case "F":
                doubly_linked_list.append(input_value())
            case "I":
                doubly_linked_list.prepend(input_value())
            case "D":
                doubly_linked_list.print_forward()
            case "Z":
                doubly_linked_list.print_backward()
            case "X":
                if doubly_linked_list.is_empty_list():
                    print("La lista esta vacia. No se puede eliminar.")
                    continue
                doubly_linked_list.delete(input_value())
            case "S":
                print("Saliendo del sistema")
                break
            case _:
                print("Opcion invalida. Intente de nuevo.")
                continue
        
        doubly_linked_list.print_forward()
        input("Presione Enter para continuar.")

if __name__ == "__main__":
    main()

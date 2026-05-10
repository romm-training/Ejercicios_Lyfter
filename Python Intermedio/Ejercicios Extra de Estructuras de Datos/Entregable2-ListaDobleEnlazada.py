import subprocess

def clear_screen():
    subprocess.run("cls",shell=True)

class Node:
    data : str

    def __init__(self, data, previous=None, next=None):
        self.data = data
        self.previous = previous
        self.next = next

class Linked_List:
    head : Node

    def __init__(self, head=None):
        self.head = head

    def print_forward(self):
        if self.head == None:
            print("La lista esta vacia. No se puede imprimir.")
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

class Doubly_Linked_List(Linked_List):
    tail : Node

    def __init__(self, head=None, tail=None):
        super().__init__(head)
        self.tail = tail

    def _add_first_node(self,data):
        self.head = Node(data)
    
    def append(self, data):
        if self.is_empty_list():
            self._add_first_node(data)
            return
        
        new_node = Node(data)

        if self.tail == None:
            self.tail = new_node
            self.head.next = new_node
            self.tail.previous = self.head
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self,data):
        if self.is_empty_list():
            self._add_first_node(data)
            return
        
        new_node = Node(data)
        current_node = self.head

        if self.tail == None:
            self.tail = self.head
            self.tail.previous = new_node
            self.head = new_node
            self.head.next = self.tail
        else:
            self.head = new_node
            current_node.previous = new_node
            self.head.next = current_node

    def head_exists_only(self):
        return self.head != None and self.tail == None
    
    def tail_exists_only(self):
        return self.head == None and self.tail != None
    
    def is_empty_list(self):
        return self.head == None and self.tail == None

    def print_backward(self):
        if self.is_empty_list():
            print("La lista esta vacia. No se puede imprimir.")
            return

        if self.are_head_exists_only():
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
        
        if self.head_exists_only():
            self.head = None
            return
        
        if self.tail_exists_only():
            self.tail = None
            return
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return
        
        #Si el head es igual que data, debe eliminarse, por lo que el nuevo head es el head.next y head.next.previous es None
        if self.head.data == data:
            self.head = self.head.next
            self.head.previous = None
            return
        
        if self.tail.data == data:
            current_node = self.tail.previous
            current_node.next = None
            self.tail = current_node
            return
        
        current_node = self.head

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

def enter_to_continue():
    input("Presione Enter para continuar.")

def main():

    doubly_linked_list = Doubly_Linked_List()
    print_control_list = True

    while True:
        clear_screen()
        opt = input(
"""
----------------------------
----- Menú de Opciones -----
----------------------------
D=Agregar al inicio
F=Agregar al final
E=Imprimir de izquierda a derecha
R=Imprimir derecha a izquierda
X=Eliminar
Q=Salir
----------------------------
Ingrese la opcion: """).upper()

        match opt:
            case "D":
                doubly_linked_list.prepend(input_value())
            case "F":
                doubly_linked_list.append(input_value())
            case "E":
                doubly_linked_list.print_forward()
                print_control_list = False
            case "R":
                doubly_linked_list.print_backward()
                print_control_list = False
            case "X":
                if doubly_linked_list.is_empty_list():
                    print("La lista esta vacia. No se puede eliminar.")
                    enter_to_continue()
                    continue
                doubly_linked_list.delete(input_value())
                print_control_list = True
            case "Q":
                print("Saliendo del sistema")
                break
            case _:
                print("Opcion invalida. Intente de nuevo.")
                continue
        
        if print_control_list:
            doubly_linked_list.print_forward()
        enter_to_continue()

if __name__ == "__main__":
    main()

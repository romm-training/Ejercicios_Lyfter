def order_array(parray):
    for i in range(0, len(parray)-1): #O(N) Porque depende del tamano de la lista.
        smaller = i #O(1)
        for j in range(i+1, len(parray)): #O(N^2) Porque es un ciclo anidado que depende del tamano de la lista.
            if parray[j] < parray[smaller]: #O(1)
                smaller = j #O(1)
        temp = parray[i] #O(1)
        parray[i] = parray[smaller] #O(1)
        parray[smaller] = temp #O(1)
    return parray #O(1)

def print_array(array_to_print):
    print("-".join(str(n) for n in array_to_print)) #O(N) porque depende del tamano de la lista.

def main():
    my_array = [3,5,10,6,1,4,12,2,8,9,11,7] #O(1)
    print_array(my_array) #O(1)
    print_array(order_array(my_array)) #O(1)
    print("") #O(1)

    my_array1 = [12,5,10,6,7,4,3,2,8,9,11,1] #O(1)
    print_array(my_array1) #O(1)
    print_array(order_array(my_array1)) #O(1)
    print("") #O(1)
    
    my_array2 = [7,5,10,6,1,4,12,2,8,9,11,3] #O(1)
    print_array(my_array2) #O(1)
    print_array(order_array(my_array2)) #O(1)
    print("") #O(1)

    my_array3 = [7,5,1,6,1,4,7,2,8,9,3,0] #O(1)
    print_array(my_array3) #O(1)
    print_array(order_array(my_array3)) #O(1)
    print("") #O(1)
    
if __name__ == "__main__":
    main()  #O(N^2) porque es la notacion dominante dentro del main.
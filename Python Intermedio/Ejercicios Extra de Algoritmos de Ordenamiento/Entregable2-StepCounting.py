def order_array(parray):
    iterations = 0
    changes = 0
    for i in range(0, len(parray)-1):
        smaller = i
        iterations += 1
        for j in range(i+1, len(parray)):
            iterations += 1
            if parray[j] < parray[smaller]:
                smaller = j
        if smaller == i:
            continue
        temp = parray[i]
        parray[i] = parray[smaller]
        parray[smaller] = temp
        changes += 1
        #print(f"i={i} j={j} -> {parray}")
    return parray, iterations, changes

def print_array(array_to_print):
    print("-".join(str(n) for n in array_to_print))

def main():
    my_array = [3,5,10,6,1,4,12,2,8,9,11,7]
    print_array(my_array)
    ordered_array, interations, changes = order_array(my_array)
    print_array(ordered_array)
    print(f"Iteraciones={interations}, Intercambios={changes}")
    print("")

    my_array1 = [5,2,7,4,3,6,8,9,10,1]
    print_array(my_array1)
    ordered_array1, interations, changes = order_array(my_array1)
    print_array(ordered_array1)
    print(f"Iteraciones={interations}, Intercambios={changes}")
    print("")
    
    my_array2 = [7,5,6,1,4,2,8,3]
    print_array(my_array2)
    ordered_array2, interations, changes = order_array(my_array2)
    print_array(ordered_array2)
    print(f"Iteraciones={interations}, Intercambios={changes}")
    print("")

    my_array3 = [7,5,6,1,4,2,8,9,3,0]
    print_array(my_array3)
    ordered_array3, interations, changes = order_array(my_array3)
    print_array(ordered_array3)
    print(f"Iteraciones={interations}, Intercambios={changes}")
    print("")

    my_array4 = [1,2,3,4,5,6,7,8,9,10]
    print_array(my_array4)
    ordered_array4, interations, changes = order_array(my_array4)
    print_array(ordered_array4)
    print(f"Iteraciones={interations}, Intercambios={changes}")
    print("")
    
if __name__ == "__main__":
    main()
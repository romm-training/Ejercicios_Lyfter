def is_empty_list(parray):
    try:
        if len(parray) == 0:
            raise ValueError("Atención, la lista está vacía.")
    except ValueError as e:
        print(f"{e}")
        return True
    return False

def validate_no_numeric_elemets(parray):
    try:
        if any(not isinstance(n, (int, float)) for n in parray):
            raise ValueError("Atención, la lista contiene elementos no numéricos.")
    except ValueError as e:
        print(f"{e}")
        return True
    return False

def order_array(parray):
    if validate_no_numeric_elemets(parray):
        return []
    
    if is_empty_list(parray):
        return []

    for i in range(0, len(parray)-1):
        smaller = i
        for j in range(i+1, len(parray)):
            if parray[j] < parray[smaller]:
                smaller = j
        if smaller == i:
            continue
        temp = parray[i]
        parray[i] = parray[smaller]
        parray[smaller] = temp
        #print(f"i={i} j={j} -> {parray}")
    return parray

def print_array(array_to_print):
    print("-".join(str(n) for n in array_to_print))

def main():
    my_array = [3,5,10,"A",1,4,12,2,8,9,11,7]
    print_array(my_array)
    ordered_array = order_array(my_array)
    print_array(ordered_array)
    print("")

    my_array1 = [5,2,7,4,".",6,8,9,10,1]
    print_array(my_array1)
    ordered_array1 = order_array(my_array1)
    print_array(ordered_array1)
    print("")
    
    my_array2 = [7,5,6,1,"****",2,8,3]
    print_array(my_array2)
    ordered_array2 = order_array(my_array2)
    print_array(ordered_array2)
    print("")

    my_array3 = []
    print_array(my_array3)
    ordered_array3 = order_array(my_array3)
    print_array(ordered_array3)
    print("")

    my_array4 = [1,2,3,4,5,6,7,8,9,10]
    print_array(my_array4)
    ordered_array4 = order_array(my_array4)
    print_array(ordered_array4)
    print("")
    
if __name__ == "__main__":
    main()
def order_array(parray):
    for i in range(0, len(parray)-1):
        for j in range(i+1, len(parray)):
            if parray[i] > parray[j]:
                temp = parray[i]
                parray[i] = parray[j]
                parray[j] = temp
    return parray

def print_array(array_to_print):
    print("-".join(str(n) for n in array_to_print))

def main():
    my_array = [3,5,10,6,1,4,12,2,8,9,11,7]
    print_array(my_array)
    print_array(order_array(my_array))
    print("")

    my_array1 = [12,5,10,6,7,4,3,2,8,9,11,1]
    print_array(my_array1)
    print_array(order_array(my_array1))
    print("")
    
    my_array2 = [7,5,10,6,1,4,12,2,8,9,11,3]
    print_array(my_array2)
    print_array(order_array(my_array2))
    print("")

    my_array3 = [7,5,1,6,1,4,7,2,8,9,3,0]
    print_array(my_array3)
    print_array(order_array(my_array3))
    print("")
    
if __name__ == "__main__":
    main()
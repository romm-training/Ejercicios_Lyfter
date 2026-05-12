def sort_array_backwards(parray):
    for i in range(len(parray)-1,-1,-1):
        greater = i
        for j in range(i-1, -1, -1):
            if parray[j] > parray[greater]:
                greater = j
        temp = parray[i]
        parray[i] = parray[greater]
        parray[greater] = temp
        print(f"i={i} j={j} -> {parray}")
    return parray

def print_array(parray):
    print("-".join(str(n) for n in parray))

def main():
    my_array = [3,5,10,6,1,4,12,2,8,9,11,7]
    print_array(my_array)
    print_array(sort_array_backwards(my_array))
    print("")

    my_array1 = [12,5,10,6,7,4,3,2,8,9,11,1]
    print_array(my_array1)
    print_array(sort_array_backwards(my_array1))
    print("")

    my_array2 = [7,5,10,6,1,4,12,2,8,9,11,3]
    print_array(my_array2)
    print_array(sort_array_backwards(my_array2))
    print("")

    my_array3 = [7,5,1,6,1,4,7,2,8,9,3,0]
    print_array(my_array3)
    print_array(sort_array_backwards(my_array3))
    print("")

if __name__ == "__main__":
    main()
def print_numbers_times_2(numbers_list):
	for number in numbers_list: #O(N) porque depende del tamaño de la lista
		print(number * 2) #O(1)
		
def check_if_lists_have_an_equal(list_a, list_b): 
	for element_a in list_a: #O(N) porque depende del tamaño de la lista a
		for element_b in list_b: #O(N*M) porque depende del tamaño de la lista b y esta anidada al ciclo de lista a.
			if element_a == element_b: #O(1)
				return True #O(1)
				
	return False #O(1)

def print_10_or_less_elements(list_to_print):
	list_len = len(list_to_print) #O(1)
	for index in range(min(list_len, 10)): #O(1) porque se va a ejecutar un maximo de 10 veces, sin importar el valor del minimo de la lista.
		print(list_to_print[index]) #O(1)
		
def generate_list_trios(list_a, list_b, list_c):
	result_list = [] #O(1)
	for element_a in list_a: #O(N) porque depende del tamano de la lista a
		for element_b in list_b: #O(N*M) porque depende del tamano de la listas b y esta anidada
			for element_c in list_c: #O(N*M*P) porque depende del tamano de la lista c y esta anidada en tercer nivel
				result_list.append(f'{element_a} {element_b} {element_c}') #O(1)
				
	return result_list #O(1)
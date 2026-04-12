my_list = [1, 4, 17, 6, 7, 13, 9, 11, 67]

def is_prime_number(number):
    is_prime = False
    exact_divisors_count = 0
    if number > 1:
        for divisor in range(1,number+1):
            if number % divisor == 0:
                exact_divisors_count = exact_divisors_count + 1

        if exact_divisors_count == 2:
            is_prime = True

    return is_prime

def extract_prime_numbers_list(list):
    prime_numbers = []
    for number in list:
        if is_prime_number(number):
            prime_numbers.append(number)

    return prime_numbers

print(extract_prime_numbers_list(my_list))
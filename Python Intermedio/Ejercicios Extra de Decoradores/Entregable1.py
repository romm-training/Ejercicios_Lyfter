def repeat_twice(func):
    def wrapper(name):
        func(name)
        func(name)

    return wrapper

@repeat_twice
def greeting(name):
    print(f"Hora, {name}")

def main():
    greeting("Jose")
    greeting("Maria")

if __name__ == "__main__":
    main()
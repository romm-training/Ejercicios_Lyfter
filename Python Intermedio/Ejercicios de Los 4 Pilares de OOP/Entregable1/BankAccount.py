class BankAccount:
    def __init__(self):
        self.balance = 0
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def __str__(self):
        return f"El saldo es {self.balance}."
    

class SavingsAccount(BankAccount):
    def __init__(self, min_balance):
        super().__init__()
        self.min_balance = min_balance

    def withdraw(self, amount):
        try:
            if (self.balance - amount) < self.min_balance:
                raise ValueError(f"No se puede retirar porque quedaría un saldo inferior al mínimo de {self.min_balance}")

            super().withdraw(amount)
        except ValueError as e:
            print(e)

class main():
    savings_account = SavingsAccount(100)
    savings_account.deposit(100)
    print(str(savings_account))
    savings_account.deposit(100)
    print(str(savings_account))
    savings_account.withdraw(150)
    print(str(savings_account))

if __name__ == "__main__":
    main()

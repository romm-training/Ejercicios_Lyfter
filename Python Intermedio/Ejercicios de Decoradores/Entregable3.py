from datetime import date

class User:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth
    
    @property
    def age(self):
        return date.today().year - self.date_of_birth.year
        

def validate_user_over_18(func):
    def wrapper(user):
        if user.age < 18:
            raise ValueError("Atencion, el usuario es menor de edad.")
        
        return func(user)
    
    return wrapper

@validate_user_over_18
def enroll_user(user):
    print("The user has been enrolled")

def activate_user(user):
    print("The user has been activated")

def main():
    user1 = User(date(2000,1,1))
    enroll_user(user1)
    activate_user(user1)

    user2 = User(date(2020,1,1))
    enroll_user(user2)
    activate_user(user2)

if __name__ == "__main__":
    main()
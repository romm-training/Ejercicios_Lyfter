from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def has_permission(self, permission):
        pass

class AdminUser(User):
    def __init__(self, name):
        self.name = name
        self.role = "Administrador"

    def get_role(self):
        return self.role
    
    def has_permission(self, permission):
        return True
    
    def __str__(self):
        return f"El usuario {self.name} tiene el rol de {self.role}."
    
class RegularUser(User):
    def __init__(self, name):
        self.name = name
        self.role = "Solo Lectura"

    def get_role(self):
        return self.role
    
    def has_permission(self, permission):
        if permission == "read":
            return True
        
        return False
    
    def __str__(self):
        return f"El usuario {self.name} tiene el rol de {self.role}."

def main():
    user1 = AdminUser("Carlos")
    user2 = RegularUser("Andrea")

    print(f"{user1.name} tiene permiso para eliminar? = {user1.has_permission("delete")}")
    print(f"{user2.name} tiene permiso para eliminar? = {user2.has_permission("delete")}")

    print(str(user1))
    print(str(user2))

if __name__ == "__main__":
    main()
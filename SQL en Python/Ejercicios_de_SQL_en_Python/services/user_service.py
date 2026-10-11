class UserService():
    def __init__(self, user_repository, state_machine):
        self.user_repository = user_repository
        self.state_machine = state_machine

    def get_all_users(self):
        try:
            return self.user_repository.get_all()
        except Exception as e:
            print("Error al obtener todos los usuarios: ", e)
            raise

    def get_user_by_id(self, user_id):
        try:
            return self.user_repository.get_by_id(user_id)
        except Exception as e:
            print("Error al obtener usuario por Id: ", e)
            raise

    def create_user(self, user_data):
        try:
            #self.user_repository.create(user_data)
            return self.state_machine.create("user", user_data)
        except Exception as e:
            print("Error al crear usuario: ", e)
            raise

    def update_user(self, user_id, user_data):
        try:
            return self.state_machine.update(user_id, user_data)
        except Exception as e:
            print("Error al actualizar usuario: ", e)
            raise

    def delete_user(self, user_id):
        try:
            self.user_repository.delete(user_id)
            return True
        except Exception as e:
            print("Error al eliminar usuario: ", e)
            raise
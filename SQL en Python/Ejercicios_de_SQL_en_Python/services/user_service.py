class UserService():
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_all_users(self):
        try:
            return self.user_repository.get_all()
        except Exception as e:
            print("Error in UserService.get_all_users: ", e)
            raise

    def get_user_by_id(self, user_id):
        try:
            return self.user_repository.get_by_id(user_id)
        except Exception as e:
            print("Error in UserService.get_user_by_id: ", e)
            raise

    def create_user(self, user_data):
        try:
            self.user_repository.create(user_data)
        except Exception as e:
            print("Error in UserService.create_user: ", e)
            raise

    def update_user(self, user_id, user_data):
        try:
            self.user_repository.update(user_id, user_data)
        except Exception as e:
            print("Error in UserService.update_user: ", e)
            raise

    def delete_user(self, user_id):
        try:
            self.user_repository.delete(user_id)
            return True
        except Exception as e:
            print("Error in UserService.delete_user: ", e)
            raise
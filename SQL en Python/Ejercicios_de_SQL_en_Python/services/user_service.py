class UserService():
    def __init__(self, user_repository, state_machine, db_manager):
        self.user_repository = user_repository
        self.state_machine = state_machine
        self.db_manager = db_manager

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, user_data):
        return self.state_machine.create("user", user_data)

    def update_user(self, user_id, user_data):
        new_status = user_data.pop("account_status", None)
        with self.db_manager.transaction():
            car = self.user_repository.get_by_id_for_update(user_id)
            if new_status and new_status != car["account_status"]:
                self.state_machine.change_status("user", user_id, new_status)
            return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id):
        self.user_repository.delete(user_id)
        return True

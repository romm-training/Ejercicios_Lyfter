class UserService():
    def __init__(self, user_repository, state_machine, db_manager):
        self.user_repository = user_repository
        self.state_machine = state_machine
        self.db_manager = db_manager

    def get_all_users(self, filters):
        return self.user_repository.get_all(filters)

    def get_user_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, user_data):
        return self.state_machine.create("user", user_data)

    def update_user(self, user_id, user_data):
        new_status = user_data.pop("account_status", None)
        with self.db_manager.transaction():
            user = self.user_repository.get_by_id_for_update(user_id)
            if new_status and new_status != user["account_status"]:
                self.state_machine.change_status("user", user_id, new_status)

            name_field = "name"
            if name_field not in user_data:
                user_data[name_field] = user[name_field]

            email_field = "email"
            if email_field not in user_data:
                user_data[email_field] = user[email_field]

            username_field = "username"
            if username_field not in user_data:
                user_data[username_field] = user[username_field]

            password_field = "password"
            if password_field not in user_data:
                user_data[password_field] = user[password_field]

            birthdate_at_field = "birthdate_at"
            if birthdate_at_field not in user_data:
                user_data[birthdate_at_field] = user[birthdate_at_field]

            return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id):
        self.user_repository.delete(user_id)
        return True

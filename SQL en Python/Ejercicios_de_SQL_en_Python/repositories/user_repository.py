class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, user_record):
        return {
            "id": user_record[0],
            "name": user_record[1],
            "email": user_record[2],
            "username": user_record[3],
            "password": user_record[4],
            "birthdate_at": user_record[5],
            "account_status": user_record[6]
        }

    def get_all(self):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, name, email, username, password, birthdate_at, account_status " \
                "FROM lyfter_car_rental.user;"
            )
            formatted_results = [self._format_record(result) for result in results]
            print("Retrieved all users from database.")
            return formatted_results
        except Exception as e:
            print("Error getting all users from database: ", e)
            raise

    def get_by_id(self, user_id):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, name, email, username, password, birthdate_at, account_status " \
                "FROM lyfter_car_rental.user " \
                "WHERE id = %s;",
                (user_id,)
            )
            formatted_results = self._format_record(results[0])
            print("Retrieved user by ID from database.")
            return formatted_results
        except Exception as e:
            print("Error getting user by ID from database: ", e)
            raise

    def create(self, user_data):
        try:
            self.db_manager.execute_query(
                "INSERT INTO lyfter_car_rental.user (name, email, username, password, birthdate_at, account_status) " \
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (
                    user_data["name"],
                    user_data["email"],
                    user_data["username"],
                    user_data["password"],
                    user_data["birthdate_at"],
                    user_data["account_status"]
                )
            )
            print("User created in database.")
        except Exception as e:
            print("Error creating user in database: ", e)
            raise

    def update(self, user_id, user_data):
        try:
            self.db_manager.execute_query(
                "UPDATE lyfter_car_rental.user " \
                "SET name = %s, email = %s, username = %s, password = %s, birthdate_at = %s, account_status = %s " \
                "WHERE id = %s;",
                (
                    user_data["name"],
                    user_data["email"],
                    user_data["username"],
                    user_data["password"],
                    user_data["birthdate_at"],
                    user_data["account_status"],
                    user_id
                )
            )
            print("User updated in database.")
        except Exception as e:
            print("Error updating user in database: ", e)
            raise

    def delete(self, user_id):
        try:
            self.db_manager.execute_query(
                "DELETE FROM lyfter_car_rental.user " \
                "WHERE id = %s;",
                (user_id,)
            )
            print("User deleted from database.")
        except Exception as e:
            print("Error deleting user from database: ", e)
            raise

    
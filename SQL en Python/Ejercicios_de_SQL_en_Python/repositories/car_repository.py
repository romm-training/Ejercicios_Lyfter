class CarRepository():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, car_record):
        return {
            "id": car_record[0],
            "make": car_record[1],
            "model": car_record[2],
            "year": car_record[3],
            "status": car_record[4]
        }

    def get_all(self):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, make, model, year, status " \
                "FROM lyfter_car_rental.car;"
            )
            formatted_results = [self._format_record(result) for result in results]
            print("Consulta exitosa.")
            return formatted_results
        except Exception as e:
            print("Error al obtener registros de la base de datos: ", e)
            raise

    def get_by_id(self, car_id):
        try:
            results = self.db_manager.execute_query(
                "SELECT id, make, model, year, status " \
                "FROM lyfter_car_rental.car " \
                "WHERE id = %s;",
                (car_id,)
            )
            formatted_results = self._format_record(results[0])
            print("Consulta exitosa.")
            return formatted_results
        except Exception as e:
            print("Error al obtener registro por ID de la base de datos: ", e)
            raise

    def create(self, car_data):
        try:
            self.db_manager.execute_query(
                "INSERT INTO lyfter_car_rental.car (make, model, year, status) " \
                "VALUES (%s, %s, %s, %s);",
                (
                    car_data["make"],
                    car_data["model"],
                    car_data["year"],
                    car_data["status"]
                )
            )
            print("Creación exitosa.")
        except Exception as e:
            print("Error al crear registro en la base de datos: ", e)
            raise

    def update(self, car_id, car_data):
        try:
            self.db_manager.execute_query(
                "UPDATE lyfter_car_rental.car " \
                "SET make = %s, model = %s, year = %s, status = %s WHERE id = %s;",
                (
                    car_data["make"],
                    car_data["model"],
                    car_data["year"],
                    car_data["status"],
                    car_id
                )
            )
            print("Actualización exitosa.")
        except Exception as e:
            print("Error al actualizar registro en la base de datos: ", e)
            raise

    def delete(self, car_id):
        try:
            self.db_manager.execute_query(
                "DELETE FROM lyfter_car_rental.car " \
                "WHERE id = %s;",
                (car_id,)
            )
            print("Eliminación exitosa.")
        except Exception as e:
            print("Error al eliminar registro de la base de datos: ", e)
            raise
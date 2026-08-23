from dto import category_dto
from persistency import persistency_category

class Category_Biz():
    def append_data(category_dto):
        persistency_category.append_data(category_dto)

    def read_data() -> list:
        data = []
        try:
            data = persistency_category.read_data()
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return data
        
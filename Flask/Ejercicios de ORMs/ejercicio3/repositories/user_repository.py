from sqlalchemy.orm import selectinload, Session

from ejercicio3.repositories.base_repository import BaseRepository

from ejercicio3.models.user_model import User
from ejercicio3.repositories.car_repository import CarRepository

class UserRepository(BaseRepository[User]):
    model = User
    updatable = frozenset({"name", "full_name"})
    load_options = (selectinload(User.addresses), selectinload(User.cars))

    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self._cars = CarRepository(session)

    def associate_car(self, user_id: int, car_id: int) -> User:
        user = self.get_by_id(user_id)
        car = self._cars.get_by_id(car_id)
        if car not in user.cars:
            user.cars.append(car)
            self._session.flush()
        return user

    def disassociate_user_car(self, user_id: int, car_id: int) -> bool:
        user = self.get_by_id(user_id)
        car = self._cars.get_by_id(car_id)

        if user is None or car is None:
            return False

        if car in user.cars:
            user.cars.remove(car)
            self._session.flush()
            return True
        return False
        
from .base_domain_exception import BaseDomainException


class DishNotFoundException(BaseDomainException):
    def __init__(self, dish_id: str) -> None:
        super().__init__(
            message=f"Dish with id '{dish_id}' was not found.",
            response_code=404,
            name="dish_not_found",
        )

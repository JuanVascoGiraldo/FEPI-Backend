from typing import Optional
import functools


def from_camel_case_to_snake_case(name: str) -> str:
    if not name:
        return name
    result = []
    for char in name:
        if char.isupper():
            if result:
                result.append('_')
            result.append(char.lower())
        else:
            result.append(char)
    return ''.join(result)


class BaseDomainException(Exception):
    code = 0
    response_code = 500

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def __class_name__(cls):
        return from_camel_case_to_snake_case(cls.__name__)

    def __init__(
        self,
        message: str,
        response_code: Optional[int] = 500,
        name: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response_code = response_code
        if name is None:
            self.name = self.__class_name__
        else:
            self.name = name

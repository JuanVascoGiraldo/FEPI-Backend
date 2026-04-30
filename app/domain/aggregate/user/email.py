from pydantic import BaseModel, EmailStr, field_validator


class Email(BaseModel):
    value: EmailStr

    @field_validator("value", mode="before")
    @classmethod
    def normalize(cls, v: str) -> str:
        return v.strip().lower()

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other.lower()
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def domain(self) -> str:
        return self.value.split("@")[1]

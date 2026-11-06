from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str | None = None

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
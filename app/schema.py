import datetime, uuid
from typing import Literal
from pydantic import BaseModel
from special_types import ROLE


class IdResponse(BaseModel):
    id: int

class SuccessResponse(BaseModel):
    status: Literal["Success!"]

class AdvCreateRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str

class AdvCreateResponse(IdResponse):
    pass

class AdvUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None

class AdvUpdateResponse(SuccessResponse):
    pass

class AdvGetResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    creation_time: datetime.datetime

class AdvSearchResponse(BaseModel):
    results: list[AdvGetResponse]

class AdvDeleteResponse(SuccessResponse):
    pass

class BaseUserRequest(BaseModel):
    name: str
    password: str

class CreateUserRequest(BaseUserRequest):
    pass


class CreateUserResponse(IdResponse):
    pass


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID

class UserGetResponse(BaseModel):
    id: int
    name: str

class UserUpdateResponse(SuccessResponse):
    pass

class UserUpdateRequest(BaseModel):
    name: str | None = None
    password: str | None = None
    role: ROLE | None = None

class UserDeleteResponse(SuccessResponse):
    pass

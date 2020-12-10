from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserInfoBase):
    fullname: str
    password: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class BlogBase(BaseModel):
    title: str
    content: str


class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True

class Dog(BaseModel):
    id:str
    name:str
    picture:str
    create_date:str
    is_adopted:bool






# from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    disabled: Optional[bool] = False
    first_name: str
    last_name: str
    description: Optional[str]
    todos: Optional[list]
    categories: Optional[list]
    photo_id: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Bladeburner01",
                "email": "Bladeburner01@gmail.com",
                "disabled": "false",
                "first_name": "Lee",
                "last_name": "Pham",
                "description": "hello world, i like to code, i like to consider that im a real software engineer but im just actually having fun!",
                "todos": [
                    "647c33b7257a0b5aa8bf7a3f",
                    "647c61bff3250a39f366376d",
                    "647c66cbf3250a39f366376e",
                ],
                "categories": ["647c619df3250a39f366376b", "647c61a7f3250a39f366376c"],
                "photo_id": "64a388ecb30cf54357043921",
            }
        }


class UserInDb(User):
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Bladeburner01",
                "email": "Bladeburner01@gmail.com",
                "disabled": "false",
                "first_name": "Lee",
                "last_name": "Pham",
                "description": "hello world, i like to code, i like to consider that im a real software engineer but im just actually having fun!",
                "todos": [
                    "647c33b7257a0b5aa8bf7a3f",
                    "647c61bff3250a39f366376d",
                    "647c66cbf3250a39f366376e",
                ],
                "categories": ["647c619df3250a39f366376b", "647c61a7f3250a39f366376c"],
                "photo_id": "64a388ecb30cf54357043921",
                "hashed_password": "Password123!",
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[str]
    disabled: Optional[bool] = False
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]
    todos: Optional[list]
    categories: Optional[list]
    photo_id: Optional[str]
    hashed_password: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Bladeburner01",
                "email": "Bladeburner01@gmail.com",
                "disabled": "false",
                "first_name": "Lee",
                "last_name": "Pham",
                "description": "hello world, i like to code, i like to consider that im a real software engineer but im just actually having fun!",
                "todos": [
                    "647c33b7257a0b5aa8bf7a3f",
                    "647c61bff3250a39f366376d",
                    "647c66cbf3250a39f366376e",
                ],
                "categories": ["647c619df3250a39f366376b", "647c61a7f3250a39f366376c"],
                "photo_id": "64a388ecb30cf54357043921",
                "hashed_password": "Password123!",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

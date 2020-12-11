from bson import ObjectId
from pydantic import BaseModel, BaseConfig


class PyObjectId(ObjectId):
    """
    开启orm模式非常方便，但是无法正确显示object_id
    原因是pydantic无法直接转换mongo object
    我们新建一个类型用于通过检测和转换
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class MongoModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

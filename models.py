from bson import ObjectId
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema
from typing import Any
from typing import Annotated, Union

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

class GameModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ExperienceModel(BaseModel):
    id: int = Field(alias="_id")
    level: str
    color: str
    label: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TipModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    game_id: PyObjectId
    experience_id: int = Field(ge=1, lt=4)
    spoiler_free: bool
    title: str
    description: str
    likes: int = Field(ge=0)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ReportModel(BaseModel):
    class Reason(Enum):
        INCORRECT = "Incorrect Information"
        OUTDATED = "Outdated"
        TYPO = "Typo"

    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    tip_id: PyObjectId
    reason: Reason
    description: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

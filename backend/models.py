from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# Utility to handle MongoDB ObjectId in Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Models
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

# Farm Models
class FarmBase(BaseModel):
    name: str
    location: str

class FarmCreate(FarmBase):
    pass

class FarmInDB(FarmBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class FarmResponse(FarmBase):
    id: str
    owner: str
    createdAt: str

# Livestock Models
class LivestockBase(BaseModel):
    type: str
    animalId: str
    age: float
    weight: float

class LivestockCreate(LivestockBase):
    farmId: str

class LivestockInDB(LivestockBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    farm: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class LivestockResponse(LivestockBase):
    id: str
    farm: FarmResponse
    createdAt: str

# Feed Plan Models
class FeedPlanBase(BaseModel):
    feedType: str
    quantity: float
    date: str
    notes: Optional[str] = None

class FeedPlanCreate(FeedPlanBase):
    livestockId: str

class FeedPlanInDB(FeedPlanBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    livestock: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class FeedPlanResponse(FeedPlanBase):
    id: str
    livestock: LivestockResponse
    createdAt: str

# Health Record Models
class HealthRecordBase(BaseModel):
    condition: str
    date: str
    notes: Optional[str] = None

class HealthRecordCreate(HealthRecordBase):
    livestockId: str

class HealthRecordInDB(HealthRecordBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    livestock: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class HealthRecordResponse(HealthRecordBase):
    id: str
    livestock: LivestockResponse
    createdAt: str

# Recommendation Models
class RecommendationBase(BaseModel):
    type: str
    recommendation: str
    confidence: float

class RecommendationCreate(RecommendationBase):
    livestockId: str

class RecommendationInDB(RecommendationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    livestock: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RecommendationResponse(RecommendationBase):
    id: str
    livestock: LivestockResponse
    createdAt: str
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from models import (
    FarmCreate, FarmInDB, FarmResponse,
    LivestockCreate, LivestockInDB, LivestockResponse,
    FeedPlanCreate, FeedPlanInDB, FeedPlanResponse,
    HealthRecordCreate, HealthRecordInDB, HealthRecordResponse,
    RecommendationCreate, RecommendationInDB, RecommendationResponse,
    UserInDB,
)
from datetime import datetime

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")
db = client["cattlefeedai"]
farms_collection = db["farms"]
livestock_collection = db["livestock"]
feed_plans_collection = db["feedplans"]
health_records_collection = db["healthrecords"]
recommendations_collection = db["recommendations"]

# Farm CRUD
def create_farm(farm: FarmCreate, owner_id: str) -> FarmInDB:
    farm_dict = farm.dict()
    farm_dict["owner"] = ObjectId(owner_id)
    farm_dict["createdAt"] = datetime.utcnow()
    result = farms_collection.insert_one(farm_dict)
    farm_dict["_id"] = result.inserted_id
    return FarmInDB(**farm_dict)

def get_farms_by_owner(owner_id: str) -> List[FarmResponse]:
    farms = farms_collection.find({"owner": ObjectId(owner_id)}).sort("createdAt", -1)
    return [FarmResponse(**farm) for farm in farms]

def get_farm_by_id(farm_id: str, owner_id: str) -> Optional[FarmResponse]:
    farm = farms_collection.find_one({"_id": ObjectId(farm_id), "owner": ObjectId(owner_id)})
    return FarmResponse(**farm) if farm else None

def update_farm(farm_id: str, owner_id: str, farm_update: FarmCreate) -> Optional[FarmResponse]:
    farm = farms_collection.find_one_and_update(
        {"_id": ObjectId(farm_id), "owner": ObjectId(owner_id)},
        {"$set": farm_update.dict()},
        return_document=True
    )
    return FarmResponse(**farm) if farm else None

def delete_farm(farm_id: str, owner_id: str) -> bool:
    result = farms_collection.delete_one({"_id": ObjectId(farm_id), "owner": ObjectId(owner_id)})
    return result.deleted_count > 0

# Livestock CRUD
def create_livestock(livestock: LivestockCreate, owner_id: str) -> LivestockInDB:
    farm = farms_collection.find_one({"_id": ObjectId(livestock.farmId), "owner": ObjectId(owner_id)})
    if not farm:
        raise ValueError("Farm not found or not authorized")
    
    livestock_dict = livestock.dict(exclude={"farmId"})
    livestock_dict["farm"] = ObjectId(livestock.farmId)
    livestock_dict["createdAt"] = datetime.utcnow()
    result = livestock_collection.insert_one(livestock_dict)
    livestock_dict["_id"] = result.inserted_id
    livestock_dict["farm"] = farm
    return LivestockInDB(**livestock_dict)

def get_livestock_by_owner(owner_id: str) -> List[LivestockResponse]:
    farms = farms_collection.find({"owner": ObjectId(owner_id)})
    farm_ids = [farm["_id"] for farm in farms]
    livestock = livestock_collection.find({"farm": {"$in": farm_ids}}).sort("createdAt", -1)
    livestock_list = []
    for item in livestock:
        farm = farms_collection.find_one({"_id": item["farm"]})
        item["farm"] = farm
        livestock_list.append(LivestockResponse(**item))
    return livestock_list

def get_livestock_by_id(livestock_id: str, owner_id: str) -> Optional[LivestockResponse]:
    livestock = livestock_collection.find_one({"_id": ObjectId(livestock_id)})
    if not livestock:
        return None
    farm = farms_collection.find_one({"_id": livestock["farm"], "owner": ObjectId(owner_id)})
    if not farm:
        return None
    livestock["farm"] = farm
    return LivestockResponse(**livestock)

def update_livestock(livestock_id: str, owner_id: str, livestock_update: LivestockCreate) -> Optional[LivestockResponse]:
    livestock = get_livestock_by_id(livestock_id, owner_id)
    if not livestock:
        return None
    update_data = livestock_update.dict(exclude={"farmId"})
    if livestock_update.farmId:
        farm = farms_collection.find_one({"_id": ObjectId(livestock_update.farmId), "owner": ObjectId(owner_id)})
        if not farm:
            raise ValueError("Farm not found or not authorized")
        update_data["farm"] = ObjectId(livestock_update.farmId)
    livestock = livestock_collection.find_one_and_update(
        {"_id": ObjectId(livestock_id)},
        {"$set": update_data},
        return_document=True
    )
    livestock["farm"] = farm if livestock_update.farmId else farms_collection.find_one({"_id": livestock["farm"]})
    return LivestockResponse(**livestock)

def delete_livestock(livestock_id: str, owner_id: str) -> bool:
    livestock = get_livestock_by_id(livestock_id, owner_id)
    if not livestock:
        return False
    result = livestock_collection.delete_one({"_id": ObjectId(livestock_id)})
    return result.deleted_count > 0

# Feed Plan CRUD
def create_feed_plan(feed_plan: FeedPlanCreate, owner_id: str) -> FeedPlanInDB:
    livestock = get_livestock_by_id(feed_plan.livestockId, owner_id)
    if not livestock:
        raise ValueError("Livestock not found or not authorized")
    
    feed_plan_dict = feed_plan.dict(exclude={"livestockId"})
    feed_plan_dict["livestock"] = ObjectId(feed_plan.livestockId)
    feed_plan_dict["createdAt"] = datetime.utcnow()
    result = feed_plans_collection.insert_one(feed_plan_dict)
    feed_plan_dict["_id"] = result.inserted_id
    feed_plan_dict["livestock"] = livestock.dict()
    return FeedPlanInDB(**feed_plan_dict)

def get_feed_plans_by_owner(owner_id: str) -> List[FeedPlanResponse]:
    farms = farms_collection.find({"owner": ObjectId(owner_id)})
    farm_ids = [farm["_id"] for farm in farms]
    livestock = livestock_collection.find({"farm": {"$in": farm_ids}})
    livestock_ids = [item["_id"] for item in livestock]
    feed_plans = feed_plans_collection.find({"livestock": {"$in": livestock_ids}}).sort("date", -1)
    feed_plan_list = []
    for plan in feed_plans:
        livestock_data = livestock_collection.find_one({"_id": plan["livestock"]})
        farm = farms_collection.find_one({"_id": livestock_data["farm"]})
        livestock_data["farm"] = farm
        plan["livestock"] = livestock_data
        feed_plan_list.append(FeedPlanResponse(**plan))
    return feed_plan_list

def get_feed_plan_by_id(feed_plan_id: str, owner_id: str) -> Optional[FeedPlanResponse]:
    feed_plan = feed_plans_collection.find_one({"_id": ObjectId(feed_plan_id)})
    if not feed_plan:
        return None
    livestock = get_livestock_by_id(str(feed_plan["livestock"]), owner_id)
    if not livestock:
        return None
    feed_plan["livestock"] = livestock.dict()
    return FeedPlanResponse(**feed_plan)

def update_feed_plan(feed_plan_id: str, owner_id: str, feed_plan_update: FeedPlanCreate) -> Optional[FeedPlanResponse]:
    feed_plan = get_feed_plan_by_id(feed_plan_id, owner_id)
    if not feed_plan:
        return None
    update_data = feed_plan_update.dict(exclude={"livestockId"})
    if feed_plan_update.livestockId:
        livestock = get_livestock_by_id(feed_plan_update.livestockId, owner_id)
        if not livestock:
            raise ValueError("Livestock not found or not authorized")
        update_data["livestock"] = ObjectId(feed_plan_update.livestockId)
    feed_plan = feed_plans_collection.find_one_and_update(
        {"_id": ObjectId(feed_plan_id)},
        {"$set": update_data},
        return_document=True
    )
    feed_plan["livestock"] = livestock.dict() if feed_plan_update.livestockId else feed_plans_collection.find_one({"_id": feed_plan["livestock"]})
    return FeedPlanResponse(**feed_plan)

def delete_feed_plan(feed_plan_id: str, owner_id: str) -> bool:
    feed_plan = get_feed_plan_by_id(feed_plan_id, owner_id)
    if not feed_plan:
        return False
    result = feed_plans_collection.delete_one({"_id": ObjectId(feed_plan_id)})
    return result.deleted_count > 0

# Health Record CRUD
def create_health_record(health_record: HealthRecordCreate, owner_id: str) -> HealthRecordInDB:
    livestock = get_livestock_by_id(health_record.livestockId, owner_id)
    if not livestock:
        raise ValueError("Livestock not found or not authorized")
    
    health_record_dict = health_record.dict(exclude={"livestockId"})
    health_record_dict["livestock"] = ObjectId(health_record.livestockId)
    health_record_dict["createdAt"] = datetime.utcnow()
    result = health_records_collection.insert_one(health_record_dict)
    health_record_dict["_id"] = result.inserted_id
    health_record_dict["livestock"] = livestock.dict()
    return HealthRecordInDB(**health_record_dict)

def get_health_records_by_owner(owner_id: str) -> List[HealthRecordResponse]:
    farms = farms_collection.find({"owner": ObjectId(owner_id)})
    farm_ids = [farm["_id"] for farm in farms]
    livestock = livestock_collection.find({"farm": {"$in": farm_ids}})
    livestock_ids = [item["_id"] for item in livestock]
    health_records = health_records_collection.find({"livestock": {"$in": livestock_ids}}).sort("date", -1)
    health_record_list = []
    for record in health_records:
        livestock_data = livestock_collection.find_one({"_id": record["livestock"]})
        farm = farms_collection.find_one({"_id": livestock_data["farm"]})
        livestock_data["farm"] = farm
        record["livestock"] = livestock_data
        health_record_list.append(HealthRecordResponse(**record))
    return health_record_list

def get_health_record_by_id(health_record_id: str, owner_id: str) -> Optional[HealthRecordResponse]:
    health_record = health_records_collection.find_one({"_id": ObjectId(health_record_id)})
    if not health_record:
        return None
    livestock = get_livestock_by_id(str(health_record["livestock"]), owner_id)
    if not livestock:
        return None
    health_record["livestock"] = livestock.dict()
    return HealthRecordResponse(**health_record)

def update_health_record(health_record_id: str, owner_id: str, health_record_update: HealthRecordCreate) -> Optional[HealthRecordResponse]:
    health_record = get_health_record_by_id(health_record_id, owner_id)
    if not health_record:
        return None
    update_data = health_record_update.dict(exclude={"livestockId"})
    if health_record_update.livestockId:
        livestock = get_livestock_by_id(health_record_update.livestockId, owner_id)
        if not livestock:
            raise ValueError("Livestock not found or not authorized")
        update_data["livestock"] = ObjectId(health_record_update.livestockId)
    health_record = health_records_collection.find_one_and_update(
        {"_id": ObjectId(health_record_id)},
        {"$set": update_data},
        return_document=True
    )
    health_record["livestock"] = livestock.dict() if health_record_update.livestockId else health_records_collection.find_one({"_id": health_record["livestock"]})
    return HealthRecordResponse(**health_record)

def delete_health_record(health_record_id: str, owner_id: str) -> bool:
    health_record = get_health_record_by_id(health_record_id, owner_id)
    if not health_record:
        return False
    result = health_records_collection.delete_one({"_id": ObjectId(health_record_id)})
    return result.deleted_count > 0

# Recommendation CRUD
def create_recommendation(recommendation: RecommendationCreate, owner_id: str) -> RecommendationInDB:
    livestock = get_livestock_by_id(recommendation.livestockId, owner_id)
    if not livestock:
        raise ValueError("Livestock not found or not authorized")
    
    recommendation_dict = recommendation.dict(exclude={"livestockId"})
    recommendation_dict["livestock"] = ObjectId(recommendation.livestockId)
    recommendation_dict["createdAt"] = datetime.utcnow()
    result = recommendations_collection.insert_one(recommendation_dict)
    recommendation_dict["_id"] = result.inserted_id
    recommendation_dict["livestock"] = livestock.dict()
    return RecommendationInDB(**recommendation_dict)

def get_recommendations_by_owner(owner_id: str) -> List[RecommendationResponse]:
    farms = farms_collection.find({"owner": ObjectId(owner_id)})
    farm_ids = [farm["_id"] for farm in farms]
    livestock = livestock_collection.find({"farm": {"$in": farm_ids}})
    livestock_ids = [item["_id"] for item in livestock]
    recommendations = recommendations_collection.find({"livestock": {"$in": livestock_ids}}).sort("createdAt", -1)
    recommendation_list = []
    for rec in recommendations:
        livestock_data = livestock_collection.find_one({"_id": rec["livestock"]})
        farm = farms_collection.find_one({"_id": livestock_data["farm"]})
        livestock_data["farm"] = farm
        rec["livestock"] = livestock_data
        recommendation_list.append(RecommendationResponse(**rec))
    return recommendation_list

def get_recommendations_by_livestock(livestock_id: str, owner_id: str) -> List[RecommendationResponse]:
    livestock = get_livestock_by_id(livestock_id, owner_id)
    if not livestock:
        raise ValueError("Livestock not found or not authorized")
    recommendations = recommendations_collection.find({"livestock": ObjectId(livestock_id)}).sort("createdAt", -1)
    recommendation_list = []
    for rec in recommendations:
        rec["livestock"] = livestock.dict()
        recommendation_list.append(RecommendationResponse(**rec))
    return recommendation_list
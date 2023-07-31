from bson import ObjectId
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from typing import List

from models import GameModel, ExperienceModel, TipModel, ReportModel

config = dotenv_values(".env")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.on_event("startup")
def startup_db():
    # Create a new client and connect to the server
    uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@{config['CLUSTER']}/?retryWrites=true&w=majority"
    app.mongodb_client = MongoClient(uri)
    app.db = app.mongodb_client[config["DB_NAME"]]
    
    # Send a ping to confirm a successful connection
    try:
        app.mongodb_client.admin.command("ping")
        print(f"Connected to the MongoDB database: {app.db.name}")
    except Exception as e:
        print(e)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/experience/{exp_level_id}", response_description="Get experience level details", response_model=ExperienceModel)
def get_experience_level(exp_level_id: int):
    details = app.db["experience_levels"].find_one({"_id": exp_level_id})
    return details

@app.get("/games", response_description="Get all games", response_model=List[GameModel])
def get_all_games():
    games = app.db["games"].find()
    return games

@app.get("/games/{id}", response_description="Get a game with specified id", response_model=GameModel)
def get_game(id: str):
    game = app.db["games"].find_one({"_id": ObjectId(id)})
    return game

@app.get("/tips", response_description="Get tips, optionally filtering by game, experience, and/or spoilers", response_model=List[TipModel])
def get_tips(game_id: str | None = None, experience: int | None = None, spoiler_free: bool = False):
    query_filter = {}

    if game_id:
        query_filter["game_id"] = ObjectId(game_id)

    if experience:
        query_filter["experience_id"] = experience

    if spoiler_free == True:
        query_filter["spoiler_free"] = True

    tips = app.db["tips"].find(query_filter)
    return tips

@app.get("/tips/{id}", response_description="Get a tip with specified id", response_model=TipModel)
def get_tip(id: str):
    tip = app.db["tips"].find_one({"_id": ObjectId(id)})
    return tip

@app.patch("/tips/{id}/like", response_description="Add a like to a tip", response_model=TipModel)
def add_like_to_tip(id: str):
    update_tip = app.db["tips"].update_one({"_id": ObjectId(id)}, {"$inc": {"likes": 1}})

    if update_tip.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Tip with ID {id} has not been modified")
    
    # Return updated tip if successful
    updated_tip = app.db["tips"].find_one({"_id": ObjectId(id)})
    if updated_tip:
        return updated_tip
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tip with ID {id} not found")

@app.get("/reports", response_description="Get all reports, optionally filtering for tip_id", response_model=List[ReportModel])
def get_all_reports(tip_id: str | None = None):
    # Add tip_id to filter if given as param
    query_filter = {}
    if tip_id:
        query_filter["tip_id"] = ObjectId(tip_id)
    
    reports = app.db["reports"].find(query_filter)
    return reports

@app.post("/reports", response_description="Report a tip with specified id", response_model=ReportModel)
def report_tip(report: ReportModel):
    # Verify that tip_id points to an existing tip
    found_tip = app.db["tips"].find_one({"_id": ObjectId(report.tip_id)})
    if not found_tip:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Could not find tip with ID {report.tip_id}")

    # Get data ready to send
    report_data = jsonable_encoder(report)
    new_report = app.db["reports"].insert_one(report_data)
    created_report = app.db["reports"].find_one({"_id": new_report.inserted_id})

    # Return the created report
    if created_report:
        return created_report
    
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Unable to find report with ID {new_report.inserted_id}")

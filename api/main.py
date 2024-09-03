import bson.json_util as json_util
from fastapi import FastAPI
import configparser
import motor.motor_asyncio

app = FastAPI()
config = configparser.ConfigParser()
config.read('config.ini')

client = motor.motor_asyncio.AsyncIOMotorClient(config['MongoDB']['URI'])
db = client.legos

@app.get("/")
def read_root():
    return { "status": 200}

@app.get("/sets/yearly_stats")
async def read_yearly_stats():
    sets_cursor = db.sets_stats.find({}, {"_id": 0})
    return json_util.dumps(await sets_cursor.to_list(length=100))
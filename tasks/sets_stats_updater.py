import asyncio
import configparser
import motor.motor_asyncio
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

client = motor.motor_asyncio.AsyncIOMotorClient(config['MongoDB']['URI'])
db = client.legos

async def update_sets_yearly_stats():
    for year in range(2010, datetime.now().year+1):
        parts_sum = 0
        sets_cursor = db.sets.find({"year": year})
        sets_count = await db.sets.count_documents({"year": year})
        
        async for set in sets_cursor:
            parts_sum += set['num_parts']
        
        avg_parts = parts_sum / sets_count
        await db.sets_stats.find_one_and_update(
            {
                "year": year
            },
            {
                "$set": {
                    "year": year,
                    "sets_no": sets_count,
                    "avg_parts": avg_parts
                }
            },
            upsert=True
        )

asyncio.run(update_sets_yearly_stats())

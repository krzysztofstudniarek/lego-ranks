import asyncio
import json
import configparser
from time import sleep
import urllib.request
import motor.motor_asyncio

config = configparser.ConfigParser()
config.read('config.ini')

client = motor.motor_asyncio.AsyncIOMotorClient(config['MongoDB']['URI'])
db = client.legos

async def update_sets(url):
    request = urllib.request.Request(url+'?page_size=200&min_parts=10&min_year=2010')
    request.add_header("Authorization", f"key {config['Api']['REBRICKABLE_API_KEY']}")
    response = json.load(urllib.request.urlopen(request))

    for set in response['results']:
        await db.sets.find_one_and_update(
            {
                "set_id": set['set_num']
            }
            ,{
                "$set": {
                    "set_id": set['set_num'],
                    "name": set['name'],
                    "year": set['year'],
                    "num_parts": set['num_parts'],
                }
            },
            upsert=True
        )

    document_count = await db.sets.estimated_document_count()
    print(f"Progress: {document_count/response['count']*100} %")
    sleep(10)
    if response['next'] is not None:
        await update_sets(response['next'])
    
async def sets_updater():
    await update_sets("https://rebrickable.com/api/v3/lego/sets/")

asyncio.run(sets_updater())
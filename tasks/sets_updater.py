import schedule
import time
import configparser
import urllib.request
import motor.motor_asyncio

config = configparser.ConfigParser()
config.read('config.ini')

client = motor.motor_asyncio.AsyncIOMotorClient(config['MongoDB']['URI'])
db = client.legos

def sets_updater():
    print("Updating sets")

    request = urllib.request.Request("https://rebrickable.com/api/v3/lego/sets/")
    response = request.add_header("Authorization", f"key {config['Api']['REBRICKABLE_API_KEY']}")

    print(response)

    db.sets.insert_one({
        "hello": "mongo"
    })

    print("Sets updated")

schedule.every(10).seconds.do(sets_updater)

while True:
    schedule.run_pending()
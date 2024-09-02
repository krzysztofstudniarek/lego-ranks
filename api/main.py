from fastapi import FastAPI
import configparser
import urllib.request

app = FastAPI()
config = configparser.ConfigParser()
config.read('config.ini')


@app.get("/")
def read_root():
    if 'REBRICKABLE_API_KEY' not in config['Api']:
        return { "status": -1, "message": "Rebrickable API not reachable" }

    req = urllib.request.Request("https://rebrickable.com/api/v3/lego/sets/")
    req.add_header("Authorization", f"key {config['Api']['REBRICKABLE_API_KEY']}")

    return urllib.request.urlopen(req).read()
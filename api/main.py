from fastapi import FastAPI
import configparser
import urllib.request

app = FastAPI()
config = configparser.ConfigParser()
config.read('config.ini')


@app.get("/")
def read_root():
    return { "status": 200}

@app.get("/sets/yearly_stats")
def read_yearly_stats():
    return {
        "status": 200,
        "data": [
            {"year": 2010, "sets": 100, "avg_parts": 100},
            {"year": 2011, "sets": 100, "avg_parts": 100},
            {"year": 2012, "sets": 100, "avg_parts": 100},
        ]
    }
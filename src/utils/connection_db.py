from pymongo import MongoClient
from config import user, password

url = f"mongodb+srv://{user}:{password}@bootcamp.ml0ht.mongodb.net/test"
client = MongoClient(url)
db = client.get_database("Bootcamp")
projectdb = db.mid_project

def read_database(match={}, project={"__id":0, "name":1}):
    return projectdb.find(match, project)
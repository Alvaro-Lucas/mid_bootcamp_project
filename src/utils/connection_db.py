from pymongo import MongoClient
from config import user, password

url = f"mongodb+srv://{user}:{password}@core-bdml.t6lgs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

db = client.get_database("core-bdml")
pokemondb = db.pokemon

def read_database(match={"name":"charmander"}, project={"__id":0,"name":1}):
    print(f"{match = } {project = }")
    data = list(pokemondb.find(match, project))
    return str(data)
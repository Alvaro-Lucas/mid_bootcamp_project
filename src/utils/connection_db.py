from pymongo import MongoClient
from config import user, password

url = f"mongodb+srv://{user}:{password}@bootcamp.ml0ht.mongodb.net/test"
client = MongoClient(url)

def create_data(db, collection, data):
    db = client.get_database(db)[collection]
    result = db.insert_one(data)
    return str(result.inserted_id)

def read_database(db, collection, match={}, project=None):
    print(f"{match = } {project = }")
    db = client.get_database(db)[collection]
    return list(db.find(match, project))

def update_data(db, collection, query, new_data):
    db = client.get_database(db)[collection]
    res = db.update_many(query, new_data)

    return {"Modified elements": res.modified_count}

def delete_data(db, collection, condition):
    db = client.get_database(db)[collection]
    res = db.delete_many(condition)
    return {"Deleted elements": res.deleted_count}

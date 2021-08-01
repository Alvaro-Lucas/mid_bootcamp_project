from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import *
from utils.type_casting import type_casting, str_to_dict
from flask import request
import json
from app import app

@app.route("/get")
@handle_error
#http://127.0.0.1:3500/get?name=Hello&second=World
def read_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    try:
        project = {element: 1 for element in params['project'].split(",")}
    except:
        project=None
    
    return json_response(read_database("mid_project", "covid", params, project))

#http://127.0.0.1:3500/post?name=Hola&second=Mundo
@app.route("/post")
@handle_error
def write_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    print(params)
    return json_response(create_data("mid_project", "covid", params))

@app.route("/delete")
@handle_error
def delete_db():
    condition = type_casting(**dict(request.args))
    if not condition:
        raise ValueError("There isn't any query parameters")
    print(condition)
    return json_response(delete_data("mid_project", "covid", condition))

#http://127.0.0.1:3500/update?query=name=Hola,second=Mundo&new_data=name=Hello,second=World
@app.route("/update")
@handle_error
def update_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    query = str_to_dict(params['query'])
    new_data = {"$set":str_to_dict(params['new_data'])}
    print(f"{new_data = }")
    return json_response(update_data("mid_project", "covid", query, new_data))

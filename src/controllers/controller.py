from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import *
from utils.type_casting import type_casting, str_to_dict
from flask import request
import json
from app import app

def get_project(params, db_collection):
    found = False
    try:
        project = {element: 1 for element in params['project'].split(",")}
        params.pop("project")
        for key, value in project.items():
            if key == "_id":
                found = True
        if "Total" in project:
            aux = read_database("mid_project", db_collection, {'Country/Region':'Spain'})
            project[aux[0].popitem()[0]] = 1
            project.pop("Total")
        if not found:
            project["_id"] = 0
    except Exception:
        project=None
    return project

dic_operators_to_query ={
    ">":"$gt",
    ">=":"$gte",
    "<":"$lt", 
    "<=":"$lte"
}

dic_db_collection = {
    "deaths":"deaths_covid",
    "recovered":"recovered_covid",
    "ccaa_data":"ccaa_covid_data",
    "ccaa_vac":"ccaa_covid_vac"
}

@app.route("/get/<db_collection>")
@handle_error
def read_db_collection(db_collection):
      return read_db(dic_db_collection[db_collection])


#http://127.0.0.1:3500/get?name=Hello&second=World
#name y second son columnas
@app.route("/get")
@handle_error
def read_db(db_collection = "covid"):
    params = type_casting(**dict(request.args))

    project = get_project(params, db_collection)

    if "All" in params:
        return json_response(read_database("mid_project", db_collection, project=project))
    if not params:
        raise ValueError("There isn't any query parameters")

    keys = list(params.keys())
    if "Cuantity" in keys:
        aux = read_database("mid_project", db_collection, {'Country/Region':'Spain'})
        params[aux[0].popitem()[0]] = params["Cuantity"]
        params.pop("Cuantity")

    operators = []
    for key, value in params.items():
        advance_query_dict = {}
        value = value.split(",")
        if value[0] in [">",">=","<", "<="]:
            for op in value[::2]:
                if op in [">",">=","<", "<="]:
                    operators.append(op)
                    value.remove(op)

            limits = value[:len(operators)]
            value = value[len(operators):]

            for element in range(len(operators)):
                advance_query_dict[dic_operators_to_query[operators[element]]] = int(limits[element])
        if len(value) >= 1:
            try:
                advance_query_dict['$in'] = [float(v) for v in value]
            except:
                advance_query_dict['$in'] = [v for v in value]
        params[key] = advance_query_dict
    return json_response(read_database("mid_project", db_collection, params, project))

#http://127.0.0.1:3500/post?Polaco=cześć&Despedida=Świat
@app.route("/post")
@handle_error
def write_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    correct_dim = {}
    for key,value in params.items():
        correct_value = value.replace('"','').replace("'","")
        correct_key = key.replace('"','').replace("'","")
        try:  
            correct_dim[correct_key] = float(correct_value)
        except:
            correct_dim[correct_key] = correct_value 
    return json_response(create_data("mid_project", "covid", correct_dim), 201)

#http://127.0.0.1:3500/delete?Polaco=cześć
@app.route("/delete")
@handle_error
def delete_db():
    condition = type_casting(**dict(request.args))
    if not condition:
        raise ValueError("There isn't any query parameters")
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
    return json_response(update_data("mid_project", "covid", query, new_data))

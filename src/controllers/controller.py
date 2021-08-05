from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import *
from utils.type_casting import type_casting, str_to_dict
from flask import request
import json
from app import app

dic_operators_to_query ={
    ">":"$gt",
    ">=":"$gte",
    "<":"$lt", 
    "<=":"$lte"
}

dic_db_collection = {
    "deaths":"deaths_covid",
    "recovered":"recovered_covid"
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
    found = False
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    try:
        print(f"{params = }")
        project = {element: 1 for element in params['project'].split(",")}
        params.pop("project")
        print(f"{params = }")
        for key, value in project.items():
            if key == "_id":
                found = True

        if "Total" in project:
            project["7/28/21"] = 1
            project.pop("Total")

        if not found:
            project["_id"] = 0
    except:
        project=None

    keys = list(params.keys())
    print(f"{keys = }")
    if "Cases" in keys:
        params["7/28/21"] = params["Cases"]
        params.pop("Cases")

    operators = []
    print(f"{params = }")
    for key, value in params.items():
        advance_query_dict = {}
        print(f"{key = }")
        value = value.split(",")
        print(f"{value = }")
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
        print(f"{advance_query_dict = }")
    return json_response(read_database("mid_project", db_collection, params, project))

#http://127.0.0.1:3500/post?Polaco=cześć&Despedida=Świat
@app.route("/post")
@handle_error
def write_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    print(params)
    return json_response(create_data("mid_project", "covid", params), 201)

#http://127.0.0.1:3500/delete?Polaco=cześć
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

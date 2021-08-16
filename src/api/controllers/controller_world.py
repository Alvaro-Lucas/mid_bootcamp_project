from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import *
from utils.type_casting import type_casting, str_to_dict
from utils.process_data import get_data_in_range, apply_interval, change_name_key
from utils.shortcuts import dic_db_collection_world
from flask import request
import json
from app import app

@app.route("/countries", methods = ['GET'])
@handle_error
def countries_names():
    project = {"_id":0,"Country/Region":1}
    data = read_database("mid_project", "covid", project=project)

    return json_response(data)


@app.route("/<db_collection>/data/<countries>", methods = ['GET'])
@handle_error
def list_countries_data(db_collection, countries):
    if countries != "All":
        countries_list = list(countries.split(","))
        match = {"Country/Region":{"$in":countries_list}}
    else:
        match = {}
    project = {"_id":0}
    data = read_database("mid_project", dic_db_collection_world[db_collection], match, project)

    return json_response(data)

@app.route("/coord/<countries>", methods = ['GET'])
@handle_error
def countries_coord(countries):
    if countries != "All":
        countries_list = list(countries.split(","))
        match = {"Country/Region":{"$in":countries_list}}
    else:
        match = {}
    project = {"_id":0, "Country/Region":1, "Lat":1, "Long":1}
    data = read_database("mid_project", "covid", match, project)

    return json_response(data)


@app.route("/<db_collection>/countries/total", methods = ['GET'])
@handle_error
def total_cases(db_collection):
    sp_template = read_database("mid_project", dic_db_collection_world[db_collection], {"Country/Region":"Spain"})
    last_date = sp_template[0].popitem()[0]

    project = {"_id":0, "Country/Region":1, last_date:1}
    countries_total = read_database("mid_project", dic_db_collection_world[db_collection], project=project)

    data = change_name_key(countries_total)

    return json_response(data)


@app.route("/<db_collection>/total/<countries>", methods = ['GET'])
@handle_error
def total_cases_per_country(db_collection, countries):
    countries_list = list(countries.split(","))

    match = {"Country/Region":{"$in":countries_list}}
    project = {"_id":0}

    countries_total = read_database("mid_project", dic_db_collection_world[db_collection], match, project)

    data = change_name_key(countries_total)

    return json_response(data)


@app.route("/<db_collection>/<countries>/date_range", methods = ['GET'])
@handle_error
def range_date_countries(db_collection, countries, date_range=None):
    if date_range == None:
        if not request.args or len(dict(request.args).keys()) != 2:
            raise ValueError(f"Expected 2 parameters and received {len(dict(request.args).keys())}")
        
        date_range = dict(request.args)

    countries_list = list(countries.split(","))
    
    match = {"Country/Region":{"$in":countries_list}}
    project = {"_id":0}
    countries_all_data = read_database("mid_project", dic_db_collection_world[db_collection], match, project)

    data = get_data_in_range(countries_all_data, date_range)

    return json_response(data)


@app.route("/<db_collection>/<countries>/date_interval", methods = ['GET'])
@handle_error
def interval_date_countries(db_collection, countries):
    interval = int(list(request.args)[0])
    countries_list = list(countries.split(","))

    match = {"Country/Region":{"$in":countries_list}}
    project = {"_id":0}
    countries_all_data = read_database("mid_project", dic_db_collection_world[db_collection], match, project)
    
    data = apply_interval(countries_all_data, interval)
    return json_response(data)


@app.route("/<db_collection>/<countries>/<interval>/date_range", methods = ['GET'])
@handle_error
def interval_date_range_countries(db_collection, countries, interval):
    interval = int(interval)
    date_range = dict(request.args)
    r_d_c = range_date_countries(db_collection, countries, date_range).json
    print(f"{r_d_c =}")
    data = apply_interval(r_d_c, interval)

    return json_response(data)

#http://127.0.0.1:3500/post?Polaco=cześć&Despedida=Świat
@app.route("/post", methods = ['POST'])
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
@app.route("/delete", methods = ['DELETE'])
@handle_error
def delete_db():
    condition = type_casting(**dict(request.args))
    if not condition:
        raise ValueError("There isn't any query parameters")
    return json_response(delete_data("mid_project", "covid", condition))

#http://127.0.0.1:3500/update?query=name=Hola,second=Mundo&new_data=name=Hello,second=World
@app.route("/update", methods = ['POST'])
@handle_error
def update_db():
    params = type_casting(**dict(request.args))
    if not params:
        raise ValueError("There isn't any query parameters")
    query = str_to_dict(params['query'])
    new_data = {"$set":str_to_dict(params['new_data'])}
    return json_response(update_data("mid_project", "covid", query, new_data))

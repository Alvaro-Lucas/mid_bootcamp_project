from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import *
from flask import request
from app import app


def retrieve_data_from_db(communities, p_show):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0}
    for item in p_show:
        project[item]=1

    data = read_database("mid_project", "ccaa_covid_data", match, project)

    return data

@app.route("/ccaa_covid_data/communities", methods = ['GET'])
@handle_error
def communities_names():
    project = {"_id":0,"Community":1}
    data = read_database("mid_project", "ccaa_covid_data", project=project)

    return json_response(data)


@app.route("/<db_collection>/<communities>/data", methods = ['GET'])
@handle_error
def communities_data(db_collection, communities):
    params = dict(request.args)
    project = {"_id":0}
    if "-" in list(params.keys()):
        for key in params["-"].split(","):
            project[key] = 0
    
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    
    data = read_database("mid_project", db_collection, match, project)

    return json_response(data)


@app.route("/<communities>/coord", methods = ['GET'])
@handle_error
def communities_coord(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Lat":1, "Long":1}
    data = read_database("mid_project", "ccaa_covid_data", match, project)

    return json_response(data)


@app.route("/ccaa_covid_data/<communities>/population", methods = ['GET'])
@handle_error
def communities_population(communities):
    print(f"{communities =}")
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
        print(f"{match =}")
    else:
        match = {}
    project = {"_id":0, "Community":1, "Population":1}
    data = read_database("mid_project", "ccaa_covid_data", match, project)

    return json_response(data)


@app.route("/ccaa_covid_data/<communities>/cases", methods = ['GET'])
@handle_error
def communities_cases(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Cases":1}
    data = read_database("mid_project", "ccaa_covid_data", match, project)

    return json_response(data)


@app.route("/ccaa_covid_data/<communities>/deceased", methods = ['GET'])
@handle_error
def communities_deceased(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Deaths":1}
    data = read_database("mid_project", "ccaa_covid_data", match, project)

    return json_response(data)


@app.route("/ccaa_covid_vac/<communities>/doses", methods = ['GET'])
@handle_error
def communities_doses(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Dosis administradas":1}
    data = read_database("mid_project", "ccaa_covid_vac", match, project)

    return json_response(data)


@app.route("/ccaa_covid_vac/<communities>/vaccinated_people", methods = ['GET'])
@handle_error
def communities_vaccinated_people(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Personas vacunadas":1}
    data = read_database("mid_project", "ccaa_covid_vac", match, project)

    return json_response(data)


@app.route("/ccaa_covid_vac/<communities>/full_vaccinated", methods = ['GET'])
@handle_error
def communities_full_vaccinated(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "Completamente vacunadas":1}
    data = read_database("mid_project", "ccaa_covid_vac", match, project)

    return json_response(data)


@app.route("/ccaa_covid_vac/<communities>/%_vaccinated", methods = ['GET'])
@handle_error
def communities_percent_vaccinated(communities):
    if communities != "All":
        match = {"Community":{"$in":list(communities.split(","))}}
    else:
        match = {}
    project = {"_id":0, "Community":1, "% completamente vacunadas":1}
    data = read_database("mid_project", "ccaa_covid_vac", match, project)

    return json_response(data)
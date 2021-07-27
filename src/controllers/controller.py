from utils.handle_error import handle_error
from utils.json_response import json_response
from utils.connection_db import read_database
from flask import request
import json
from app import app

@app.route("/all")
@handle_error
def get_all_info():
    match = request.args.get("search")
    project = request.args.get("project")

    print(f"{match = } {project = }")

    consulta = []
    if not match is None:
        consulta.append(json.loads(match))
        print(consulta[0])
    else:
        consulta.append({})
    if not project is None:
        consulta.append(json.loads(project))
        print(consulta[1])
    else:
        project = {"_id":0}
        for k in project.keys():
            project[k] = 1
        consulta.append({"_id":0, "name":1})

    data = read_database(consulta[0], consulta[1])
    return json_response(data)

from utils.connection_db import projectdb
from utils.handle_error import handle_error
from utils.json_response import json_response
from connection_db import read_database
import app
from flask import request


@app.route("/all")
@handle_error
def get_all_info():
    data = read_database()
    return json_response(data,status)

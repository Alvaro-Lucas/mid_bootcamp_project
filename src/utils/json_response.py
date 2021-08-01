from flask import Response
from bson.json_util import dumps, loads

def json_response(data, status=200):
    return Response(
        dumps(data),
        status,
        mimetype="application/json"  
    )
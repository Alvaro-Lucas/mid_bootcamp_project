from utils.json_response import json_response

def handle_error(fn):
    def wrapper(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except Exception as e:
            print("Se ha producido un error")
            print(e)
            return json_response({"error":str(e)}, 500)
    wrapper.__name__ = fn.__name__
    return wrapper
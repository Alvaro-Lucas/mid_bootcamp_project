from config import PORT
from app import app
from controllers import controller

app.run("0.0.0.0", PORT, debug=True)
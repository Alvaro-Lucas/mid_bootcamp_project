from app import app
from controllers import controller

app.run("0.0.0.0", "3500", debug=True)
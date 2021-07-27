import os
import dotenv

dotenv.load_dotenv()

PORT = dotenv.getenv("PORT")
user = dotenv.getenv("USER_ATLAS")
password = dotenv.getenv("PASS_ATLAS")
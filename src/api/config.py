import os
import dotenv

dotenv.load_dotenv()

PORT = os.getenv("PORT")
user = os.getenv("ATLAS_USER")
password = os.getenv("ATLAS_PASS")
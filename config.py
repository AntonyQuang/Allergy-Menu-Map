from dotenv import load_dotenv
import os

parent_folder = os.path.dirname(os.getcwd())
print(parent_folder)
print(os.path.join(parent_folder, '.env'))
load_dotenv(os.path.join(parent_folder, '.env'))
load_dotenv('.env')
flask_secret_key = os.getenv("flask_secret_key")
print(flask_secret_key)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
sqlalchemy_database_uri = os.getenv("sqlalchemy_database_uri")
ipinfo_token = os.getenv("ipinfo_token")

class Config:
    SECRET_KEY = flask_secret_key
    GOOGLEMAPS_KEY = GOOGLE_API_KEY
    GOOGLE_API_KEY = GOOGLE_API_KEY
    SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri
    ipinfo_token = ipinfo_token
    demo_user_email = "demo_user@example.com"
    demo_admin_email = "demo_admin@example.com"
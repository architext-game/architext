import os
from dotenv import load_dotenv
import json

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
env_file = f".env.{ENVIRONMENT}"
load_dotenv(env_file)
print(f"Using environment file {env_file}")
print(f"CLERK_SECRET_KEY: {os.getenv('CLERK_SECRET_KEY')}")
print(os.getenv('DB_PASSWORD'))
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
USE_MEMORY_DB = os.getenv('USE_MEMORY_DB') == 'true'
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
try:
    CORS_ALLOWED_ORIGINS = json.loads(os.environ['CORS_ALLOWED_ORIGINS'])
except json.JSONDecodeError:
    CORS_ALLOWED_ORIGINS = os.environ['CORS_ALLOWED_ORIGINS']
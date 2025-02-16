import os
from dotenv import load_dotenv

load_dotenv()

#App
APP_NAME=os.getenv("APP_NAME")
APP_HOST=os.getenv("APP_HOST")
APP_PORT=int(os.getenv("APP_PORT"))


#postgres
DB_USER     = os.getenv("DB_USER")
DB_PASSWD   = os.getenv("DB_PASSWD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = int(os.getenv("DB_PORT"))
DB_DB       = os.getenv("DB_DB")
DB_URL      = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_DB}"


CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS").split(",") 
DIR_LOG     = os.getenv("DIR_LOG")


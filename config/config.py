from dotenv import load_dotenv
from os import getenv

load_dotenv()

SQL_HOST = getenv("SQL_HOST", "127.0.0.1")
SQL_USER = getenv("SQL_USER", "root")
SQL_PORT = getenv("SQL_PORT", "5432")
SQL_PASSWORD = getenv("SQL_PASSWORD")
SQL_DATABASE = getenv("SQL_DATABASE")
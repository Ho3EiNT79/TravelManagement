import psycopg2
import travel.config as config

def get_db():
    cnx = psycopg2.connect(
        host=config.SQL_HOST,
        user=config.SQL_USER,
        password=config.SQL_PASSWORD,
        database=config.SQL_DATABASE,
    )
    return cnx
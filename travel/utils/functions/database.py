from travel.db import get_db
from travel import logger
import json
from datetime import datetime


def create_tables():
    cnx = get_db()
    cursor = cnx.cursor()
    sql_1 = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    username VARCHAR(32) NOT NULL,
    password VARCHAR(32) NOT NULL,
    phone_number VARCHAR(32) NOT NULL,
    email_number VARCHAR(32) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')));"""

    sql_2 = """CREATE TABLE IF NOT EXISTS travels (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    travel_type TEXT[] NOT NULL,
    vehicles JSONB NOT NULL);"""

    sql_3 = """CREATE TABLE IF NOT EXISTS reserves (
    id SERIAL PRIMARY KEY,
    travel_id INT NOT NULL REFERENCES travels(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    travel_type TEXT NOT NULL,
    price INTEGER NOT NULL,
    seat_numbers INT[] NOT NULL,
    travel_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    reserved_at TIMESTAMP DEFAULT now());"""

    cursor.execute(sql_1)
    cursor.execute(sql_2)
    cursor.execute(sql_3)
    cnx.commit()


def login_user_db(username, password):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""SELECT * FROM users WHERE username = %s AND password = %s;"""
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return False


def add_user_db(first_name, last_name, username, password, phone_number, email_number, role):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""INSERT INTO users (first_name, last_name, username, password, phone_number, email_number, role) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    values = (first_name, last_name, username, password, phone_number, email_number, role)
    cursor.execute(sql, values)
    cnx.commit()


# ----------User----------
def get_reserve_travel_db(origin, destination, travel_type):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = """SELECT id, origin, destination, vehicles FROM travels WHERE origin = %s AND destination = %s AND %s = ANY(travel_type);"""
    val = (origin, destination, travel_type)
    cursor.execute(sql, val)
    travels = cursor.fetchall()
    cursor.close()
    return travels


def update_travel_db(pk, vehicles):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = "UPDATE travels SET vehicles = %s WHERE id = %s;"
    val = (json.dumps(vehicles), pk)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()


def login_admin_db(username, password):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""SELECT role FROM users WHERE username = %s AND password = %s;"""
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()[0]
    cursor.close()
    return result == "admin"


# ----------Admin----------
def add_travel_db(origin, destination, travel_type, vehicles):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""INSERT INTO travels (origin, destination, travel_type, vehicles) VALUES (%s, %s, %s, %s);"""
    values = (origin, destination, travel_type, json.dumps(vehicles))
    cursor.execute(sql, values)
    cnx.commit()


def edit_travel_db(pk, origin, destination, travel_type, vehicles):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""UPDATE travels SET origin = %s, destination = %s, travel_type = %s, vehicles = %s WHERE id = %s;"""
    val = (origin, destination, travel_type, json.dumps(vehicles), pk)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()


def get_travels_db():
    cnx = get_db()
    cursor = cnx.cursor()
    cursor.execute("SELECT id, origin, destination, travel_type FROM travels;")
    travels = cursor.fetchall()
    cursor.close()
    return travels


def delete_travel_db(travel_id):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"""DELETE FROM travels WHERE id = %s;"""
    values = (travel_id,)
    a = cursor.execute(sql, values)
    print(a)
    cnx.commit()
    cursor.close()


def get_travel_by_id_db(travel_id):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = "SELECT vehicles FROM travels WHERE id = %s;"
    values = (travel_id,)
    cursor.execute(sql, values)
    travels = cursor.fetchone()[0]
    cursor.close()
    return travels


# ----------Reserves----------

def add_to_reserve_db(travel_id, user_id, travel_type, price, seat_numbers, travel_date):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = "INSERT INTO reserves (travel_id, user_id, travel_type, price, seat_numbers, travel_date) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (travel_id, user_id, travel_type, price, seat_numbers, datetime.strptime(travel_date, "%Y-%m-%d %H:%M"))
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()


def list_reserves_db(user_id=None):
    now = datetime.now()
    cnx = get_db()
    cursor = cnx.cursor()
    if user_id:
        user = f"AND user_id = {user_id}"
    else:
        user = ""
    sql = f"SELECT * FROM reserves WHERE travel_date >= %s {user};"
    val = (now,)
    cursor.execute(sql, val)
    results = cursor.fetchall()
    cursor.close()
    return results


def get_reserve_info(travel_id):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = "SELECT * FROM reserves WHERE id = %s;"
    val = (travel_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    return result


def del_reserve_db(travel_id):
    cnx = get_db()
    cursor = cnx.cursor()
    sql = f"DELETE FROM reserves WHERE id = %s;"
    val = (travel_id,)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()

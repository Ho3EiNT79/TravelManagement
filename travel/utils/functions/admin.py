from .database import add_travel_db, get_travels_db, delete_travel_db, edit_travel_db, list_reserves_db, login_admin_db, add_user_db
from datetime import datetime
from travel import logger


def register_superuser():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number: ")
    email_number = input("Enter your email number: ")
    add_user_db(first_name, last_name, username, password, phone_number, email_number, "admin")
    logger(__name__).info("SuperUser registered successfully")

def login_admin():
    from travel.utils.shell.admin_shell import AdminLoginShell
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if login_admin_db(username, password):
        logger(__name__).info(f"Login User: {username} successful")
        shell = AdminLoginShell()
        shell.cmdloop()
    else:
        print("Login failed")


def list_travels():
    travels = get_travels_db()
    travel_ids = []
    for pk, origin, destination, travel_types in travels:
        travel_ids.append(pk)
        print(f"Travel ID: {pk}, Origin: {origin}, Destination: {destination}, Vehicles: {travel_types}")
        print("-" * 80)
    return travel_ids


def add_travel():
    origin = input("Enter your origin address: ")
    destination = input("Enter your destination address: ")
    travel_types = input("Enter your travel type (like bus, train): ").replace(" ", "").split(",")
    travel_date = input("Enter your travel date(YYYY-MM-DD): ")
    vehicles = {}
    for travel_type in travel_types:
        hour = input(f"Enter your travel hour for {travel_type} (HH:MM): ")
        new_travel_date = datetime.strptime(f"{travel_date} {hour}", "%Y-%m-%d %H:%M")
        capacity = int(input(f"Enter your travel capacity for {travel_type}: "))
        price = int(input(f"Enter your travel price for {travel_type}: "))
        seat_data = {i: None for i in range(1, capacity + 1)}
        vehicles[travel_type] = {"travel_date": new_travel_date.strftime("%Y-%m-%d %H:%M"), "seat_data": seat_data,
                                 "price": price}
    add_travel_db(origin, destination, travel_types, vehicles)
    logger(__name__).info(f"Travel({origin} - {destination}) added successfully.")


def edit_travel():
    travels_ids = list_travels()
    pk = int(input("Please enter your travel id: "))
    if pk in travels_ids:
        origin = input("Enter your origin address: ")
        destination = input("Enter your destination address: ")
        travel_types = input("Enter your travel type (like bus, train): ").replace(" ", "").split(",")
        travel_date = input("Enter your travel date(YYYY-MM-DD): ")
        vehicles = {}
        for travel_type in travel_types:
            hour = input(f"Enter your travel hour for {travel_type} (HH:MM): ")
            new_travel_date = datetime.strptime(f"{travel_date} {hour}", "%Y-%m-%d %H:%M")
            capacity = int(input(f"Enter your travel capacity for {travel_type}: "))
            price = int(input(f"Enter your travel price for {travel_type}: "))
            seat_data = {i: None for i in range(1, capacity + 1)}
            vehicles[travel_type] = {"travel_date": new_travel_date.strftime("%Y-%m-%d %H:%M"), "seat_data": seat_data,
                                     "price": price}
        edit_travel_db(pk, origin, destination, travel_types, vehicles)
        logger(__name__).info(f"Travel({origin} - {destination}) edited successfully.")
    else:
        print(f"Travel {pk} does not exist")


def delete_travel():
    travel_ids = list_travels()
    try:
        pk = int(input("Please enter your id: "))
    except Exception as e:
        print(e)
        return delete_travel()
    if pk in travel_ids:
        delete_travel_db(pk)
        logger(__name__).info(f"Travel {pk} deleted successfully.")
    else:
        logger(__name__).info(f"Travel {pk} does not exist")
        return delete_travel()


def show_reserves_admin():
    tickets = list_reserves_db()
    for ticket in tickets:
        ticket_id, travel_id, user_id, travel_type, price, seat_numbers, travel_date, reserved_at = ticket
        txt = f"""Ticket ID: {ticket_id}
Travel ID: {travel_id}
User ID: {user_id}
Travel type: {travel_type}
Price: {price}
Seat numbers: {seat_numbers}
Travel date: {travel_date}
Buy date: {reserved_at}"""
        print(txt)
        print("-" * 35)

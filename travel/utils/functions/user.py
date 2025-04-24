from .database import get_reserve_travel_db, update_travel_db, add_to_reserve_db, list_reserves_db, get_reserve_info, \
    del_reserve_db, get_travel_by_id_db, add_user_db, login_user_db
from travel.misc import user_session
from travel import logger


def register_user():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number: ")
    email_number = input("Enter your email number: ")
    add_user_db(first_name, last_name, username, password, phone_number, email_number, "user")
    logger(__name__).info(f"User({username}) added successfully.")


def login_user():
    from travel.utils.shell.user_shell import UserLoginShell
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    pk = login_user_db(username, password)
    if pk:
        user_session['user_id'] = pk
        user_session['username'] = username
        print("Login successful")
        shell = UserLoginShell()
        shell.cmdloop()
    else:
        print("Login failed")


def reserve_travel():
    origin = input("Enter the origin of travel: ")
    destination = input("Enter the destination of travel: ")
    travel_type = input("Enter the type of travel: ")
    results = get_reserve_travel_db(origin, destination, travel_type)
    if not results:
        print("No reserve travel found")
        return reserve_travel()
    for num, result in enumerate(results, start=1):
        _, origin, destination, vehicle = result
        seat_data = vehicle[travel_type]
        empty_seats = [k for k, v in seat_data["seat_data"].items() if v is None]
        print(
            f"Number: {num}, Travel date: {seat_data['travel_date']}, Price: {seat_data['price']}, Empty seats: {len(empty_seats)}")
        print("-" * 20)
    user_id = user_session["user_id"]
    n = int(input(f"Please enter travel Number: "))
    pk, origin, destination, vehicle = results[n - 1]
    seat_data = vehicle[travel_type]
    empty_seats = {}
    for k, v in seat_data["seat_data"].items():
        empty_seats[k] = "reserved" if v else "empty"
    if not empty_seats:
        print(f"There are no available seats for travel ID {n}")
        return reserve_travel()
    else:
        print(empty_seats)
        choices = input("Choose your seats (like 1,2,3): ").replace(" ", "").split(",")
        for choice in choices:
            selected = empty_seats[choice]
            if not selected:
                print(f"{choice} is not available for travel ID {n}")
                return reserve_travel()
            if selected == "reserved":
                print(f"{choice} is reserved for travel ID {n}")
                return reserve_travel()
            else:
                vehicle[travel_type]["seat_data"][choice] = user_id

    update_travel_db(pk, vehicle)
    add_to_reserve_db(pk, user_id, travel_type, seat_data["price"], list(map(int, choices)), seat_data["travel_date"])
    print("Your seats have been successfully reserved. Thank you!")


def show_reserve_user():
    user_id = user_session["user_id"]
    tickets = list_reserves_db(user_id)
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


def cancel_reserve_user():
    show_reserve_user()
    selected = int(input("Please Select Ticket ID: "))
    reserve = get_reserve_info(selected)
    if not reserve:
        print("No reserve travel found")
        return cancel_reserve_user()
    reserve_id, travel_id, user_id, travel_type, price, seat_numbers, travel_date, reserved_at = reserve
    del_reserve_db(reserve_id)
    vehicles = get_travel_by_id_db(travel_id)
    for seat_number in seat_numbers:
        vehicles[travel_type]["seat_data"][seat_number] = None
    update_travel_db(travel_id, vehicles)

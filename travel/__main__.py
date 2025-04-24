import sys
from travel.utils.functions.database import create_tables
from travel.utils.functions.admin import login_admin, register_superuser
from travel.utils.functions.user import login_user, register_user
from travel import logger


def main():
    create_tables()
    logger(__name__).info("Tables created or checked")
    if len(sys.argv) != 2:
        print("Usage: python app.py <command>")
        sys.exit(1)
    command = sys.argv[1]
    if command == "register_user":
        register_user()
    elif command == "login_user":
        login_user()
    elif command == "login_admin":
        login_admin()
    elif command == "register_superuser":
        register_superuser()


if __name__ == "__main__":
    main()

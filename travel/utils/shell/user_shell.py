import cmd
from travel import logger
from travel.utils.functions import list_travels
from travel.utils.functions.user import reserve_travel, show_reserve_user, cancel_reserve_user


class UserLoginShell(cmd.Cmd):
    intro = 'Welcome to Travel Management Shell'
    prompt = '>>> '

    def do_exit(self, args):
        logger(__name__).info("Exit.")
        return True

    def do_reserve(self, args):
        reserve_travel()

    def do_show_reserves(self, args):
        show_reserve_user()

    def do_cancel_reserve(self, args):
        cancel_reserve_user()

    def do_list_travels(self, args):
        list_travels()
import cmd
from travel import logger
from travel.utils.functions import add_travel, list_travels, delete_travel, edit_travel, show_reserves_admin


class AdminLoginShell(cmd.Cmd):
    intro = 'Welcome to Travel Management Shell'
    prompt = '>>> '

    def do_exit(self, args):
        logger(__name__).info("Exit.")
        return True

    def do_add_travel(self, args):
        add_travel()

    def do_list_travels(self, args):
        list_travels()

    def do_del_travel(self, args):
        delete_travel()

    def do_edit_travel(self, args):
        edit_travel()

    def do_show_reserves(self, args):
        show_reserves_admin()

import curses
from contextlib import contextmanager

class InterfaceEngine:

    @contextmanager
    def get_interface():
        # TODO: do we need curses.wrapper() to handle unexpected crashes?
        interface = Interface()
        try:
            yield interface
        finally:
            interface.close()


class Interface:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def close(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()
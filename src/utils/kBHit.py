import sys
import termios
import atexit
from select import select


class KBHit:

    def __init__(self):
        """
        Creates a Key Board Hit object that you can call to do various keyboard things.
        https://stackoverflow.com/questions/2408560/python-nonblocking-console-input/22085679
        """

        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """
        Resets to normal terminal.  On Windows this is a no-op.
        """
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    @staticmethod
    def get_ch():
        """
         Returns a keyboard character after kbhit() has been called.
        """
        return sys.stdin.read(1)

    @staticmethod
    def kb_hit():
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []

    @staticmethod
    def clear():
        """
        Clears the input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

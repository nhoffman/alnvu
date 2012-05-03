import signal
import sys

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

def _exit_on_signal(sig, status=None, message=None):
    def exit(sig, frame):
        if message:
            print >> sys.stderr, message
        raise SystemExit(status)
    signal.signal(sig, exit)

def exit_on_sigint(status=1, message="Canceled."):
    """
    Set program to exit on SIGINT, with provided status and message.
    """
    _exit_on_signal(signal.SIGINT, status, message)

def exit_on_sigpipe(status=None):
    """
    Set program to exit on SIGPIPE
    """
    _exit_on_signal(signal.SIGPIPE, status)

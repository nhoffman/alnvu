import signal
import sys
from os.path import join, dirname

_data = join(dirname(__file__), 'data')

__version__ = '1.'

try:
    with open(join(_data, 'sha')) as s, open(join(_data, 'ver')) as v:
        sha = s.read().strip()
        ver = int(v.read())
except Exception, e:
    __version__ += '0'
else:
    __version__ += '%04i.%s' % (ver, sha)

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

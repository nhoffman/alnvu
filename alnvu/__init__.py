import signal
import sys
import glob
from os import path

_data = path.join(path.dirname(__file__), 'data')

try:
    with open(path.join(_data, 'ver')) as f:
        __version__ = f.read().strip().replace('-', '+', 1).replace('-', '.')
except Exception as e:
    __version__ = ''


def _exit_on_signal(sig, status=None, message=None):
    def exit(sig, frame):
        if message:
            sys.stderr.write(message)
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


def package_data(fname, pattern=None):
    """Return the absolute path to a file included in package data,
    raising ValueError if no such file exists. If `pattern` is
    provided, return a list of matching files in package data
    (ignoring `fname`).

    """

    if pattern:
        return glob.glob(path.join(_data, pattern))

    pth = path.join(_data, fname)

    if not path.exists(pth):
        raise ValueError('Package data does not contain the file %s' % fname)

    return pth

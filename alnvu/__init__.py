import signal
import sys
import glob
import os

from ._version import get_version

_data = os.path.join(os.path.dirname(__file__), 'data')
__version__ = get_version()


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


def package_data(fname, pattern=None, data_dir=_data):
    """Return the absolute path to a file included in package data,
    raising ValueError if no such file exists. If `pattern` is
    provided, return a list of matching files in package data
    (ignoring `fname`).

    """

    if pattern:
        return glob.glob(os.path.join(data_dir, pattern))

    pth = os.path.join(data_dir, fname)

    if not os.path.exists(pth):
        raise ValueError('Package data does not contain the file %s' % fname)

    return pth

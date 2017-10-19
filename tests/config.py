import sys
import logging
import re

log = logging


def funcname(idstr):
    return '.'.join(idstr.split('.')[1:])


try:
    logflag = re.findall(r'-[vq]+\b', ' '.join(sys.argv[1:]))[0]
except IndexError:
    logflag = ''

logging.basicConfig(
    stream=sys.stdout,
    format='%(levelname)s %(module)s %(lineno)s %(message)s'
    if logflag.startswith('-v') else '%(message)s',
    level={'-q': logging.ERROR,
           '': logging.WARNING,
           '-v': logging.INFO,
           '-vv': logging.DEBUG}[logflag]
)

# module data
datadir = 'testfiles'

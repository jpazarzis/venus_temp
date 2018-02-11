"""Implements health check callables to use for testing."""


def verify_fileaccess(host, user, passwd):
    return 'OK'


class MyException(Exception):
    """This is completely junk."""


def raising_exception():
    raise MyException('junk')


def check_mysql():
    pass

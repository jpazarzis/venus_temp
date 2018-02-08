try:
    import MySQLdb
except:
    import unittest.mock
    MySQLdb = unittest.mock.MagicMock()


def mysql_connect():
    pass

def mysql_schema():
    pass

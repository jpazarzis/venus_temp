try:
    import redis
except:
    import unittest.mock
    redis = unittest.mock.MagicMock()

def redis_connect():
    pass

def redis_access():
    pass

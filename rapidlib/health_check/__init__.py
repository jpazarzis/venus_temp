from .health_check import check_health
from .health_check import HealthCheckerError

__all__ = [
    'check_health',
    'HealthCheckerError'
]

__doc__ = """
health_checker - A library to allow for automatic health checks.
=====================================================================

Features
-------------
Exposes a function called check_health which receives a description of
the applicable tests which can be passed as yaml or json files or as a python
dictionary.  This function returns a description of the health of the system
as a python dictionary.

Examples of health check descriptions:

yaml sample: health_check.yaml

health_checks:
  check_redis_connection:
      callable: health_checks.check_redis
      parameters:
        server: localhost
        passwd: $PASSWORD

json sample: health_check.json

{
   "health_checks":{
      "check_redis_connection":{
         "callable":"health_checks.check_redis",
         "parameters":{
            "host":"localhost",
            "passwd":"$PASSWORD"
         }
      }
}

python dict sample:

health_checks = {
   "health_checks":{
      "check_redis_connection":{
         "callable":"health_checks.check_redis",
         "parameters":{
            "host":"localhost",
            "passwd":"$PASSWORD"
         }
      }
}

Example of a health check callable:

    >>> def check_redis(server, passwd):
    >>>    # Apply your checks and return a dict

You can now use this library using any of the supported formats (yaml - json -
dict) to build a checker and call it using the returned function object:

    >>> health = check_health('health_check.yaml')


Exception handling
------------------
This library is expected to raise only this exception:

    HealthCheckerError

who's message explains the specific reason of failure.
"""

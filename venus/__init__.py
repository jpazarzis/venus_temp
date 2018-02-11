from .health_check import make_health_checker
from .health_check import HealthCheckerError

__all__ = [
    'make_health_checker',
    'HealthCheckerError'
]


__doc__ = """
health_checker - A library to allow for automatic health checks.
=====================================================================

Features
-------------
Exposes a function called make_health_checker which receives a description of
the applicable tests which can be passed as yaml or json files or as a python
dictionary.  This function returns a function object which can be called using
the () notation to run all the health checks and return the applicable status
as a python dictionary.

Examples of use:

Using a yaml file:

Assuming the existence of the following yaml:

health_check.yaml
=================
health_checks:
  check_redis_connection:
      callable: health_checks.check_redis
      parameters:
        server: localhost
        passwd: $PASSWORD

and the existence of a function check_redis (which is implemented in a package
called health_checks) similar to the following::

>>> def check_redis(server, passwd):
>>>    # Apply your checks and return a dict

You can now use this library as follows::

>>> checker = make_health_checker()
>>> health_check = checker()

"""
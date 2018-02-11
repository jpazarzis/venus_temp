"""Implements the health check functionality."""

import importlib
import json
import yaml


class HealthCheckerError(Exception):
    """Used for any exception raised by HealthChecker."""


def make_health_checker(instructions):
    """Makes a health checker object.

    :parameter instructions: Must be one of the following types:

        - dict: Containing the health checks as a python dict.

        - str: A filename of one of the supported formats:

            - A yaml file containing the health checks.
            - A json file containing the health checks.

    :returns: A function object encapsulating the health check rules as they are
        described in the instructions.

        Calling this object returns a dictionary consisting of the description
        of the health check.

        The most important key in the response is called status and points to a
        boolean value which designates a healthy (True) or unhealthy (False)
        system.  Also contains all the specified checks with their
        underlined details and individual status.

    :raises HealthCheckerError: Redirects any possible exception that can raised
        to this generic exception.  Doing so to simplify the behaviour of the
        called who should only have a single catching scope.
    """
    try:
        if isinstance(instructions, str):
            if instructions.endswith('.yaml'):
                with open(instructions) as stream:
                    instructions = yaml.load(stream)
            elif instructions.endswith('.json'):
                instructions = json.load(open(instructions))
    except:
        raise HealthCheckerError

    if not isinstance(instructions, dict) or not instructions:
        raise HealthCheckerError

    heatlh_check_nodes = instructions.get('health_checks')
    if not heatlh_check_nodes:
        raise HealthCheckerError

    assert isinstance(heatlh_check_nodes, dict)

    checkers = [
        _HealthCheck(name, **attrs)
        for name, attrs in heatlh_check_nodes.items()
        ]

    return _HealthCheckCollection(checkers)


class _HealthCheckCollection(list):
    """Holds a collection of health checks.

    This is the function object that the user of this library receives when he
    makes a health checker.

    It consists of a list of the health checks that each of them will be
    executed when the object is called.  If all the checks are healthy then the
    status key of the response will be True (False otherwise).
    """

    def __call__(self):
        """Allows for 'function object' behaviour.

        :returns: A dictionary consisting of a composite of the results of all
            the contained health checks.
        """
        heatlh_check_results = {c.name: c() for c in self}

        return {
            'status': all(c['status'] for c in heatlh_check_results.values()),
            'checks': heatlh_check_results
        }


class _HealthCheck:
    """Encapsulates the details of an individual health check."""

    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def function_to_execute(self):
        """The function that is specified by the configuration.

        :raises: TypeError: When unable to resolve the function.

        :returns: A callable that is loaded using the path that is specified
            in the configuration file or the dict used.
        """
        try:
            module_name, function_name = self.callable.rsplit('.', 1)
        except (TypeError, ValueError):
            raise TypeError
        my_module = importlib.import_module(module_name)
        return getattr(my_module, function_name)

    def __call__(self, *args, **kwargs):
        """Executed when the user calls the object using the () notation.

        :returns: A dictionary containing the related information.
        """
        result = {}
        try:
            if hasattr(self, 'parameters'):
                self.function_to_execute(**self.parameters)
            else:
                self.function_to_execute()
            # If the function to execute completes without raising an exception
            # we do not need any further information aside from marking its
            # status as True.
            result['status'] = True
        except Exception as ex:
            # The function to execute raised an exception so we need to inform
            # the user for it by adding the necessary keys to the dictionary
            # that will be returned to him.
            if isinstance(ex, Exception):
                exception_type = type(ex).__name__
            else:
                exception_type = ex.__name__

            result['status'] = False
            result['exception'] = '%s %s' % (exception_type, str(ex))
            result['desc'] = str(ex)
        return result

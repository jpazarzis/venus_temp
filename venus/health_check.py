import yaml
import importlib

_SUPPORTED_FILE_EXTENSIONS = ['.yaml', '.json']


def make_health_checker(instructions):
    """Makes a health checker object.

    :parameter instructions: Must be one of the following types:
        - dict: Containing the health checks as a python dict.
        - str: A filename of one of the supported formats:
            - A yaml file containing the health checks.
            - A json file containing the health checks.

    :raises InvalidFilenameError: Unsupported filename.
    :raises FileNotFoundError: File does not exist.
    :raises SyntaxError: File is invalid.
    :raises ValueError: Invalid instructions were passed.
    """
    if isinstance(instructions, str):
        # instructions must point to a filename.
        if not any(
                instructions.endswith(extension)
                for extension in _SUPPORTED_FILE_EXTENSIONS):
            raise NameError('Invalid Filename: % s ' % instructions)
        elif instructions.endswith('.yaml'):
            with open(instructions) as stream:
                try:
                    instructions = yaml.load(stream)
                except yaml.parser.ParserError:
                    raise SyntaxError(
                        "Invalid format in yaml file %s" % instructions
                    )

    if not isinstance(instructions, dict) or not instructions:
        raise ValueError("Invalid instructions: %s" % instructions)

    heatlh_check_nodes = instructions.get('health_checks')
    if not heatlh_check_nodes:
        raise SyntaxError(
            "Invalid format in health check instructions."
        )

    assert isinstance(heatlh_check_nodes, dict)

    checkers = [
        _HealthCheck(name, **attrs)
        for name, attrs in heatlh_check_nodes.items()
        ]

    return _HealthCheckCollection(checkers)


class _HealthCheckCollection(list):
    """Holds a collection of health checks."""

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
    """Encapsulates the details of an individual health check.

    The health check which w

    """
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def function_to_execute(self):
        try:
            module_name, function_name = self.callable.rsplit('.', 1)
        except (TypeError, ValueError):
            raise TypeError("Need a valid target to patch.")
        my_module = importlib.import_module(module_name)
        return getattr(my_module, function_name)

    def __call__(self, *args, **kwargs):
        result = {}
        try:
            if hasattr(self, 'parameters'):
                _ = self.function_to_execute(**self.parameters)
            else:
                _ = self.function_to_execute()
            result['status'] = True
        except Exception as ex:
            if isinstance(ex, Exception):
                exception_type = type(ex).__name__
            else:
                exception_type = ex.__name__

            result['status'] = False
            result['exception'] = '%s %s' % (exception_type, str(ex))
            result['desc'] = str(ex)
        return result

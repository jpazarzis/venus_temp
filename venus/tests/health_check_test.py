import os
import unittest

from venus import apply_health_checks

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
_RESOURCES_DIR = os.path.join(_CURRENT_DIR, 'resources')
_HEALTH_CHECKS_FILENAME = os.path.join(_RESOURCES_DIR, 'health-checks.yaml')


class TestHealthCheck(unittest.TestCase):
    def test_loading_health_check_script(self):
        apply_health_checks(_HEALTH_CHECKS_FILENAME)

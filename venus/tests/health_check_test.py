import os
import unittest

from venus import make_health_checker

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
_RESOURCES_DIR = os.path.join(_CURRENT_DIR, 'resources')
_UNHEALTHY_HEALTH_CHECKS = os.path.join(
    _RESOURCES_DIR, 'failing-health-checks.yaml')
_HEALTHY_HEALTH_CHECKS = os.path.join(
    _RESOURCES_DIR, 'success-health-checks.yaml')

_INALID_YAMLS = [
    os.path.join(_RESOURCES_DIR, 'invalid_1.yaml'),
    os.path.join(_RESOURCES_DIR, 'invalid_2.yaml'),
]

_INSTRUCTIONS_1 = {
    'health_checks': {
        'check_redis_connection':
            {
                'callable': 'venus.verify_fileaccess',
                'parameters': {
                    'host': 'localhost',
                    'user': 'root',
                    'passwd': 'vagrant'
                }
            }
    }
}

_INSTRUCTIONS_2 = {
    'health_checks':
        {
            'check_redis_connection':
                {
                    'parameters':
                        {
                            'user': 'root',
                            'host': 'localhost',
                            'passwd': 'ΧΧΧΧ'
                        },
                    'callable': 'venus.verify_fileaccess'
                },
            'a_malfunctioning_example':
                {
                    'callable': 'venus.raising_exception'
                }
        }
}


class TestHealthCheck(unittest.TestCase):
    def test_unsupported_filename(self):
        with self.assertRaises(NameError):
            make_health_checker('_unsupported')

    def test_non_existing_yaml(self):
        with self.assertRaises(FileNotFoundError):
            make_health_checker('_unsupported.yaml')

    def test_invalid_yaml(self):
        for invalid_file in _INALID_YAMLS:
            with self.assertRaises(SyntaxError):
                make_health_checker(invalid_file)

    def test_unhealthy_from_yaml(self):
        health_checks = make_health_checker(_UNHEALTHY_HEALTH_CHECKS)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['a_malfunctioning_example', 'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names), sorted(expected_names))
        health = health_checks()
        self.assertTrue(isinstance(health['status'], bool))
        self.assertFalse(health['status'])


    def test_healthy_from_yaml(self):
        health_checks = make_health_checker(_HEALTHY_HEALTH_CHECKS)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['check_mysql',
                          'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names),
                             sorted(expected_names))

        health = health_checks()

        self.assertTrue(isinstance(health['status'], bool))
        self.assertTrue(health['status'])

    def test_invalid_instructions(self):
        invalid_instructions = [
            123,
            ['a'],
            {},
            lambda: 1
        ]
        for instruction in invalid_instructions:
            with self.assertRaises(ValueError):
                make_health_checker(instruction)

    def test_loading_from_dict(self):
        health_checks = make_health_checker(_INSTRUCTIONS_2)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['a_malfunctioning_example', 'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names), sorted(expected_names))

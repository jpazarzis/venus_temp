"""Tests rapidlib.health_check.make_health_checker"""

import os
import unittest
import unittest.mock as mock

import rapidlib.health_check.health_check
import rapidlib.health_check.tests.dummy_callables as dummy_callables
from rapidlib.health_check import HealthCheckerError
from rapidlib.health_check import check_health
from rapidlib.health_check.health_check import _make_health_checker


class TestLoadingFromYaml(unittest.TestCase):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    YAML_DIR = os.path.join(CURRENT_DIR, 'resources', 'yaml-samples')
    UNHEALTHY_YAML = os.path.join(YAML_DIR, 'unhealthy.yaml')
    HEALTHY_YAML = os.path.join(YAML_DIR, 'healthy.yaml')
    USING_ENV_VAR = os.path.join(YAML_DIR, 'using-env-variable.yaml')

    INALID_YAMLS = [
        os.path.join(YAML_DIR, 'invalid.yaml'),
        os.path.join(YAML_DIR, 'bad-structure.yaml'),
        os.path.join(YAML_DIR, 'missing-callable.yaml'),
    ]

    def test_unsupported_filename(self):
        with self.assertRaises(HealthCheckerError):
            check_health('_unsupported')

    def test_non_existing_yaml(self):
        with self.assertRaises(HealthCheckerError):
            check_health('_unsupported.yaml')

    def test_invalid_yaml(self):
        for invalid_file in self.INALID_YAMLS:
            with self.assertRaises(HealthCheckerError):
                check_health(invalid_file)

    def test_unhealthy_from_yaml(self):
        health_checks = _make_health_checker(self.UNHEALTHY_YAML)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['a_malfunctioning_example', 'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names), sorted(expected_names))
        health = health_checks()
        self.assertTrue(isinstance(health['status'], bool))
        self.assertFalse(health['status'])

    def test_healthy_from_yaml(self):
        health_checks = _make_health_checker(self.HEALTHY_YAML)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['check_mysql',
                          'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names),
                             sorted(expected_names))

        health = health_checks()

        self.assertTrue(isinstance(health['status'], bool))
        self.assertTrue(health['status'])

    def test_nonexisting_env_variable(self):
        with self.assertRaises(HealthCheckerError):
            check_health(self.USING_ENV_VAR)

    @mock.patch.object(rapidlib.health_check.health_check, 'os')
    @mock.patch.object(dummy_callables, 'verify_fileaccess')
    def test_env_variable(self, mocked_verify_fileaccess, mocked_os):
        mocked_os.environ = {'PASSWORD': 'dummy_pass'}
        health = check_health(self.USING_ENV_VAR)
        self.assertTrue(health['status'])
        mocked_verify_fileaccess.assert_called_with(
            host='localhost',
            user='root',
            passwd='dummy_pass'
        )


class TestLoadingFromDict(unittest.TestCase):
    VALID_INSTRUCTIONS = {
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
                        'callable': 'rapidlib.health_check.verify_fileaccess'
                    },
                'a_malfunctioning_example':
                    {
                        'callable': 'rapidlib.health_check.raising_exception'
                    }
            }
    }

    INVALID_INSTRUCTIONS = [123, ['a'], {}, lambda: 1]

    def test_invalid_instructions(self):
        for instruction in self.INVALID_INSTRUCTIONS:
            with self.assertRaises(HealthCheckerError):
                _make_health_checker(instruction)

    def test_loading_from_dict(self):
        health_checks = _make_health_checker(self.VALID_INSTRUCTIONS)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['a_malfunctioning_example', 'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names), sorted(expected_names))


class TestLoadingFromJson(unittest.TestCase):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    JSON_DIR = os.path.join(CURRENT_DIR, 'resources', 'json-samples')
    UNHEALTHY_JSON = os.path.join(JSON_DIR, 'unhealthy.json')
    HEALTHY_JSON = os.path.join(JSON_DIR, 'healthy.json')
    USING_ENV_VAR = os.path.join(JSON_DIR, 'using-env-variable.json')

    INALID_JSONS = [
        os.path.join(JSON_DIR, 'invalid.json'),
        os.path.join(JSON_DIR, 'bad-structure.json'),
    ]

    def test_unsupported_filename(self):
        with self.assertRaises(HealthCheckerError):
            check_health('_unsupported')

    def test_non_existing_json(self):
        with self.assertRaises(HealthCheckerError):
            check_health('_unsupported.json')

    def test_invalid_json(self):
        for invalid_file in self.INALID_JSONS:
            with self.assertRaises(HealthCheckerError):
                check_health(invalid_file)

    def test_make_health_checker(self):
        health_checks = _make_health_checker(self.UNHEALTHY_JSON)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['a_malfunctioning_example', 'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names), sorted(expected_names))

    def test_unhealthy_from_json(self):
        health = check_health(self.UNHEALTHY_JSON)
        self.assertTrue(isinstance(health['status'], bool))
        self.assertFalse(health['status'])

    def test_healthy_from_json(self):
        health_checks = _make_health_checker(self.HEALTHY_JSON)
        self.assertEqual(len(health_checks), 2)
        retrieved_names = [hc.name for hc in health_checks]
        expected_names = ['check_mysql',
                          'check_redis_connection']
        self.assertListEqual(sorted(retrieved_names),
                             sorted(expected_names))

        health = check_health(self.HEALTHY_JSON)
        self.assertTrue(isinstance(health['status'], bool))
        self.assertTrue(health['status'])

    def test_nonexisting_env_variable(self):
        with self.assertRaises(HealthCheckerError):
            check_health(self.USING_ENV_VAR)

    @mock.patch.object(rapidlib.health_check.health_check, 'os')
    @mock.patch.object(dummy_callables, 'verify_fileaccess')
    def test_env_variable(self, mocked_verify_fileaccess, mocked_os):
        mocked_os.environ = {'PASSWORD': 'dummy_pass'}
        health = check_health(self.USING_ENV_VAR)
        self.assertTrue(health['status'])
        mocked_verify_fileaccess.assert_called_with(
            host='localhost',
            user='root',
            passwd='dummy_pass'
        )

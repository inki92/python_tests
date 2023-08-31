import subprocess
import time
import unittest
import requests
import tests.unittest.common.data as test_data
from parameterized import parameterized
from tests.unittest.logger.logger import logger
from retrying import retry


class APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start the Docker container for the REST app and get headers."""
        cls.start_container()
        try:
            cls.connection_attempt()
        except requests.exceptions.ConnectTimeout as e:
            logger.error('Could not establish a connection to API')
            raise e
        else:
            logger.info('Connection try to API successful')
        cls.authorization()
        logger.info('Pre-test conditions setup completed successfully.')

    @classmethod
    def start_container(cls):
        """Start REST app container"""
        try:
            subprocess.run(
                ['/usr/local/bin/docker-compose', 'up', '-d'],
                check=True
            )
            logger.info(
                'Docker container with rest app has been started successfully.'
            )
        except Exception as e:
            logger.error('Running of REST API container failed. '
                         'Check path to docker application or '
                         'docker container.')
            raise e

    @classmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def connection_attempt(cls):
        """REST app API connection test."""
        # URL for request
        r_url = test_data.API_URL
        requests.get(r_url, timeout=3)

    @classmethod
    def authorization(cls):
        """Get authorization headers"""
        try:
            # Log in and get an access token
            # URL for login request
            r_url = test_data.API_URL + 'login'
            # json data for login request
            r_json = {'username': test_data.TRUE_LOGIN_NAME,
                      'password': test_data.TRUE_LOGIN_PASS}
            token = requests.post(r_url, json=r_json).json()
            cls.headers = {
                'Authorization': f"Bearer {token['access_token']}"
            }
            logger.info('Authorization token successfully created.')
        except requests.exceptions.RequestException as e:
            logger.error("Authorization attempt failed.")
            raise e

    @classmethod
    def tearDownClass(cls):
        """Stop the Docker container after tests"""
        subprocess.run(
            ['/usr/local/bin/docker-compose', 'down'],
            check=True
        )
        logger.info('Docker container with REST app has been stopped.')

    def test_01_api_response(self):
        """
        TEST CASE 1. Check if the application API is available.

        Basic test for check availability status of the application API.
        Get init message from the app.
        TEST DATA:
            INIT_MESSAGE - message from app API about OK status,
            API_URL      - url for API of application.
        """
        logger.info("Testcase 'test_01_api_response'")
        # URL for init request
        r_url = test_data.API_URL
        output = requests.get(r_url).json()
        self.assertEqual(test_data.INIT_MESSAGE, output)

    # Parametrize data for 2 and 3 test cases with same test.
    @parameterized.expand([
        (
                test_data.TRUE_LOGIN_NAME,
                test_data.TRUE_LOGIN_PASS,
                test_data.LOGIN_MESSAGE
        ),
        (
                test_data.WRONG_LOGIN_NAME,
                test_data.WRONG_LOGIN_PASS,
                test_data.LOGIN_MESSAGE_NEGATIVE
        ),
    ])
    def test_02_3_login(self, user, password, expected_result):
        """
        TEST CASE 2, 3. Check login to the server.

        2. Login to the server and receive access token.
        3. Negative. Login to the server with bad credentials attempt.
        TEST DATA:
        General:
            API_URL - url for API of application.
        For positive scenario:
            TRUE_LOGIN_NAME, TRUE_LOGIN_PASS - existed credentials,
            LOGIN_MESSAGE - message with access token.
        For negative scenario:
            WRONG_LOGIN_NAME, WRONG_LOGIN_PASS - not existed credentials,
            LOGIN_MESSAGE_NEGATIVE - no such username or password message.
         """
        logger.info("Testcase 'test_02_3_login'")
        # URL for login request
        r_url = test_data.API_URL + 'login'
        # json data for login request
        r_json = {'username': user, 'password': password}
        output = requests.post(r_url, json=r_json).json()
        self.assertIn(expected_result, str(output))

    # Parametrize data for 4 and 6 test cases with same test.
    @parameterized.expand([
        (
                test_data.ADD_TEST_SUITE_DATA,
                test_data.ADD_TEST_SUITE_MESSAGE,
                test_data.SUCCESS_CODE
        ),
        (
                test_data.ADD_TEST_SUITE_DATA_NEGATIVE,
                test_data.ADD_TEST_SUITE_MESSAGE_NEGATIVE,
                test_data.BAD_REQ_BODY_CODE
        ),
    ])
    def test_04_6_add_test_suite(self, add_test_suite_data,
                                 expected_result, expected_result_code):
        """
        TEST CASE 4, 6. Check adding test suite.

        4. Create new test suite.
        6. Negative. Add test suite attempt without 'title' value.
        TEST DATA:
        General:
            API_URL - url for API of application.
        For positive scenario:
            ADD_TEST_SUITE_DATA - correct data for creation test suite,
            ADD_TEST_SUITE_MESSAGE - message about successful creation,
            SUCCESS_CODE - status code of successful creation.
        For negative scenario:
            ADD_TEST_SUITE_DATA_NEGATIVE - incorrect data for creation suite,
            ADD_TEST_SUITE_MESSAGE_NEGATIVE - message about bad data,
            BAD_REQ_BODY_CODE - error status code.
        """
        logger.info("Testcase 'test_04_6_add_test_suite'")
        # URL for add test suite request
        r_url = test_data.API_URL + 'test_suites'
        # json data for add test suite request
        r_json = add_test_suite_data
        output = requests.post(r_url, headers=self.headers, json=r_json)
        self.assertEqual(expected_result_code, output.status_code)
        self.assertIn(expected_result, str(output.json()))

    def test_05_show_test_suites(self):
        """
        TEST CASE 5. Check showing existed test suites.

        Get all existed test suites.
        TEST DATA:
            API_URL            - url for API of application.
            EXISTED_TEST_CASES - message with test suite from test case 4.
        """
        logger.info("Testcase 'test_05_show_test_suites'")
        # URL for show test suite request
        r_url = test_data.API_URL + 'test_suites'
        output = requests.get(r_url, headers=self.headers).json()
        self.assertEqual(test_data.EXISTED_TEST_CASES, output)

    # Parametrize data for 7 and 8 test cases with same test.
    @parameterized.expand([
        (
                test_data.SUITE_ID,
                test_data.TEST_CASE_TITLE,
                test_data.TEST_CASE_DESCRIPTION,
                test_data.ADD_TEST_CASE_MESSAGE
        ),
        (
                test_data.WRONG_SUITE_ID,
                test_data.WRONG_CASE_TITLE,
                test_data.WRONG_CASE_DESCRIPTION,
                test_data.ADD_TEST_CASE_MESSAGE_NEGATIVE
        )
    ])
    def test_07_8_add_test_case(self, suite_id, title,
                                description, expected_result):
        """
        TEST CASE 7, 8. Check adding new test-case.

        7. Create new test-case.
        8. Negative. Add new test-case to nonexistent test-suite attempt.
        TEST DATA:
        General:
            API_URL - url for API of application.
        For positive scenario:
            SUITE_ID, TEST_CASE_TITLE,
            TEST_CASE_DESCRIPTION - correct data for adding test case,
            ADD_TEST_CASE_MESSAGE - message about successful adding.
        For negative scenario:
            WRONG_SUITE_ID, WRONG_CASE_TITLE,
            WRONG_CASE_DESCRIPTION - incorrect data for adding test case,
            ADD_TEST_CASE_MESSAGE_NEGATIVE - error message about adding.
        """
        logger.info("Testcase 'test_07_8_add_test_case'")
        # URL for add test case request
        r_url = test_data.API_URL + 'test_cases'
        # json data for add test case request
        r_json = {"suiteID": suite_id,
                  "title": title,
                  "description": description}
        output = requests.post(r_url, headers=self.headers, json=r_json).json()
        self.assertEqual(expected_result, output)

    def test_09_update_test_case(self):
        """
        TEST CASE 9. Check updating data for test-case.

        Update data('description') for existed test-case.
        TEST DATA:
            API_URL                   - url for API of application.
            SUITE_ID                  - existed suite id,
            TEST_CASE_TITLE           - test case title from test case 7,
            TEST_CASE_DESCRIPTION_UPD - update test case description,
            UPDATE_TEST_CASE_MESSAGE  - testcase info with updated description.
        """
        logger.info("Testcase 'test_09_update_test_case'")
        # URL for update test case request
        r_url = test_data.API_URL + 'test_cases/1'
        # json data for update test case request
        r_json = {"suiteID": test_data.SUITE_ID,
                  "title": test_data.TEST_CASE_TITLE,
                  "description": test_data.TEST_CASE_DESCRIPTION_UPD}
        output = requests.put(r_url, headers=self.headers, json=r_json).json()
        self.assertEqual(test_data.UPDATE_TEST_CASE_MESSAGE, output)

    def test_10_get_test_case_data(self):
        """
        TEST CASE 10. Check get data for test-case.

        Get data for existed test-case.
        TEST DATA:
            API_URL            - url for API of application.
            GET_TEST_CASE_DATA - message with data of existed test case.
        """
        logger.info("Testcase 'test_10_get_test_case_data'")
        # URL for get test case request
        r_url = test_data.API_URL + 'test_cases/1'
        output = requests.get(r_url, headers=self.headers).json()
        self.assertEqual(test_data.GET_TEST_CASE_DATA, output)

    def test_11_delete_test_case(self):
        """
        TEST CASE 11. Check deleting test-case.

        Delete test-case.
        TEST DATA:
            API_URL                   - url for API of application.
            TEST_CASE_DEL_MESSAGE     - message about successful deletion,
            TEST_CASE_DEL_GET_MESSAGE - message about absent test case.
        """
        logger.info("Testcase 'test_11_delete_test_case'")
        # URL for delete test case request
        r_url = test_data.API_URL + 'test_cases/1'
        output_del = requests.delete(r_url, headers=self.headers).json()
        output_get = requests.get(r_url, headers=self.headers).json()
        self.assertEqual(test_data.TEST_CASE_DEL_MESSAGE, output_del)
        self.assertEqual(test_data.TEST_CASE_DEL_GET_MESSAGE, output_get)

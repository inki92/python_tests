import requests
import unittest
from unittest.mock import Mock, patch
from tests.unittest.logger.logger import logger
import tests.unittest.common.data as test_data


class APITestMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Authorization imitation with fake token."""
        cls.headers = {'Authorization': 'Bearer "268 symbol token"'}

    @patch('requests.post')
    def test_add_test_suite_mock(self, mock_post):
        """
        TEST CASE 4. Check adding test suite.

        4. Create new test suite.
        TEST DATA:
            ADD_TEST_SUITE_DATA    - correct data for creation test suite,
            ADD_TEST_SUITE_MESSAGE - message about successful creation,
            SUCCESS_CODE           - status code of successful creation,
            API_URL                - url for API of application.
        """
        logger.info("Testcase 'test_add_test_suite_mock'")
        expected_result = test_data.ADD_TEST_SUITE_MESSAGE
        # Set return values for the mocks
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_data.ADD_TEST_SUITE_MESSAGE
        mock_post.return_value = mock_response
        # URL for add test suite request
        r_url = test_data.API_URL + 'test_suites'
        # Do request.post
        output = requests.post(
            r_url, headers=self.headers, json=test_data.ADD_TEST_SUITE_DATA
        )
        # Check that mock was called
        mock_post.assert_called_once_with(
            r_url, headers=self.headers, json=test_data.ADD_TEST_SUITE_DATA
        )
        self.assertIn(expected_result, str(output.json()))
        self.assertEqual(test_data.SUCCESS_CODE, output.status_code)

    @patch('requests.post')
    def test_add_test_case_mock(self, mock_post):
        """
        TEST CASE 7. Check adding new test-case.

        7. Create new test-case.
        TEST DATA:
        For positive scenario:
            SUITE_ID, TEST_CASE_TITLE,
            TEST_CASE_DESCRIPTION - correct data for adding test case,
            ADD_TEST_CASE_MESSAGE - message about successful adding,
            API_URL               - url for API of application.
        """
        logger.info("Testcase 'test_add_test_case_mock'")
        expected_result = test_data.ADD_TEST_CASE_MESSAGE
        mock_response = Mock()
        mock_response.json.return_value = test_data.ADD_TEST_CASE_MESSAGE
        mock_post.return_value = mock_response
        # URL for add test case request
        r_url = test_data.API_URL + 'test_cases'
        # json data for request
        r_json = {"suiteID": test_data.SUITE_ID,
                  "title": test_data.TEST_CASE_TITLE,
                  "description": test_data.TEST_CASE_DESCRIPTION}
        output = requests.post(
            r_url, headers=self.headers, json=r_json).json()
        mock_post.assert_called_once_with(
            r_url, headers=self.headers, json=r_json)
        self.assertEqual(expected_result, output)

    @patch('requests.get')
    @patch('requests.delete')
    def test_delete_test_case_mock(self, mock_delete, mock_get):
        """
        TEST CASE 11. Check deleting test-case.

        Delete test-case.
        TEST DATA:
            TEST_CASE_DEL_MESSAGE     - message about successful deletion,
            TEST_CASE_DEL_GET_MESSAGE - message about absent test case,
            API_URL                   - url for API of application.
        """
        logger.info("Testcase 'test_delete_test_case_mock'")
        # Create instances
        mock_response_delete = Mock()
        mock_response_get = Mock()
        # Return values definition for json method
        mock_response_delete.json.return_value = \
            test_data.TEST_CASE_DEL_MESSAGE
        mock_response_get.json.return_value = \
            test_data.TEST_CASE_DEL_GET_MESSAGE
        # Set return values for mocks
        mock_delete.return_value = mock_response_delete
        mock_get.return_value = mock_response_get
        # URL for test case delete request
        r_url = test_data.API_URL + 'test_cases/1'
        # Requests with mocks
        output_del = requests.delete(
            r_url, headers=self.headers).json()
        output_get = requests.get(
            r_url, headers=self.headers).json()
        # Check those mocks were called with correct parameters
        mock_delete.assert_called_once_with(
            r_url, headers=self.headers)
        mock_get.assert_called_once_with(
            r_url, headers=self.headers)
        # Check asserts
        self.assertEqual(test_data.TEST_CASE_DEL_MESSAGE, output_del)
        self.assertEqual(test_data.TEST_CASE_DEL_GET_MESSAGE, output_get)

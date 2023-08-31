"""Module with test data for REST app api testing."""

# URL for API of app
API_URL = 'http://127.0.0.1:5000/api/v1/'

# Test data for test case 1
# Check if the application API is available
INIT_MESSAGE = {'message': 'Simple Test Management System API'}

# Test data for test case 2
# Check login to the server.
TRUE_LOGIN_NAME = 'test'
TRUE_LOGIN_PASS = 'test'
LOGIN_MESSAGE = 'access_token'

# Test data for test case 3
# Check login to the server. Negative
WRONG_LOGIN_NAME = 'user'
WRONG_LOGIN_PASS = 'password'
LOGIN_MESSAGE_NEGATIVE = 'No such username or password'

# Test data for test case 4
# Check if the application API is available
SUITE_ID = "1"
SUITE_TITLE = "suite_id_1"
SUITE_DESCRIPTION = SUITE_TITLE
SUCCESS_CODE = 200
ADD_TEST_SUITE_MESSAGE = 'suite successfully added'
ADD_TEST_SUITE_DATA = {
    "suitID": SUITE_ID, "title": SUITE_TITLE,
    "description": SUITE_DESCRIPTION
}

# Test data for test case 5
# Check showing existed test suites
EXISTED_TEST_CASES = {
    'test_suites': [
        {'cases': [], 'id': SUITE_ID,
         'length': '0', 'title': SUITE_TITLE}
    ]
}

# Test data for test case 6
# Check adding test suite. Negative
WRONG_SUITE_ID = "2"
WRONG_SUITE_DESCRIPTION = "suite_id_2"
ADD_TEST_SUITE_DATA_NEGATIVE = {
    "suitID": WRONG_SUITE_ID,
    "description": WRONG_SUITE_DESCRIPTION
}
BAD_REQ_BODY_CODE = 400
ADD_TEST_SUITE_MESSAGE_NEGATIVE = 'Bad request body'

# Test data for test case 7
# Check adding new test-case
TEST_CASE_TITLE = "testcase_1"
TEST_CASE_DESCRIPTION = "test_case_sample"
ADD_TEST_CASE_MESSAGE = {'id': '1', 'message': 'Test case successfully added'}

# Test data for test case 8
# Check adding new test-case. Negative
WRONG_CASE_TITLE = "testcase_2"
WRONG_CASE_DESCRIPTION = "test_case_negative"
ADD_TEST_CASE_MESSAGE_NEGATIVE = {'message': 'Test suite does not exist'}

# Test data for test case 9
# Check updating data for test-case
TEST_CASE_DESCRIPTION_UPD = "test_case_sample_change"
UPDATE_TEST_CASE_MESSAGE = {'message': 'Test case successfully updated'}

# Test data for test case 10
# Check get data for test-case
GET_TEST_CASE_DATA = {'test_case': {
    'description': TEST_CASE_DESCRIPTION_UPD,
    'id': '1', 'suiteID': SUITE_ID,
    'title': TEST_CASE_TITLE}
}

# Test data for test case 11
# Check deleting test-case
TEST_CASE_DEL_MESSAGE = {'message': 'Test case successfully deleted'}
TEST_CASE_DEL_GET_MESSAGE = {'message': "Test case doesn't exist"}

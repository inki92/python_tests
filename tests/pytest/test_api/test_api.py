import pytest
import requests
import common.data as test_data


def test_api_response(docker_compose_fixture):
    """
    TEST CASE 1. Check if the application API is available.

    Basic test for check availability status of the application API.
    Get init message from the app.
    TEST DATA:
    INIT_MESSAGE - message from app API about OK status.
    """
    output = requests.get("http://127.0.0.1:5000/api/v1").json()
    assert test_data.INIT_MESSAGE == output


# Parametrize fixture to do 2 and 3 test cases with same test.
@pytest.mark.parametrize("user,password,expected_result", [(
            test_data.TRUE_LOGIN_NAME,
            test_data.TRUE_LOGIN_PASS,
            test_data.LOGIN_MESSAGE
    ), (
            test_data.WRONG_LOGIN_NAME,
            test_data.WRONG_LOGIN_PASS,
            test_data.LOGIN_MESSAGE_NEGATIVE
    )
    ])
def test_login(docker_compose_fixture, user, password, expected_result):
    """
     TEST CASE 2, 3. Check login to the server.

     2. Login to the server and receive access token.
     3. Negative. Login to the server with bad credentials attempt.
     TEST DATA:
    For positive scenario:
        TRUE_LOGIN_NAME, TRUE_LOGIN_PASS - existed credentials,
        LOGIN_MESSAGE - message with access token.
    For negative scenario:
        WRONG_LOGIN_NAME, WRONG_LOGIN_PASS - not existed credentials,
        LOGIN_MESSAGE_NEGATIVE - no such username or password message.

     """
    output = requests.post('http://127.0.0.1:5000/api/v1/login',
                           json={'username': user,
                                 'password': password}).json()
    assert expected_result in str(output)


# Parametrize fixture to do 4 and 6 test cases with same test.
@pytest.mark.parametrize(
    "add_test_suite_data, expected_result, expected_result_code", [(
            test_data.ADD_TEST_SUITE_DATA,
            test_data.ADD_TEST_SUITE_MESSAGE,
            test_data.SUCCESS_CODE
    ), (
            test_data.ADD_TEST_SUITE_DATA_NEGATIVE,
            test_data.ADD_TEST_SUITE_MESSAGE_NEGATIVE,
            test_data.BAD_REQ_BODY_CODE
    )
    ])
def test_add_test_suite(
        app_login_fixture, add_test_suite_data,
        expected_result, expected_result_code):
    """
    TEST CASE 4, 6. Check adding test suite.

    4. Create new test suite.
    6. Negative. Add test suite attempt without 'title' value.
    TEST DATA:
    For positive scenario:
        ADD_TEST_SUITE_DATA - correct data for creation test suite,
        ADD_TEST_SUITE_MESSAGE - message about successful creation,
        SUCCESS_CODE - status code of successful creation.
    For negative scenario:
        ADD_TEST_SUITE_DATA_NEGATIVE - incorrect data for creation test suite,
        ADD_TEST_SUITE_MESSAGE_NEGATIVE - message about bad data for creation,
        BAD_REQ_BODY_CODE - error status code.
    """
    headers = app_login_fixture
    output = requests.post(
        "http://127.0.0.1:5000/api/v1/test_suites",
        headers=headers, json=add_test_suite_data)
    print(add_test_suite_data)
    assert expected_result_code == output.status_code
    assert expected_result in str(output.json())


def test_show_test_suites(app_login_fixture):
    """
    TEST CASE 5. Check showing existed test suites.

    Get all existed test suites.
    TEST DATA:
    EXISTED_TEST_CASES - message with test suite from test case 4.
    """
    headers = app_login_fixture
    output = requests.get("http://127.0.0.1:5000/api/v1/test_suites",
                          headers=headers).json()
    assert test_data.EXISTED_TEST_CASES == output


# Parametrize fixture to do 7 and 8 test cases with same test.
@pytest.mark.parametrize("suite_id, title, description, expected_result", [(
            test_data.SUITE_ID,
            test_data.TEST_CASE_TITLE,
            test_data.TEST_CASE_DESCRIPTION,
            test_data.ADD_TEST_CASE_MESSAGE
    ), (
            test_data.WRONG_SUITE_ID,
            test_data.WRONG_CASE_TITLE,
            test_data.WRONG_CASE_DESCRIPTION,
            test_data.ADD_TEST_CASE_MESSAGE_NEGATIVE
    )
    ])
def test_add_test_case(
        app_login_fixture, suite_id, title, description, expected_result
):
    """
    TEST CASE 7, 8. Check adding new test-case.

    7. Create new test-case.
    8. Negative. Add new test-case to nonexistent test-suite attempt.
    TEST DATA:
    For positive scenario:
        SUITE_ID, TEST_CASE_TITLE,
        TEST_CASE_DESCRIPTION - correct data for adding test case,
        ADD_TEST_CASE_MESSAGE - message about successful adding.
    For negative scenario:
        WRONG_SUITE_ID, WRONG_CASE_TITLE,
        WRONG_CASE_DESCRIPTION - incorrect data for adding test case,
        ADD_TEST_CASE_MESSAGE_NEGATIVE - error message about adding process.
    """
    headers = app_login_fixture
    output = requests.post("http://127.0.0.1:5000/api/v1/test_cases",
                           headers=headers,
                           json={"suiteID": suite_id, "title": title,
                                 "description": description}).json()
    assert expected_result == output


def test_update_test_case(app_login_fixture):
    """
    TEST CASE 9. Check updating data for test-case.

    Update data('description') for existed test-case.
    TEST DATA:
        SUITE_ID - existed suite id,
        TEST_CASE_TITLE - test case title from test case 7,
        TEST_CASE_DESCRIPTION_UPD - update test case description,
        UPDATE_TEST_CASE_MESSAGE - test case info with updated description.
    """
    headers = app_login_fixture
    output = requests.put(
        "http://127.0.0.1:5000/api/v1/test_cases/1",
        headers=headers,
        json={"suiteID": test_data.SUITE_ID,
              "title": test_data.TEST_CASE_TITLE,
              "description": test_data.TEST_CASE_DESCRIPTION_UPD}).json()
    assert test_data.UPDATE_TEST_CASE_MESSAGE == output


def test_get_test_case_data(app_login_fixture):
    """
      TEST CASE 10. Check get data for test-case.

      Get data for existed test-case.
      TEST DATA:
          GET_TEST_CASE_DATA - message with data of existed test case.
    """
    headers = app_login_fixture
    output = requests.get("http://127.0.0.1:5000/api/v1/test_cases/1",
                          headers=headers).json()
    assert test_data.GET_TEST_CASE_DATA == output


def test_delete_test_case(app_login_fixture):
    """
      TEST CASE 11. Check deleting test-case.

      Delete test-case.
      TEST DATA:
          TEST_CASE_DEL_MESSAGE - message about successful deletion,
          TEST_CASE_DEL_GET_MESSAGE - message about absent test case.
      """
    headers = app_login_fixture
    output_del = requests.delete("http://127.0.0.1:5000/api/v1/test_cases/1",
                                 headers=headers).json()
    output_get = requests.get("http://127.0.0.1:5000/api/v1/test_cases/1",
                              headers=headers).json()
    assert test_data.TEST_CASE_DEL_MESSAGE == output_del
    assert test_data.TEST_CASE_DEL_GET_MESSAGE == output_get

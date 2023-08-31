*** Settings ***
Documentation    Test suite for testing REST API
Library    RequestsLibrary
Resource   ../keywords/api_keywords.robot
Variables   ../data/variables.py
Suite Setup    Start Container
Suite Teardown    Stop Container
Test Setup    Log To Console    ${TEST NAME} started
Test Teardown    Log To Console    ${TEST NAME} finished

*** Keywords ***
Login Test Template
    [Documentation]    Template for test cases 2, 3
    [Arguments]    ${user}    ${password}    ${expected_result}
    # URL for login request
    ${r_url}=    Set Variable    ${API_URL}login
    # json data for login request
    ${r_json}=    Create Dictionary    username=${user}    password=${password}
    ${output}=  Run Keyword And Return  Run Keyword And Ignore Error    POST    url=${r_url}  json=${r_json}
    Should Contain    ${output.json()}    ${expected_result}

Add Test Suite Template
    [Documentation]    Template for test cases 4,6
    [Arguments]    ${add_test_suite_data}    ${expected_result_code}    ${expected_result}
    # URL for add test suite request
    ${r_url}=    Set Variable    ${API_URL}test_suites
    # json data for add test suite request
    ${r_json}=    Set Variable    ${add_test_suite_data}
    ${output}=    Run Keyword And Return  Run Keyword And Ignore Error    POST    url=${r_url}  headers=${HEADERS}  json=${r_json}
    Should Be Equal As Strings    ${expected_result_code}    ${output.status_code}
    Should Contain    ${expected_result}    ${output.json()}

Add Test Case Template
    [Documentation]    Template for test cases 7, 8
    [Arguments]    ${suite_id}    ${title}    ${description}    ${expected_result}
    # URL for add test case request
    ${r_url}=    Set Variable    ${API_URL}test_cases
    # json data for add test case request
    ${r_json}=    Create Dictionary     suiteID=${suite_id}    title=${title}    description=${description}
    ${output}=  Run Keyword And Return  Run Keyword And Ignore Error    POST    url=${r_url}  headers=${HEADERS}  json=${r_json}
    Should Be Equal As Strings    ${expected_result}  ${output.json()}


*** Test Cases ***
API Response
    [Documentation]    TEST CASE 1. Check if the application API is available.
    ...    Basic test for check availability status of the application API.
    ...    Get init message from the app.
    ...    TEST DATA:
    ...        INIT_MESSAGE - message from app API about OK status,
    ...        API_URL      - url for API of application.
    [Tags]    test_case_1
    ${response}=    GET    url=${API_URL}
    Should Be Equal As Strings    ${INIT_MESSAGE}    ${response.json()}

Login
    [Template]    Login Test Template
    [Documentation]    TEST CASE 2, 3. Check login to the server.
    ...    2. Login to the server and receive access token.
    ...    3. Negative. Login to the server with bad credentials attempt.
    ...    TEST DATA:
    ...    General:
    ...        API_URL - url for API of application.
    ...    For positive scenario:
    ...        TRUE_LOGIN_NAME, TRUE_LOGIN_PASS - existed credentials,
    ...        LOGIN_MESSAGE - message with access token.
    ...    For negative scenario:
    ...        WRONG_LOGIN_NAME, WRONG_LOGIN_PASS - not existed credentials,
    ...        LOGIN_MESSAGE_NEGATIVE - no such username or password message.
    [Tags]    test_case_2_3
    ${TRUE_LOGIN_NAME}    ${TRUE_LOGIN_PASS}    ${LOGIN_MESSAGE}
    ${WRONG_LOGIN_NAME}    ${WRONG_LOGIN_PASS}    ${LOGIN_MESSAGE_NEGATIVE}

Add Test Suite
    [Template]    Add Test Suite Template
    [Documentation]    TEST CASE 4, 6. Check adding test suite.
    ...    4. Create new test suite.
    ...    6. Negative. Add test suite attempt without 'title' value.
    ...    TEST DATA:
    ...    General:
    ...        API_URL - url for API of application.
    ...    For positive scenario:
    ...        ADD_TEST_SUITE_DATA - correct data for creation test suite,
    ...        ADD_TEST_SUITE_MESSAGE - message about successful creation,
    ...        SUCCESS_CODE - status code of successful creation.
    ...    For negative scenario:
    ...        ADD_TEST_SUITE_DATA_NEGATIVE - incorrect data for creation suite,
    ...        ADD_TEST_SUITE_MESSAGE_NEGATIVE - message about bad data,
    ...        BAD_REQ_BODY_CODE - error status code.
    [Tags]    test_case_4_6
    ${ADD_TEST_SUITE_DATA}    ${SUCCESS_CODE}    ${ADD_TEST_SUITE_MESSAGE}
    ${ADD_TEST_SUITE_DATA_NEGATIVE}    ${BAD_REQ_BODY_CODE}    ${ADD_TEST_SUITE_MESSAGE_NEGATIVE}

Show Test Suites
    [Documentation]    TEST CASE 5. Check showing existed test suites.
    ...    Get all existed test suites.
    ...    TEST DATA:
    ...        API_URL            - url for API of application.
    ...        EXISTED_TEST_CASES - message with test suite from test case 4.
    [Tags]    test_case_5
    # URL for show test suites request
    ${r_url}=    Set Variable    ${API_URL}test_suites
    ${output}=    GET    url=${r_url}  headers=${HEADERS}
    Should Be Equal    ${EXISTED_TEST_CASES}    ${output.json()}

Add Test Case
    [Template]    Add Test Case Template
    [Documentation]    TEST CASE 7, 8. Check adding new test-case.
    ...    7. Create new test-case.
    ...    8. Negative. Add new test-case to nonexistent test-suite attempt.
    ...    TEST DATA:
    ...    General:
    ...        API_URL - url for API of application.
    ...    For positive scenario:
    ...        SUITE_ID, TEST_CASE_TITLE,
    ...        TEST_CASE_DESCRIPTION - correct data for adding test case,
    ...        ADD_TEST_CASE_MESSAGE - message about successful adding.
    ...    For negative scenario:
    ...        WRONG_SUITE_ID, WRONG_CASE_TITLE,
    ...        WRONG_CASE_DESCRIPTION - incorrect data for adding test case,
    ...        ADD_TEST_CASE_MESSAGE_NEGATIVE - error message about adding.
    [Tags]    test_case_7_8
    ${SUITE_ID}    ${TEST_CASE_TITLE}    ${TEST_CASE_DESCRIPTION}    ${ADD_TEST_CASE_MESSAGE}
    ${WRONG_SUITE_ID}    ${WRONG_CASE_TITLE}    ${WRONG_CASE_DESCRIPTION}    $(ADD_TEST_CASE_MESSAGE_NEGATIVE)

Update Test Case
    [Documentation]    TEST CASE 9. Check updating data for test-case.
    ...    Update data('description') for existed test-case.
    ...    TEST DATA:
    ...        API_URL                   - url for API of application.
    ...        SUITE_ID                  - existed suite id,
    ...        TEST_CASE_TITLE           - test case title from test case 7,
    ...        TEST_CASE_DESCRIPTION_UPD - update test case description,
    ...        UPDATE_TEST_CASE_MESSAGE  - testcase info with updated description.
    [Tags]    test_case_9
    # URL for update test case request
    ${r_url}=    Set Variable    ${API_URL}test_cases/1
    # json data for update test case request
    ${r_json}=    Create Dictionary    suiteID=${SUITE_ID}  title=${TEST_CASE_TITlE}  description=${TEST_CASE_DESCRIPTION_UPD}
    ${output}=    PUT    url=${r_url}  headers=${HEADERS}  json=${r_json}
    Should Be Equal    ${UPDATE_TEST_CASE_MESSAGE}    ${output.json()}

Get Test Case Data
    [Documentation]    TEST CASE 10. Check get data for test-case.
    ...    Get data for existed test-case.
    ...    TEST DATA:
    ...        API_URL            - url for API of application.
    ...        GET_TEST_CASE_DATA - message with data of existed test case.
    [Tags]    test_case_10
    # URL for get test case request
    ${r_url}=    Set Variable    ${API_URL}test_cases/1
    ${output}=    GET    url=${r_url}  headers=${HEADERS}
    Should Be Equal    ${GET_TEST_CASE_DATA}    ${output.json()}

Delete Test Case
    [Documentation]    TEST CASE 11. Check deleting test-case.
    ...    Delete test-case.
    ...    TEST DATA:
    ...        API_URL                   - url for API of application.
    ...        TEST_CASE_DEL_MESSAGE     - message about successful deletion,
    [Tags]    test_case_11
    # URL for delete test case request
    ${r_url}=    Set Variable    ${API_URL}test_cases/1
    ${output_del}=    DELETE    url=${r_url}  headers=${HEADERS}
    # Check GET request status to deleted test case. Should be 404.
    ${output_get}=    GET    url=${r_url}  headers=${HEADERS}    expected_status=404
    # Check response about successful deleting.
    Should Be Equal    ${TEST_CASE_DEL_MESSAGE}    ${output_del.json()}

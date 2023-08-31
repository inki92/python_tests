*** Settings ***
Documentation    This resource file contains keywords related to
...              API testing

Library    Process
Library     RequestsLibrary
Variables   ../data/variables.py

*** Variables ***
${CONNECTION_TRY}=  0
${CONNECTION_LIMIT}=  60

*** Keywords ***
Start Container
    [Documentation]    Start the Docker container for the REST app
    [Tags]    start_container
    Log    Starting REST API container
    TRY
        Run Process    /usr/local/bin/docker-compose    up    -d    stdout=PIPE    stderr=PIPE
        Log    Container successfully started
    EXCEPT
        Log to console   Container run process failed
    END
    Wait Until Keyword Succeeds    ${CONNECTION_LIMIT}x    1s    API Request Should Succeed
    Get Headers

Get headers
    [Documentation]    Get access token and return headers for login
    [Tags]    get_headers
    Log    Try to get access token
    ${json}=    Create Dictionary    username=${TRUE_LOGIN_NAME}    password=${TRUE_LOGIN_PASS}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${response}=    POST    url=${API_URL}login    json=${json}    headers=${headers}
    ${access_token}=    Set Variable    Bearer ${response.json()['access_token']}
    Log    Access token successfully received.
    ${headers}=    Create Dictionary    Authorization=${access_token}
    Set Global Variable    ${HEADERS}    ${headers}
    [Return]    ${HEADERS}

API Request Should Succeed
    [Documentation]    Get request to API
    [Tags]    get_to_api
    ${response}=    GET    url=${API_URL}
    Should Be Equal As Strings    ${SUCCESS_CODE}    ${response.status_code}

Stop Container
    [Documentation]    Stop the Docker container for the REST app
    Run Process    /usr/local/bin/docker-compose   down    shell=True
    Log    REST API container is down

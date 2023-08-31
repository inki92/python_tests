"""This module provides fixtures for testing the REST test application."""
import pytest
import subprocess
import requests
import time
import common.data as test_data


@pytest.fixture(scope='session', autouse=False)
def docker_compose_fixture():
    """Fixture to start and stop the Docker container for the test REST app."""
    response_code = ''
    connection_try: int = 0
    connection_limit = 60
    try:
        subprocess.run(
            ['/usr/local/bin/docker-compose', 'up', '-d'],
            check=True
        )
        while response_code != test_data.SUCCESS_CODE:
            try:
                response_code = requests.get(
                    "http://127.0.0.1:5000/api/v1"
                ).status_code
            except requests.exceptions.RequestException as e:
                if connection_try >= connection_limit:
                    # Raise an exception if the connection limit is reached
                    raise e
                    break
                connection_try += 1
                time.sleep(1)
        print('Docker container with rest app has been started successfully.')
        # Yield to the test function
        yield
    finally:
        # Stop the Docker container
        subprocess.run(
            ['/usr/local/bin/docker-compose', 'down'],
            check=True
        )
        print('Docker container with REST app has been stopped.')


@pytest.fixture(scope='session', autouse=True)
def app_login_fixture(docker_compose_fixture):
    """Fixture to log in to the REST test app and get an access token."""
    try:
        # Log in and get an access token
        token = requests.post(
            'http://127.0.0.1:5000/api/v1/login',
            json={'username': test_data.TRUE_LOGIN_NAME,
                  'password': test_data.TRUE_LOGIN_PASS}
        ).json()
        headers = {'Authorization': f"Bearer {token['access_token']}"}
        print('Authorization token successfully created.')
        # Yield the headers to the test function
        yield headers
    finally:
        # Delete the headers after the test function is finished
        del headers
        print('Authorization token successfully deleted.')

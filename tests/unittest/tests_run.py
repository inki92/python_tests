"""Function for run all tests with reporting."""
import unittest
import os
from datetime import datetime
import tests.unittest.runner.runner as runner
from tests.unittest.logger.logger import logger as logger
import tests.unittest.test_api.test_api
import tests.unittest.test_api.test_api_mock

# Test suites:
suites = tests.unittest.test_api.test_api.APITest,\
    tests.unittest.test_api.test_api_mock.APITestMock
# Format for report - 'html', 'xml' or 'text'
report_format = ''
# Path to directory with reports
reports_directory = "tests/reports/"


def start_tests(test_suites, test_report_format):
    """
    Start tests and choose report format.

    Description:
        start runner with one of chosen formats of reporting:
        html:   for html report,
        xml:    for xml report,
        text:   for detailed report to stdout
        empty:  no report
    """
    logger.info('Runner start')
    suite = unittest.TestSuite()
    # Add test suites to unittest runner
    for test_suite in test_suites:
        suite.addTest(unittest.makeSuite(test_suite))
    # Check directory for reports exists and create it, if not
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory)
    if test_report_format == 'html':
        runner.runner_html(suite, reports_directory)
    elif test_report_format == 'xml':
        runner.runner_xml(suite, reports_directory)
    elif test_report_format == 'text':
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        unittest.TextTestRunner().run(suite)


# Start tests
start_tests(suites, report_format)

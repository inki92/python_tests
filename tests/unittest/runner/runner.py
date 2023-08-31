"""Test runners for application."""
import HtmlTestRunner
import xmlrunner
from tests.unittest.logger.logger import logger as logger
import os


def runner_html(suite, reports_directory):
    """Test runner with reporting in html file."""
    # Get absolute path for reports directory.
    reports_path = os.path.abspath(reports_directory)
    logger.info(f"Report file path: {reports_path}")
    runner = HtmlTestRunner.HTMLTestRunner(output=reports_path)
    runner.run(suite)
    logger.info(f"Report saved to {reports_path}")


def runner_xml(suite, reports_directory):
    """Test runner with reporting to xml file."""
    # Get absolute path for report file
    reports_path = os.path.abspath(reports_directory)
    logger.info(f"Report file path: {reports_path}")
    runner = xmlrunner.XMLTestRunner(output=reports_path)
    runner.run(suite)
    logger.info(f"Report saved to {reports_path}")

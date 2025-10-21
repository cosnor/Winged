"""
Test runner configuration for users service tests
"""
import pytest
import sys
import os

# Add the app directory to Python path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_all_tests():
    """Run all tests in the test directory"""
    test_args = [
        "-v",  # verbose output
        "--tb=short",  # shorter traceback format
        "--strict-markers",  # require markers to be defined
        os.path.dirname(__file__)  # run tests in this directory
    ]
    
    return pytest.main(test_args)

def run_specific_test(test_file):
    """Run a specific test file"""
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    test_args = [
        "-v",
        "--tb=short",
        test_path
    ]
    
    return pytest.main(test_args)

def run_with_coverage():
    """Run tests with coverage report"""
    test_args = [
        "-v",
        "--tb=short",
        "--cov=../",  # coverage for parent app directory
        "--cov-report=term-missing",  # show missing lines
        "--cov-report=html:coverage_html",  # generate HTML report
        os.path.dirname(__file__)
    ]
    
    return pytest.main(test_args)

if __name__ == "__main__":
    # Default: run all tests
    exit_code = run_all_tests()
    sys.exit(exit_code)
import pytest

from conda_utils.cli import env_to_yaml, main

__author__ = "t-silvers"
__copyright__ = "t-silvers"
__license__ = "MIT"


def test_env_to_yaml():
    """API Tests"""
    with pytest.raises(AssertionError):
        env_to_yaml()


def test_main():
    """CLI Tests"""
    pass
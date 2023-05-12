import pytest

from conda_utils.cli import env_to_yaml, main

__author__ = "t-silvers"
__copyright__ = "t-silvers"
__license__ = "MIT"


def test_env_to_yaml():
    """API Tests"""
    with pytest.raises(AssertionError):
        env_to_yaml()


# def test_main(capsys):
def test_main():
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    # main(["7"])
    # captured = capsys.readouterr()
    # assert "The 7-th Fibonacci number is 13" in captured.out
    pass
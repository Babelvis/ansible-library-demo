"""Test module for DemoApi."""

import unittest
from demoapi import DemoApi

class TestApi(unittest.TestCase):
    """Test Class"""

    def setUp(self):
        self.demo_api = DemoApi('user', 'password', None, 'http://localhost:5041/')
        # clear all characters (if any)
        characters = self.demo_api.list()
        for character in characters:
            self.demo_api.reset(character)

    def test_username(self) -> None:
        """Test module with username/password

        yes i know, only test 1 thing every test...
        """
        characters = self.demo_api.list()
        for character in characters:
            self.demo_api.reset(character)
        # set A and B
        self.demo_api.set('A', 5)
        self.demo_api.set('B', 7)
        # check value of A
        check = self.demo_api.get('A')
        assert check == 5
        # check list
        check = self.demo_api.list()
        assert len(check) == 2
        assert 'A' in check
        assert 'B' in check

    def test_token(self) -> None:
        """Test module with token."""
        self.demo_api = DemoApi(None, None, 'secret', 'http://localhost:5041/')
        # set A and B
        self.demo_api.set('A', 5)
        # check value of A
        check = self.demo_api.get('A')
        assert check == 5

if __name__ == '__main_':
    unittest.main()

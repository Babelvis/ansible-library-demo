import unittest
from demoapi import DemoApi

class Test_Api(unittest.TestCase):

    def setUp(self):
        self.demoApi = DemoApi('user', 'password', None, 'http://localhost:5041/')
        # clear all characters (if any)
        characters = self.demoApi.list()
        for character in characters:
            self.demoApi.reset(character)
    
    # yes i know, only test 1 thing every test...
    def test_username(self):
        characters = self.demoApi.list()
        for character in characters:
            self.demoApi.reset(character)
        # set A and B
        self.demoApi.set('A', 5)
        self.demoApi.set('B', 7)
        # check value of A
        check = self.demoApi.get('A')
        assert check == 5
        # check list
        check = self.demoApi.list()
        assert len(check) == 2
        assert 'A' in check
        assert 'B' in check

    # test token
    def test_token(self):
        self.demoApi = DemoApi(None, None, 'secret', 'http://localhost:5041/')
        # set A and B
        self.demoApi.set('A', 5)
        # check value of A
        check = self.demoApi.get('A')
        assert check == 5

if __name__ == '__main_':
    unittest.main()

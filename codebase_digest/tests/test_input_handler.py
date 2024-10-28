import unittest
from unittest.mock import patch
from input_handler import InputHandler

class TestInputHandler(unittest.TestCase):

    def test_get_regular_input(self):
        handler = InputHandler(no_input=False)
        with patch('builtins.input', return_value='Yes'):
            self.assertEqual(handler.get_input('Enter something: '), 'yes')

    def test_surpassed_input_should_return_assigned_detault(self):
        handler = InputHandler(no_input=True, default_response='n')
        self.assertEqual(handler.get_input('Enter something: '), 'n')

    def test_surpassed_input_should_return_yes_by_default(self):
        handler = InputHandler(no_input=True)
        self.assertEqual(handler.get_input('Enter something: '), 'y')

if __name__ == '__main__':
    unittest.main()
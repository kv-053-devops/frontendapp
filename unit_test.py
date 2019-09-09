"""
Cover your basics task functions with unit tests.
"""
import unittest

from server_flask import app, receive_data_for_table, receive_data_for_charts, receive_symbol_list_from_settings_db


class TestFrontend(unittest.TestCase):

    def test_receive_data_for_table(self):
        test_list = receive_data_for_table( None )
        self.assertNotEqual(test_list, [] )

    def test_receive_data_for_charts(self):
        test_list = receive_data_for_charts( None )
        self.assertNotEqual(test_list, [] )

    # def test_exception_receive_symbol_list_from_settings_db(self):
    #     # receive_symbol_list_from_settings_db()
    #     self.assertRaises(Exception, receive_symbol_list_from_settings_db)


if __name__ == '__main__':
    unittest.main()

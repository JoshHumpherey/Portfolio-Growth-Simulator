"""
unittest: default library for unit testing
patch: used for object oriented testing
investment_growth: the base file to test
"""
import unittest
from unittest.mock import patch
import investment_growth

class InvestmentGrowthTests(unittest.TestCase):
    """ Unit tests for investment_growth.py """
    def test_get_quartile_data(self):
        """ This tests to make sure that the quartiles are divded correctly. """
        number_of_simulations = 100
        expected_lower = 25
        expected_middle = 50
        expected_upper = 75
        test_quartile_object = investment_growth.get_quartile_data(number_of_simulations)
        self.assertEqual(expected_lower, test_quartile_object.lower)
        self.assertEqual(expected_middle, test_quartile_object.middle)
        self.assertEqual(expected_upper, test_quartile_object.upper)

    @patch('investment_growth.yearly_data')
    def test_update_balance(self, mock_yearly_data):
        """ Test to make sure the investor balance updates correctly. """
        yearly_data = mock_yearly_data
        yearly_data.stock_return = 0.1
        yearly_data.bond_return = 0.1
        yearly_data.stock_percentage = 0.8
        iteration_balance = 90
        contribution = 10
        expected_result = 110
        test_balance = investment_growth.update_balance(iteration_balance,
                                                        contribution, yearly_data)
        self.assertEqual(test_balance, expected_result)

    def test_create_matrix(self):
        """ Tests to make sure matrices are correctly created. """
        test_matrix = investment_growth.create_matrix(5, 2)
        self.assertEqual(0, test_matrix[1][4])
        with self.assertRaises(Exception):
            test_matrix[2][5]

if __name__ == '__main__':
    unittest.main()

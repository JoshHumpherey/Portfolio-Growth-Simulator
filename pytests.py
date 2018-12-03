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
        LOWER = 0
        MID = 1
        UPPER = 2
        number_of_simulations = 100
        expected_lower = 25
        expected_middle = 50
        expected_upper = 75
        quartile_tuple = investment_growth.get_quartile_data(number_of_simulations)
        self.assertEqual(expected_lower, quartile_tuple[LOWER])
        self.assertEqual(expected_middle, quartile_tuple[MID])
        self.assertEqual(expected_upper, quartile_tuple[UPPER])

    def test_update_balance(self):
        """ Test to make sure the investor balance updates correctly. """
        current_year_tuple = (0.1, 0.1, 0.8)
        iteration_balance = 90
        contribution = 10
        expected_result = 110
        test_balance = investment_growth.update_balance(iteration_balance, contribution, current_year_tuple)
        self.assertEqual(test_balance, expected_result)

    def test_create_matrix(self):
        """ Tests to make sure matrices are correctly created. """
        test_matrix = investment_growth.create_matrix(5, 2)
        self.assertEqual(0, test_matrix[1][4])
        with self.assertRaises(Exception):
            test_matrix[2][5]

if __name__ == '__main__':
    unittest.main()

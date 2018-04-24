import unittest
from unittest.mock import patch,Mock
import InvestmentGrowth

class InvestmentGrowthTests(unittest.TestCase):

    def test_GetQuartileData(self):
        numberOfSimulations = 100
        expectedLower = 25
        expectedMiddle = 50
        expectedUpper = 75
        testQuartileObject = InvestmentGrowth.GetQuartileData(numberOfSimulations)
        self.assertEqual(expectedLower, testQuartileObject.lower)
        self.assertEqual(expectedMiddle, testQuartileObject.middle)
        self.assertEqual(expectedUpper, testQuartileObject.upper)

    @patch('InvestmentGrowth.yearlyData')
    def test_UpdateBalance(self,mockYearlyData):
        yearlyData = mockYearlyData
        yearlyData.stockReturn = 0.1
        yearlyData.bondReturn = 0.1
        yearlyData.stockPercentage = 0.8
        iterationBalance = 90
        contribution = 10
        expectedResult = 110
        testBalance = InvestmentGrowth.UpdateBalance(iterationBalance,contribution,yearlyData)
        self.assertEqual(testBalance,expectedResult)





if __name__ == '__main__':
    unittest.main()

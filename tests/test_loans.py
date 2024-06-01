from toolbox import Loan
from unittest import TestCase

class LoanOperationalTest(TestCase):

    def setUp(self):
        self.loan = Loan(0.07, 30, 500000)
        print('running setup')


    def test_attributes(self):
        print(self.loan)
    





from unittest import TestCase
import pandas as pd

from lib.loans import Loan, Expense, InvestmentProperty


class LoanOperationalTest(TestCase):

    def test_attributes(self):
        test_loan = Loan(0.07, 30, 500000)
        # Test payment amount.
        self.assertEqual(round(test_loan.pmt, 2), 3326.51)


    def test_table(self):
        test_loan = Loan(0.07, 30, 500000)
        
        # Test first entries in table
        interest = test_loan.loan_table().iloc[0, 1].item(0)
        principal = test_loan.loan_table().iloc[0, 2].item(0)
        balance = test_loan.loan_table().iloc[0, 3].item(0)

        self.assertEqual(round(interest, 2), 2916.67)
        self.assertEqual(round(principal, 2), 409.85)
        self.assertEqual(round(balance, 2), 499590.15)

        # Test last entries in table
        interest = test_loan.loan_table().iloc[-1, 1].item(0)
        principal = test_loan.loan_table().iloc[-1, 2].item(0)
        balance = test_loan.loan_table().iloc[-1, 3].item(0)

        self.assertEqual(round(interest, 2), 19.29)
        self.assertEqual(round(principal, 2), 3307.22)
        self.assertEqual(round(balance, 2), 0)

class ExpenseTest(TestCase):

    def test_attributes(self):
        e = Expense('test', 100, '2024-01-01', '2024-02-01', '2W')
        # test first entry in table index is start date
        self.assertEqual(str(e.table.index[1]), '2024-01-21 00:00:00')
        # test there are 2 rows
        self.assertEqual(len(e.table.index), 2)
    
    def test_single_expense(self):
        e = Expense('test', 100, '2024-01-01')
        # test the table only contains 1 row
        self.assertEqual(len(e.table.index), 1)

    def test_merge(self):
        e1 = Expense('e1', 100, '2024-01-01', '2024-02-01', '2W')
        e2 = Expense('e2', 200, '2024-01-01', '2024-02-01', '1W')
        merged = pd.concat([e1.table, e2.table])
        # test the tables can be merged successfully giving 6 rows
        self.assertEqual(len(merged.index), 6)

class InvestmentPropertyTest(TestCase):

    def test_expenses(self):
        expenses = [
            {
                'value': 100,
                'description': 'test1',
                'start_date': '2024-01-01',
                'end_date': '2024-02-01',
                'freq': '1W'
            },{
                'value': 200,
                'description': 'test2',
                'start_date': '2024-01-01'             
            }

        ]

        ip = InvestmentProperty('test_ip', Loan(0.07, 30, 500000, start='2024-01-01'), expenses)
        # test the expenses detailed table has the correct rows
        self.assertEqual(len(ip.expenses.index), 5)

    def test_model(self):
        expenses = [
            {
                'value': 100,
                'description': 'test1',
                'start_date': '2024-01-01',
                'end_date': '2034-02-01',
                'freq': '1W'
            },{
                'value': 200,
                'description': 'test2',
                'start_date': '2024-01-01'             
            }

        ]

        ip = InvestmentProperty('test_ip', Loan(0.07, 30, 500000, start='2024-01-01'), expenses)

        # test that all the columns are the correct names
        self.assertListEqual(ip.model.columns.values.tolist(), ['Payment', 'Interest', 'Principal', 'Balance', 'Expenses'])
        # test there are 360 rows in the model
        self.assertEqual(ip.model.shape[0], 360)
       
    def test_break_even(self):

        expenses = [
            {
                'value': 1,
                'description': 'test1',
                'start_date': '2024-01-01',
                'end_date': '2024-02-01',
                'freq': '1Y'
            }
        ]

        ip = InvestmentProperty('test_ip', Loan(0.07, 1, 100000, start='2024-01-01'), expenses)

        be = ip.break_even()

        print(f'By Year: {be["year"]}')
        print(f'By Month: {be["month"]}')
        print(f'By Week: {be["week"]}')

        # Leaving as failing because the Loan table is not working correctly
        self.assertEqual(True, False)


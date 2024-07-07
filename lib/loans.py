import datetime as dt
from dateutils import month_start, relativedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy_financial as npf
import pandas as pd


class Loan:
    """ 
    Models the costs and implications of a Loan 

    Attributes:
        pmt (int): Amount to be paid each period
        pmt_str (str): pmt with pretty string format
    """

    def __init__(self, rate, term, loan_amount, repayments_per_year=12, start=dt.date.today().isoformat()):
        self.rate = rate / repayments_per_year
        self.periods = term * repayments_per_year
        self.repayments_per_year = repayments_per_year
        self.loan_amount = loan_amount
        self.start = month_start(dt.date.fromisoformat(start) + dt.timedelta(31))
        self.pmt = npf.pmt(self.rate, self.periods, -self.loan_amount)
        self.pmt_str = f"${self.pmt:,.2f}"
        self.table = self.loan_table()

    def loan_table(self):

        if self.repayments_per_year == 12:
            periods = [self.start + relativedelta(months=x) for x in range(self.periods)]
        if self.repayments_per_year == 26:
            periods = [self.start + relativedelta(weeks=x*2) for x in range(self.periods)]
        interest = [npf.ipmt(self.rate, month, self.periods, -self.loan_amount)
                    for month in range(1, self.periods + 1)]
        principal = [npf.ppmt(self.rate, month, self.periods, -self.loan_amount)
                     for month in range(1, self.periods + 1)]
        table = pd.DataFrame({'Payment': self.pmt,
                              'Interest': interest,
                              'Principal': principal}, index=pd.to_datetime(periods))
        table['Balance'] = self.loan_amount - table['Principal'].cumsum()
        return table.round(2)

    def plot_balances(self):
        # amort = self.loan_table()
        # plt.plot(amort.Balance, label='Balance')
        # plt.plot(amort.Interest.cumsum(), label='Interest Paid')
        # plt.grid(axis='y', alpha=.5)
        # plt.legend(loc=8)
        # plt.show()

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(self.table.index, self.table['Payment'], label='Payment')
        ax.plot(self.table.index, self.table['Interest'], label='Interest')
        ax.plot(self.table.index, self.table['Principal'], label='Principal')
        ax.plot(self.table.index, self.table['Balance'], label='Balance')

        ax.set_yscale('log')
        ax.grid(True)
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

        ax.legend()

        plt.show()

    def summary(self):
        amort = self.table
        print(f"Summary {self.__class__.__name__}")
        print("-" * 30)
        print(f'Loan Amount: {self.loan_amount:>17,.2f}')
        print(f'Payment: {self.pmt_str:>21}')
        print(f'{"Payoff Date:":19s} {amort.index.date[-1]}')
        print(f'Interest Paid: {amort.Interest.cumsum()[-1]:>15,.2f}')


    def pay_early(self, extra_amt):
        return f'{round(npf.nper(self.rate, self.pmt + extra_amt, -self.loan_amount) / 12, 2)}'

    def retire_debt(self, years_to_debt_free):
        extra_pmt = 1
        while npf.nper(self.rate, self.pmt + extra_pmt, -self.loan_amount) / 12 > years_to_debt_free:
            extra_pmt += 1
        return extra_pmt, self.pmt + extra_pmt
    

class InvestmentLoan(Loan):
    def __init__(self, rate, term, loan_amount, property_value, repayments_per_year=12, start=dt.date.today().isoformat()):
        super().__init__(rate, term, loan_amount, repayments_per_year, start)
        self.property_value = property_value
        self.lvr = self.loan_amount / self.property_value

    def summary(self):
        super().summary()
        print(f'Loan Value Ratio: {self.lvr:>12.0%}')


class InvestmentProperty:

    def __init__(self, name: str, loan: Loan, expenses: list):
        self.name = name
        self.loan = loan
        self._model = pd.DataFrame()
        self._expenses = pd.DataFrame()
        self.expenses = expenses

    @property
    def expenses(self):
        return self._expenses
    
    @expenses.setter
    def expenses(self, expenses):
        """
        Creates a table of expenses
        [{
            'value': 100,
            'description': 'test',
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'freq': '1W'
        }]

        """

        table = pd.DataFrame()
        for expense in expenses:
            e = Expense(**expense)
            table = pd.concat([e.table, table])
        self._expenses = table

    @property
    def model(self):

        expenses_summary = self.expenses[['value']].groupby(pd.Grouper(freq='MS')).sum()
        self._model = self.loan.table.join(expenses_summary)
        self._model.rename(columns={'value': 'Expenses'}, inplace=True)
        return self._model
    
    def plot_model(self):

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(self.model.index, self.model['Payment'], label='Payment')
        ax.plot(self.model.index, self.model['Interest'], label='Interest')
        ax.plot(self.model.index, self.model['Principal'], label='Principal')
        ax.plot(self.model.index, self.model['Balance'], label='Balance')
        ax.plot(self.model.index, self.model['Expenses'], label='Expenses')

        ax.set_yscale('log')
        ax.grid(True)
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

        ax.legend()

        plt.show()


class Expense:
    """ 
    Represents an expense on the investment. Expenses can repeat at a set interval between a start and end date.

    Attributes:
        table (DataFrame): table with expense, date, value and description
    
    """
    def __init__(self, description, value, start_date, end_date='', freq=''):
        self.description = description
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        self.freq = freq

        if self.end_date == '' and self.freq == '':
            self.table = pd.DataFrame({'value': value, 'description': description}, 
                                      index=pd.DatetimeIndex([f'{self.start_date} 00:00:00']))
        else:
            date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
            self.table = pd.DataFrame({'value': value, 'description': description}, index=date_range)

    def __str__(self):
        return f'Description: {self.description}, Value: {self.value} Frequency: {self.freq}'

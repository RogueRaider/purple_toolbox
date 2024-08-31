# %%

%matplotlib ipympl
from lib.loans import Loan
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt



l = Loan(0.07, 30, 500000)
table = l.loan_table()


fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(table.index, table['Payment'], label='Payment')
ax.plot(table.index, table['Interest'], label='Interest')
ax.plot(table.index, table['Principal'], label='Principal')
ax.plot(table.index, table['Balance'], label='Balance')

ax.set_yscale('log')
ax.grid(True)
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
# ax.yticks([1000, 5000, 10000, 250000, 500000])
ax.legend()

plt.show()


# %%

%matplotlib ipympl

from lib.loans import InvestmentProperty
from lib.loans import Loan
from datetime import date 

l1 = Loan(0.07, 30, 500000, start='2024-01-01')

expenses = [
    {
        'value': 700,
        'description': 'Strata',
        'start_date': '2024-01-01',
        'end_date': '2054-02-01',
        'freq': 'QS'
    },{
        'value': 1000,
        'description': 'Insurance',
        'start_date': '2024-01-01',
        'end_date': '2054-02-01',
        'freq': 'YS'             
    },{
        'value': 100,
        'description': 'Maintenance',
        'start_date': '2024-01-01',
        'end_date': '2054-02-01',
        'freq': 'MS'           
    }
]

ip = InvestmentProperty("sample-01", l1, expenses)

ip.model.head(30)

ip.plot_model()



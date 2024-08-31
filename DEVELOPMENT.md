
## Classes

### Loan
Produces a financial model of a simple mortgage.

Attributes
* Interest
* Deposit
* Repayments
* Term
* pmt_str 

Arguments
* rate
* term
* loan_amount
* repayments_per_year=12
* start 

The loan table is summarized by month for simplicity.

### InvestmentProperty

Attributes
* Loan
* Expenses: table to hold all expenses
* Model Summary: table that shows Principle, Interest, Payment, Balance and Expenses parameters grouped by month
* Running Costs: table containing Loan interest and expenses
* Rental Break Even: rent income per month required to cover all costs

### Expense 

* Expected cost along with a re-occurance interval. EG $100 every month.

The expenses_summary shows all expenses grouped by month for simplicity.

### Rental Break Even

This value includes all expenses from the expenses attribute and the interest charged on the loan. 

This value will decrease over the life of the loan because the cost of interest goes down. To give an approximate value the first 4 years of the loan are used by default.

#### Resources

https://github.com/malcolmchetwyn/realestate_investment_app

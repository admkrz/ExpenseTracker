import operator
from datetime import date, timedelta

from dateutil import relativedelta

from expensetracker import db
from expensetracker.models import TransactionType, Category


# Sum of transactions amount from last month
def sum_month(transactions):
    today = date.today()
    monthly_transactions = [transaction for transaction in transactions if
                            (today.year - transaction.date.year) * 12 + (today.month - transaction.date.month) < 1]
    return sum([transaction.amount for transaction in monthly_transactions])


# Sum of transactions amount from last week
def sum_week(transactions):
    today = date.today()
    weekly_transactions = [transaction for transaction in transactions if
                           (today - transaction.date).days < 7]
    return sum([transaction.amount for transaction in weekly_transactions])


# Calculate balance from transactions before the specified date
def balance_before_date(transactions, date):
    expenses_before_date = sum([transaction.amount for transaction in transactions if
                                transaction.type == TransactionType.expense and transaction.date <= date])
    incomes_before_date = sum([transaction.amount for transaction in transactions if
                               transaction.type == TransactionType.income and transaction.date <= date])
    return float("{:.2f}".format(incomes_before_date - expenses_before_date))


# Calculate all budgets balances in time with all of its changes
def budget_days_data(budgets):
    transactions = []
    for budget in budgets:
        for transaction in budget.transactions.filter_by().all():
            transactions.append(transaction)
    sorted_transactions = sorted(transactions, key=operator.attrgetter('date'))
    budget_days_labels = [t.date for t in sorted_transactions]
    budget_days_data = []
    for day in budget_days_labels:
        budget_days_data.append(balance_before_date(sorted_transactions, day))
    return [item.strftime('%Y-%m-%d') for item in budget_days_labels], budget_days_data


# generate array with dates from month ago to today
def get_daily_labels():
    today = date.today()
    month_ago = date.today() - timedelta(days=30)
    labels = []
    while month_ago <= today:
        labels.append(month_ago)
        month_ago += timedelta(days=1)
    return labels


# generate daily labels with daily expenses and daily incomes for last month
def get_daily_transactions(budgets):
    daily_expenses = []
    daily_incomes = []
    transactions = []
    for budget in budgets:
        for transaction in budget.transactions.filter_by().all():
            transactions.append(transaction)
    sorted_transactions = sorted(transactions, key=operator.attrgetter('date'))
    labels = get_daily_labels()
    for day in labels:
        daily_expense = 0
        daily_income = 0
        while len(sorted_transactions) > 0 and sorted_transactions[0].date == day:
            if sorted_transactions[0].type == TransactionType.expense:
                daily_expense += sorted_transactions[0].amount
            else:
                daily_income += sorted_transactions[0].amount
            sorted_transactions.pop(0)
        daily_expenses.append(daily_expense)
        daily_incomes.append(daily_income)
    return [item.strftime('%Y-%m-%d') for item in labels], daily_expenses, daily_incomes


# generate array with dates from month ago to today
def get_monthly_labels():
    today = date.today()
    year_ago = date.today() - relativedelta.relativedelta(months=11)
    labels = []
    while year_ago <= today:
        labels.append((year_ago.strftime('%B'), year_ago.strftime('%m-%Y')))
        year_ago += relativedelta.relativedelta(months=1)
    return labels


# generate daily labels with daily expenses and daily incomes for last month
def get_monthly_transactions(budgets):
    monthly_expenses = []
    monthly_incomes = []
    transactions = []
    for budget in budgets:
        for transaction in budget.transactions.filter_by().all():
            transactions.append(transaction)
    sorted_transactions = sorted(transactions, key=operator.attrgetter('date'))
    labels = get_monthly_labels()
    month_labels = []
    for month in labels:
        month_labels.append(month[0])
        monthly_expense = 0
        monthly_income = 0
        while len(sorted_transactions) > 0 and sorted_transactions[0].date.strftime('%m-%Y') == month[1]:
            if sorted_transactions[0].type == TransactionType.expense:
                monthly_expense += sorted_transactions[0].amount
            else:
                monthly_income += sorted_transactions[0].amount
            sorted_transactions.pop(0)
        monthly_expenses.append(monthly_expense)
        monthly_incomes.append(monthly_income)
    return month_labels, monthly_expenses, monthly_incomes


# Divide transactions into categories and retrieve amount sums for categories chart
def get_categories_data(categories):
    expense_categories = [['Category', 'Sum']]
    expense_sum = 0
    income_categories = [['Category', 'Sum']]
    income_sum = 0

    for category in categories:
        if category.type == TransactionType.expense:
            category_sum = sum([t.amount for t in category.transactions.filter_by().all()])
            expense_sum += category_sum
            expense_categories.append([category.name, category_sum])
        else:
            category_sum = sum([t.amount for t in category.transactions.filter_by().all()])
            income_sum += category_sum
            income_categories.append([category.name, category_sum])

    return expense_categories, income_categories, expense_sum, income_sum


# Return transactions with date after given date
def get_transactions_after_date(budgets, date):
    transactions = [transaction for budget in budgets for transaction in budget.transactions.filter_by().all()]
    expenses_records = [transaction for transaction in transactions if
                        transaction.type == TransactionType.expense and transaction.date > date]
    incomes_records = [transaction for transaction in transactions if
                       transaction.type == TransactionType.income and transaction.date > date]
    return expenses_records, incomes_records


# Calculate current budget balance
def sum_balance(budget):
    incomes_sum = sum([income.amount for income in budget.transactions.filter_by(type='income').all()])
    expenses_sum = sum([expense.amount for expense in budget.transactions.filter_by(type='expense').all()])
    budget.balance = incomes_sum - expenses_sum
    db.session.commit()


# Check if there are any hidden and unused categories
def optimize_categories(type):
    categories = Category.query.filter_by(type=type.lower(), hidden=True).all()
    for category in categories:
        if len(category.transactions.filter_by().all()) == 0:
            db.session.delete(category)
            db.session.commit()

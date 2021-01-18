import operator
from datetime import date

from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from expensetracker.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm, ChangeCurrencyForm, \
    CreateCategoryForm, RenameForm, DeleteForm, CreateBudgetForm, TransactionForm
from expensetracker import app, db, bcrypt
from expensetracker.models import User, Category, Budget, Transaction, TransactionType

new_user_expense_categories = ["Groceries", "Housing", "Shopping", "Entertainment", "Travel", "Health", "Other"]
new_user_income_categories = ["Salary", "Bonus"]
new_user_budgets = ["Card Budget", "Cash Budget"]


def sum_monthly(transactions):
    today = date.today()
    monthly_transactions = [transaction for transaction in transactions if
                            (today.year - transaction.date.year) * 12 + (today.month - transaction.date.month) < 1]
    return sum([transaction.amount for transaction in monthly_transactions])


def sum_weekly(transactions):
    today = date.today()
    weekly_transactions = [transaction for transaction in transactions if
                           (today - transaction.date).days < 7]
    return sum([transaction.amount for transaction in weekly_transactions])


@app.route('/')
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        currency = user.currency
        budgets = []
        for budget in user.budgets.filter_by().all():
            budgets.append((budget, sum_monthly(budget.transactions.filter_by(type=TransactionType.expense).all()),
                            sum_monthly(budget.transactions.filter_by(type=TransactionType.income).all())))

        expenses = []
        incomes = []

        for budget in user.budgets.filter_by().all():
            for transaction in budget.transactions.filter_by().all():
                if transaction.type == TransactionType.expense:
                    expenses.append(transaction)
                else:
                    incomes.append(transaction)

        return render_template('index.html',
                               expenses=sorted(expenses, key=operator.attrgetter("date"), reverse=True)[0:5],
                               incomes=sorted(incomes, key=operator.attrgetter("date"), reverse=True)[0:5],
                               budgets=budgets, monthly_expenses=sum_monthly(expenses),
                               monthly_incomes=sum_monthly(incomes), weekly_expenses=sum_weekly(expenses),
                               weekly_incomes=sum_weekly(incomes), currency=currency)
    else:
        return redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(index))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_passwd, currency='USD')
        db.session.add(user)
        db.session.commit()

        for category_name in new_user_expense_categories:
            expense_category = Category(name=category_name, type=TransactionType.expense, user=user, hidden=False)
            db.session.add(expense_category)
            db.session.commit()

        for category_name in new_user_income_categories:
            income_category = Category(name=category_name, type=TransactionType.income, user=user, hidden=False)
            db.session.add(income_category)
            db.session.commit()

        for budget_name in new_user_budgets:
            budget = Budget(name=budget_name, user=user)
            db.session.add(budget)
            db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(index))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash('Successfully logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Incorrect password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    account_form = UpdateAccountForm()
    password_form = ChangePasswordForm()
    currency_form = ChangeCurrencyForm()

    if account_form.validate_on_submit():
        current_user.username = account_form.username.data
        current_user.email = account_form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        account_form.username.data = current_user.username
        account_form.email.data = current_user.email

    if password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, password_form.old_password.data):
            new_password = bcrypt.generate_password_hash(password_form.password.data).decode('utf-8')
            current_user.password = new_password
            db.session.commit()
            flash('Your password has been changed!', 'success')
        else:
            flash('Incorrect old password', 'danger')
        return redirect(url_for('account'))

    if currency_form.validate_on_submit():
        current_user.currency = currency_form.currency.data
        db.session.commit()
        flash('Your currency has been changed!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        currency_form.currency.data = current_user.currency

    return render_template('account.html', title='Account', account_form=account_form, password_form=password_form,
                           currency_form=currency_form)


@app.route('/expenses')
@login_required
def expenses():
    return render_template('expenses.html', title='Expenses')


@app.route('/incomes')
@login_required
def incomes():
    return render_template('incomes.html', title='Incomes')


@app.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expenses():
    value = request.args.get('value')
    return add_transaction('Expense', value)


@app.route('/incomes/add', methods=['GET', 'POST'])
@login_required
def add_incomes():
    value = request.args.get('value')
    return add_transaction('Income', value)


def sum_balance(budget):
    incomes_sum = sum(income.amount for income in budget.transactions.filter_by(type='income').all())
    expenses_sum = sum(expense.amount for expense in budget.transactions.filter_by(type='expense').all())
    budget.balance = incomes_sum - expenses_sum
    db.session.commit()


def optimize_categories(type):
    categories = Category.query.filter_by(type=type.lower(), hidden=True).all()
    for category in categories:
        if len(category.transactions.filter_by().all()) == 0:
            db.session.delete(category)
            db.session.commit()


def add_transaction(type, value):
    user = User.query.filter_by(username=current_user.username).first()
    currency = user.currency

    categories = []
    for category in user.categories.filter_by(type=type.lower(), hidden=False).all():
        categories.append((category.id, category.name))

    budgets = []
    for budget in user.budgets.filter_by().all():
        budgets.append((budget.id, budget.name))

    form = TransactionForm()
    form.budget.choices = budgets
    form.category.choices = categories

    if form.validate_on_submit():
        transaction = Transaction(budget_id=int(form.budget.data), description=form.description.data,
                                  date=form.date.data,
                                  amount=float(form.amount.data), category_id=int(form.category.data),
                                  type=type.lower())
        db.session.add(transaction)
        db.session.commit()
        sum_balance(transaction.budget)
        flash(f'{type} created!', 'success')
        if value == "quick":
            return redirect(url_for('index'))
        else:
            return redirect(url_for(f'add_{type.lower()}s'))

    return render_template('addtransaction.html', title=f'Add {type}', type=type, form=form, currency=currency)


@app.route('/expenses/history', methods=['GET', 'POST'])
@login_required
def expenses_history():
    return transactions_history('Expense')


@app.route('/incomes/history', methods=['GET', 'POST'])
@login_required
def incomes_history():
    return transactions_history('Income')


def transactions_history(type):
    user = User.query.filter_by(username=current_user.username).first()
    currency = user.currency

    categories = []
    for category in user.categories.filter_by(type=type.lower(), hidden=False).all():
        categories.append((category.id, category.name))

    budgets = []
    for budget in user.budgets.filter_by().all():
        budgets.append((budget.id, budget.name))

    edit_form = TransactionForm()
    edit_form.budget.choices = budgets
    edit_form.category.choices = categories
    delete_form = DeleteForm()

    budgets = user.budgets.filter_by().all()
    categories = user.categories.filter_by(type=type.lower()).all()

    if edit_form.validate_on_submit():
        modified_transaction = Transaction.query.filter_by(id=int(edit_form.id.data)).first()

        old_budget = modified_transaction.budget
        new_budget = Budget.query.filter_by(id=int(edit_form.budget.data)).first()

        modified_transaction.budget_id = int(edit_form.budget.data)
        modified_transaction.description = edit_form.description.data
        modified_transaction.category_id = int(edit_form.category.data)
        modified_transaction.date = edit_form.date.data
        modified_transaction.amount = edit_form.amount.data
        db.session.commit()
        flash('Transaction changes saved!', 'success')

        sum_balance(old_budget)
        sum_balance(new_budget)
        optimize_categories(type)

        return redirect(url_for(f'{type.lower()}s_history'))

    if delete_form.validate_on_submit():
        transaction_to_delete = Transaction.query.filter_by(id=int(delete_form.item_to_delete.data))
        old_budget = transaction_to_delete.budget

        transaction_to_delete.delete()
        db.session.commit()
        flash("Transaction deleted!", 'danger')

        sum_balance(old_budget)
        optimize_categories(type)

        return redirect(url_for(f'{type.lower()}s_history'))

    return render_template('transactionshistory.html', title=f'Manage {type}s', type=type, budgets=budgets,
                           categories=categories, edit_form=edit_form, delete_form=delete_form, currency=currency)


@app.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    budget_form = CreateBudgetForm()
    rename_form = RenameForm()
    delete_form = DeleteForm()
    user = User.query.filter_by(username=current_user.username).first()
    user_budgets = user.budgets
    budgets = user_budgets.filter_by().all()

    if budget_form.validate_on_submit():
        budget = user_budgets.filter_by(name=budget_form.name.data).first()
        if budget:
            flash('Budget with this name already exists!', 'danger')
        else:
            budget = Budget(name=budget_form.name.data, user=current_user)
            db.session.add(budget)
            db.session.commit()
            flash('Budget created!', 'success')
        return redirect(url_for('budgets'))

    if rename_form.validate_on_submit():
        old_budget = user_budgets.filter_by(name=rename_form.old_name.data).first()
        new_budget = user_budgets.filter_by(name=rename_form.new_name.data).first()
        if new_budget:
            flash('Budget with this name already exists!', 'danger')
        else:
            old_budget.name = rename_form.new_name.data
            db.session.commit()
            flash('Budget name changed!', 'success')
        return redirect(url_for('budgets'))

    if delete_form.validate_on_submit():
        budget = user_budgets.filter_by(id=int(delete_form.item_to_delete.data))
        budget_name = budget.first().name

        for transaction in budget.first().transactions.filter_by().all():
            db.session.delete(transaction)
            db.session.commit()

        budget.delete()
        db.session.commit()
        flash(f"Budget '{budget_name}' deleted!", 'danger')
        return redirect(url_for('budgets'))

    return render_template('budgets.html', title='Budgets', budgets=budgets, create_bugdet_form=budget_form,
                           rename_form=rename_form, delete_form=delete_form)


@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html', title='Categories')


@app.route('/categories/income', methods=['GET', 'POST'])
@login_required
def income_categories():
    return manage_categories(TransactionType.income, 'Income')


@app.route('/categories/expense', methods=['GET', 'POST'])
@login_required
def expense_categories():
    return manage_categories(TransactionType.expense, 'Expense')


def manage_categories(category_type, type_name):
    category_form = CreateCategoryForm()
    rename_form = RenameForm()
    delete_form = DeleteForm()
    user = User.query.filter_by(username=current_user.username).first()
    user_categories = user.categories
    categories = user_categories.filter_by(type=category_type, hidden=False).all()

    if category_form.validate_on_submit():
        category = user_categories.filter_by(name=category_form.category.data, type=category_type).first()
        if category and not category.hidden:
            flash('Category with this name already exists!', 'danger')
        elif category and category.hidden:
            category.hidden = False
            db.session.commit()
            flash(f'New {type_name} category created!', 'success')
        else:
            category = Category(name=category_form.category.data, type=category_type, user=current_user,
                                hidden=False)
            db.session.add(category)
            db.session.commit()
            flash(f'New {type_name} category created!', 'success')
        return redirect(url_for(f'{type_name.lower()}_categories'))

    if rename_form.validate_on_submit():
        category = user_categories.filter_by(name=rename_form.old_name.data, type=category_type,
                                             hidden=False).first()
        new_category = user_categories.filter_by(name=rename_form.new_name.data, type=category_type).first()
        if new_category and not new_category.hidden:
            flash('Category with this name already exists!', 'danger')
        elif new_category and new_category.hidden:
            for transaction in Transaction.query.filter_by(category_id=category.id).all():
                transaction.category_id = new_category.id
                db.session.commit()
            new_category.hidden = False
            user_categories.filter_by(name=rename_form.old_name.data, type=category_type,
                                      hidden=False).delete()
            db.session.commit()
        else:
            category.name = rename_form.new_name.data
            db.session.commit()
            flash(f'{type_name} category name changed!', 'success')
        return redirect(url_for(f'{type_name.lower()}_categories'))

    if delete_form.validate_on_submit():
        category = user_categories.filter_by(id=int(delete_form.item_to_delete.data)).first()
        category_name = category.name
        if category.transactions.filter_by().all():
            category.hidden = True
        else:
            db.session.delete(category)
        db.session.commit()
        flash(f"{type_name} category '{category_name}' deleted!", 'danger')
        return redirect(url_for(f'{type_name.lower()}_categories'))

    return render_template('managecategories.html', title=f'{type_name} Categories', category_form=category_form,
                           rename_form=rename_form, delete_form=delete_form, categories=categories,
                           category_type=type_name)


@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html', title='Reports')

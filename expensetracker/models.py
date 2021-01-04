import enum
from datetime import datetime

from flask_login import UserMixin

from expensetracker import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class CategoryType(enum.Enum):
    income = 'income'
    expense = 'expense'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    currency = db.Column(db.String(3))
    accounts = db.relationship('Account', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expenses = db.relationship('Expense', backref='account', lazy=True)
    incomes = db.relationship('Income', backref='account', lazy=True)

    def __repr__(self):
        return f"Account('{self.name}, {self.user})"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y-%m-%d'))
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Expense('{self.description}, {self.date}, {self.amount}')"


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y-%m-%d'))
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Income('{self.description}, {self.date}, {self.amount}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(CategoryType), nullable=False)
    hidden = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Category('{self.name}')"

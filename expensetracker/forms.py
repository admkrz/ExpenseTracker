from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import ccy

from expensetracker.models import User


def equalTo(password):
    def _equalTo(self, field):
        if field.data != self[password].data:
            flash('Both passwords must be identical', 'danger')
            raise ValidationError('Both passwords must be identical')

    return _equalTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(message="This must be a valid email adress")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password',
                                                                                             message="Both passwords must be identical")])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already assigned to an account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(message="This must be a valid email adress")])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already assigned to an account')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), equalTo('password')])
    submit = SubmitField('Change password')


class ChangeCurrencyForm(FlaskForm):
    currencies = []
    list = ccy.all()
    for item in sorted(list):
        currency = ccy.currency(item)
        currencies.append((item, item + " - " + currency.name))
    currency = SelectField(u'Currency', choices=currencies)
    submit = SubmitField('Set currency')


class CreateCategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Create Category')


class RenameForm(FlaskForm):
    old_name = StringField('Old Name', validators=[DataRequired()])
    new_name = StringField('New Name', validators=[DataRequired()])
    submit = SubmitField('Rename')


class DeleteForm(FlaskForm):
    item_to_delete = StringField('Old Name', validators=[DataRequired()])
    submit = SubmitField('Delete Category')


class CreateBudgetForm(FlaskForm):
    name = StringField('Budget Name', validators=[DataRequired()])
    submit = SubmitField('Create Budget')

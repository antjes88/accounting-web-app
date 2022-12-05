from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired, optional


class NewRecordForm(FlaskForm):
    account_type_debit = SelectField('debit', default='Choose Account Type', choices=[
        (None, 'Choose Account Type'),
        ('Asset', 'Asset'),
        ('Equity', 'Equity'),
        ('Expense', 'Expense'),
        ('Liability', 'Liability'),
        ('Revenue', 'Revenue')
    ], validators=[DataRequired()], id="debit")

    account_type_credit = SelectField('credit', default='Choose Account Type', choices=[
        (None, 'Choose Account Type'),
        ('Asset', 'Asset'),
        ('Equity', 'Equity'),
        ('Expense', 'Expense'),
        ('Liability', 'Liability'),
        ('Revenue', 'Revenue')
    ], validators=[DataRequired()], id="credit")

    asset_account_debit = SelectField('asset_debit', choices=[], validators=[optional()], id="asset_debit")
    asset_account_credit = SelectField('asset_credit', choices=[], validators=[optional()], id="asset_credit")

    equity_account_debit = SelectField('equity_debit', choices=[], validators=[optional()], id="equity_debit")
    equity_account_credit = SelectField('equity_credit', choices=[], validators=[optional()], id="equity_credit")

    expense_account_debit = SelectField('expense_debit', choices=[], validators=[optional()], id="expense_debit")
    expense_account_credit = SelectField('expense_credit', choices=[], validators=[optional()], id="expense_credit")

    liability_account_debit = SelectField('liability_debit', choices=[], validators=[optional()], id="liability_debit")
    liability_account_credit = SelectField('liability_credit', choices=[], validators=[optional()],
                                           id="liability_credit")

    revenue_account_debit = SelectField('revenue_debit', choices=[], validators=[optional()], id="revenue_debit")
    revenue_account_credit = SelectField('revenue_credit', choices=[], validators=[optional()], id="revenue_credit")

    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[optional()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def __init__(self, accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_account_debit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Asset']['account_name'].unique().tolist())
        self.asset_account_credit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Asset']['account_name'].unique().tolist())

        self.equity_account_debit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Equity']['account_name'].unique().tolist())
        self.equity_account_credit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Equity']['account_name'].unique().tolist())

        self.expense_account_debit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Expense']['account_name'].unique().tolist())
        self.expense_account_credit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Expense']['account_name'].unique().tolist())

        self.liability_account_debit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Liability']['account_name'].unique().tolist())
        self.liability_account_credit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Liability']['account_name'].unique().tolist())

        self.revenue_account_debit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Revenue']['account_name'].unique().tolist())
        self.revenue_account_credit.choices = sorted(accounts[
            accounts['account_type_name'] == 'Revenue']['account_name'].unique().tolist())

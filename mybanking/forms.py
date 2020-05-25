from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, InputRequired,\
    NumberRange, ValidationError

from mybanking.utils import round_up_amount, is_currency


class ExchangeInputForm(FlaskForm):
    currency = StringField('Currency', [DataRequired()])
    amount = DecimalField('Amount', [InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

    def validate_amount(form, field):
        amount = field.data
        if amount == 0:
            raise ValidationError(
                    'Number must be greater than zero.')

        if amount:
            amount = round_up_amount(amount)
            if amount is None:
                raise ValidationError(
                    'Number is too high. A max 24 precision value is allowed.')
            field.data = amount

    def validate_currency(form, field):
        currency = field.data
        if is_currency(currency):
            field.data = currency.upper()
        else:
            raise ValidationError('Invalid currency.')

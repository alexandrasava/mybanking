from marshmallow import fields, validates, ValidationError, pre_load, pre_dump
import sys

from mybanking import ma
from mybanking.models import Exchange
from mybanking.utils import pretty_print_decimal, is_currency


class ExchangeSchema(ma.Schema):

    class Meta:
        fields = ("id", "currency", "amount", "exchange_rate",
                  "amount_usd", "creation_date")

    @pre_dump
    def normalize_decimals(self, data, **kwargs):
        # Trim excessive 0s, for pretty printing.
        data.amount = pretty_print_decimal(data.amount)
        data.exchange_rate = pretty_print_decimal(data.exchange_rate)
        data.amount_usd = pretty_print_decimal(data.amount_usd)
        return data


class LastInputSchema(ma.Schema):
    currency = fields.Str(missing=None)
    number = fields.Integer(missing=None)

    @pre_load
    def validate_schema(self, in_data, **kwargs):
        """Make sure at least one field is set. Also, if a field is missing,
        set it's value to None.
        """
        new_in = {}
        new_in["currency"] = in_data.get("currency", None) or None
        new_in["number"] = in_data.get("number", None) or None

        if new_in["currency"] is None and new_in["number"] is None:
            raise ValidationError("Please set currency or number.")

        # Make sure the currency contains only upper case letters.
        if new_in["currency"]:
            new_in["currency"] = new_in["currency"].upper()

        return new_in

    @validates("number")
    def validate_number(self, value):
        if value is None:
            return
        if value < 0:
            raise ValidationError("Number must be greater than zero.")
        if value >= sys.maxsize:
            raise ValidationError("Number is too high.")

    @validates("currency")
    def validate_currency(self, value):
        if value and not is_currency(value):
            raise ValidationError("Invalid currency.")

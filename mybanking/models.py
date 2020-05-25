import datetime

from mybanking import db


class Exchange(db.Model):
    """Create a Exchange table."""
    __tablename__ = 'exchanges'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False, index=True)
    amount = db.Column(db.DECIMAL(24, 8), nullable=False)
    exchange_rate = db.Column(db.DECIMAL(24, 8), nullable=False)
    amount_usd = db.Column(db.DECIMAL(24, 8), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False, index=True)

    def __init__(self, data):
        self.currency = data.get('currency')
        self.amount = data.get('amount')
        self.exchange_rate = data.get('exchange_rate')
        self.amount_usd = data.get('amount_usd')
        self.creation_date = datetime.datetime.now()

    def __repr__(self):
        return \
            '<({})Exchange {} {} = {} USD (Rate: {})>'.format(
                self.creation_date, self.amount, self.currency,
                self.amount_usd, self.exchange_rate)

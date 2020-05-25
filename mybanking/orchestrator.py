from decimal import getcontext
import logging

from mybanking.utils import round_up_amount


logger = logging.getLogger('mybanking')
logger.setLevel(logging.DEBUG)


class AppOrchestrator:
    """ Component that contains the core logic of the application with all
    the use cases.

    Parameters
    ----------
    exchange_service: Service that handles all exchange rates.
    db_service: Service that handles database interaction.
    """

    def __init__(self, exchange_service, db_service):
        self.exchange_service = exchange_service
        self.db_service = db_service

    @staticmethod
    def _currency_to_usd(currency, amount, currency_rate):
        """Converts an amount into USD."""

        # Set a high precision so that we don't loose precision when doing
        # calculations.
        getcontext().prec = 30
        amount_usd = amount / currency_rate
        amount_usd = round_up_amount(amount_usd)
        if amount_usd is None:
            return None

        logger.debug(
            "Exchange {} {} = {} {} (Rate={})"
            .format(amount, currency, amount_usd, "USD", currency_rate)
        )
        return amount_usd

    def grab_and_save(self, currency, amount):
        """Fetches the exchange rate of USD against the currency, converts
        the amount into USD and saves it into the db.

        Return
        -------
        Returns the created resource or None.
        """
        rate = self.exchange_service.exchange(currency)
        if rate is None:
            return None

        amount_usd = self._currency_to_usd(currency, amount, rate)
        if amount_usd is None:
            return None
        resource = self.db_service.create({
            'currency': currency,
            'amount': amount,
            'exchange_rate': rate,
            'amount_usd': amount_usd
        })
        return resource

    def list_exchanges(self, currency, cnt):
        """Fetches the latest n exchanges of a currency."""
        if cnt is None:
            cnt = 1

        if currency is None:
            return self.db_service.find_latest(cnt)

        return self.db_service.find_by_currency(currency, cnt)

    def list_all_exchanges(self):
        """Fetches all the exchanged."""
        return self.db_service.list_all()

    def delete_exchange(self, exchange_id):
        """Delets an exchange."""
        return self.db_service.delete(exchange_id)

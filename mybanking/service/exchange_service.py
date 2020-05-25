import logging

from mybanking.utils import round_up_amount
from mybanking.utils import get_request


logger = logging.getLogger('mybanking')
logger.setLevel(logging.DEBUG)


class ExchangeService:
    """Calls OpenExchangeRates API and grabs the latest forex rates.

    Parameters
    ----------
    api_key (str): unique API ID.
    api_url (str): API URL.
    """
    BASE_CURRENCY = "USD"

    def __init__(self, api_url, api_key):
        self.url = api_url
        self.api_key = api_key

    def exchange(self, currency):
        """Returns the latest exchange rate for 1 currency against USD.

        Parameters
        ----------
        currency (str): currency to check USD exchange rate against.

        Returns
        -------
        Exchange rate of USD to currency.
        """
        if currency == self.BASE_CURRENCY:
            return 1

        params = self._fmt_request_params(currency)
        # Query Exchange Rate API for rates.
        res = get_request(self.url, params)
        if not res:
            return None

        # Check if the currency does not exist.
        if currency not in res['rates']:
            logger.warning(
                "No exchange rate was found for {currency}."
                "Currency {currency} might be misspelled."
                .format(currency=currency)
            )
            return None

        # This rate is: 1 USD to X currency
        usd_to_currency = res['rates'][currency]
        currency_to_usd = 1 / usd_to_currency

        return round_up_amount(currency_to_usd)

    def _fmt_request_params(self, currency):
        # NOTE: we should have added a base field to the params obj but
        # unfortunately we are allowed to access only a free version of the API
        # which has a default base='USD'.
        params = {
            "app_id": self.api_key,
            "symbols": currency,
        }

        return params

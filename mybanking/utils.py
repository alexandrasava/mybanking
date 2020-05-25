import re
from decimal import Decimal, ROUND_UP, getcontext, InvalidOperation
import logging
import requests
import simplejson


logger = logging.getLogger('mybanking')
logger.setLevel(logging.INFO)

AMOUNT_PRECISION = 24
AMOUNT_NR_DECIMALS = 8


def round_up_amount(amount):
    """Rounds up a number to 8 digits."""
    getcontext().prec = AMOUNT_PRECISION
    nr_digits = pow(10, -AMOUNT_NR_DECIMALS)
    try:
        return Decimal(amount).quantize(
            Decimal('0.00000001'), rounding=ROUND_UP)
    except InvalidOperation as e:
        logger.error("{}:{}".format(amount, e))
        return None


def trim_decimal(d):
    """Removes the rightmost trailing zeros."""
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def pretty_print_decimal(d):
    d = trim_decimal(d)

    # Prevent Python using scientific notations for values below pow(1,-7).
    if d < pow(10, -6):
        d = '{:.8f}'.format(d)
    return d


def is_currency(currency):
    """ Checks if this could be a valid currency."""
    pattern = r"^[a-zA-Z]{3}$"
    return re.match(pattern, currency)


def get_request(url, params):
    """ Makes a GET request.

    Parameters
    ----------
    url (str): URL path for the request.
    params (dict): HTTP GET parameters.
    """
    try:
        r = requests.get(url=url, params=params)
    except requests.exceptions.RequestException as e:
        logger.error(
            'Exception while executing GET request: {}'
            .format(e)
        )
        return None

    try:
        return r.json()
    except ValueError as e:
        logger.error(
            'GET response can\'t be JSON decoded: {}'
            .format(e)
        )
        return None


def json_response(data, status=200, err_msg=''):
    """ Formats HTTP response.

    Parameters
    ----------
    data (dict): data content to send.
    status (int): HTTP status code.
    err_msg (str): message in case the requested action failed to be processed.
    """
    if err_msg:
        payload = {
            'error': err_msg,
            'success': False
        }
    else:
        payload = {
            'data': data,
            'success': True
        }
    return (simplejson.dumps(payload, use_decimal=True), status,
            {'content-type': 'application/json'})

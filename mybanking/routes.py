from flask import request, render_template, flash, redirect, url_for
import logging
from marshmallow import ValidationError
import os

from mybanking import app
from mybanking.forms import ExchangeInputForm
from mybanking.models import Exchange
from mybanking.orchestrator import AppOrchestrator
from mybanking.schema import LastInputSchema
from mybanking.service import ExchangeService
from mybanking.service import MySQLDBService as DBService
from mybanking.utils import json_response


logger = logging.getLogger('mybanking')
logger.setLevel(logging.DEBUG)

exchange_service = ExchangeService(
    api_url=os.getenv('EXCHANGE_API_URL'),
    api_key=os.getenv('EXCHANGE_API_KEY')
)
app_orchestrator = AppOrchestrator(
    exchange_service=exchange_service,
    db_service=DBService()
)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Welcome")


@app.route('/exchanges', methods=['GET'])
def list_exchanges():
    """List all exchanges."""
    exchanges = app_orchestrator.list_all_exchanges()
    return render_template('exchanges.html',
                           exchanges=exchanges, title="Exchanges")


@app.route('/create_exchange', methods=['GET'])
def create_exchange_page():
    """Render html page create exchange."""
    form = ExchangeInputForm()

    return render_template('create_exchange.html', action="Add",
                           form=form, title="Exchange Amount")


@app.route('/filter', methods=['GET'])
def filter_exchange_page():
    """Render html page for filtering exchanges."""
    return render_template('filter_exchanges.html', title="Filter")


@app.route('/grab_and_save', methods=['POST'])
def grab_and_save():
    form = ExchangeInputForm()
    if not form.validate_on_submit():
        logger.error(form.errors)
        err_msg = 'Invalid request parameters: {}'.format(form.errors)
        return json_response({}, 400, err_msg)

    currency = form.currency.data
    amount = form.amount.data

    resource = app_orchestrator.grab_and_save(currency,  amount)
    if not resource:
        return json_response({}, 500, 'Error creating the exchange.')

    return json_response(resource, 201)


@app.route('/last', methods=["GET"])
def last():
    try:
        args = LastInputSchema().load(request.args)
    except ValidationError as err:
        logger.error(err.messages)
        err_msg = 'Invalid request parameters: {}'.format(err.messages)
        return json_response({}, 400, err_msg)

    exchanges = app_orchestrator.list_exchanges(
        args['currency'], args['number'])
    return json_response(exchanges, 200)


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    res = app_orchestrator.delete_exchange(id)
    if res:
        flash('You have successfully deleted the exchange.')
        return redirect(url_for('list_exchanges'))

    flash('Resource not found.')

    return json_response({}, 404, "Resource not found.")

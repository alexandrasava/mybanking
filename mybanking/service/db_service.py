import datetime
import logging
import sqlalchemy

from mybanking import db
from mybanking.models import Exchange
from mybanking.schema import ExchangeSchema
from sqlalchemy import desc


logger = logging.getLogger('mybanking')
logger.setLevel(logging.DEBUG)


class MySQLDBService:
    """Handles database operations."""

    @classmethod
    def create(cls, data):
        """Creates an exchange."""
        exchange = Exchange(data)
        db.session.add(exchange)
        res = cls._session_commit()

        if res:
            logger.debug(
                "Create exchange {}."
                .format(str(exchange))
            )
            return cls.dump(exchange)

        return None

    @classmethod
    def list_all(cls):
        """Returns all exchanges ordered by creation date."""
        exchanges = Exchange.query.order_by(
            desc(Exchange.creation_date)).all()
        logger.debug(
            "Fetch all exchanges: {}."
            .format(len(exchanges))
        )
        return [cls.dump(exchange) for exchange in exchanges]

    @classmethod
    def find_by_currency(cls, currency, cnt):
        """Returns the latest n exchanges of a currency."""
        exchanges = Exchange.query.filter_by(currency=currency).order_by(
            desc(Exchange.creation_date)).limit(cnt).all()

        logger.debug(
            "Fetch latest {} {} exchanges."
            .format(len(exchanges), currency)
        )
        return [cls.dump(exchange) for exchange in exchanges]

    @classmethod
    def find_latest(cls, cnt):
        """Returns the latest n exchanges from the table."""
        exchanges = Exchange.query.order_by(
            desc(Exchange.creation_date)).limit(cnt).all()

        logger.debug(
            "Fetch latest {} exchanges."
            .format(len(exchanges))
        )
        return [cls.dump(exchange) for exchange in exchanges]

    @classmethod
    def delete(cls, id):
        """Deletes an exchange entry."""
        exchange = Exchange.query.filter_by(id=id).first()
        if not exchange:
            logger.warning("Delete: no resource with ID={} found.".format(id))
            return False

        db.session.delete(exchange)
        res = cls._session_commit()
        if res:
            logger.debug("Delete resource ID={}.".format(id))
            return True

        return False

    @staticmethod
    def _session_commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False
        return True

    @staticmethod
    def dump(data):
        """Serializes an Exchange model."""
        return ExchangeSchema().dump(data)

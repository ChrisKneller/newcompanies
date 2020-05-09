import datetime
import decimal
import json
import re


def to_camelcase(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


def alchemyencoder(obj):
    """
    JSON encoder function for SQLAlchemy special classes.
    """

    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def to_json(self, rel=None):
    return json.dumps(self.to_dict(), default=alchemyencoder)

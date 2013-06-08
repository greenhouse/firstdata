from hashlib import sha1
from time import gmtime, strftime
import base64
import hmac
import json
import httplib
import decimal
import datetime
import os

version = '0.2'
__version__ = '0.2'


def JSONHandler(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.datetime):
        return str(obj)


class FirstDataError(Exception):
    def __init__(self, msg="unknown"):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class FirstData(object):
    """
    https://firstdata.zendesk.com/entries/407571-first-data-global-gateway-e4sm-web-service-api-reference-guide
    """
    GATEWAY_TEST = "api.demo.globalgatewaye4.firstdata.com"
    GATEWAY_LIVE = "api.globalgatewaye4.firstdata.com"

    def __init__(self, key, secret, **kwargs):
        self.arguments = {}
        self.key, self.secret = str(key), str(secret)
        self.arguments.update(kwargs)

    def process(self, httpclient=None, callback=None, test=False, verbose=None):
        """
        Send the transaction out to First Data
        """
        if verbose is None:
            verbose = bool(os.environ.get('FIRSTDATA_VERBOSE', False) == 'TRUE')

        gge4_date = strftime("%Y-%m-%dT%H:%M:%S", gmtime()) + 'Z'
        transaction_body = json.dumps(self.arguments, default=JSONHandler)
        content_digest = sha1(transaction_body).hexdigest()
        headers = {'Content-Type': "application/json",
                   'X-GGe4-Content-SHA1': content_digest,
                   'X-GGe4-Date': gge4_date,
                   'Authorization': 'GGE4_API ' + self.key + ':' + base64.b64encode(hmac.new(self.secret, "POST\napplication/json\n"+content_digest+"\n"+gge4_date+"\n/transaction/v12", sha1).digest())}
        if httpclient is not None:
            httpclient.fetch(("https://" + (self.GATEWAY_TEST if test else self.GATEWAY_LIVE) + "/transaction/v12"),
                             callback,
                             validate_cert=not test,
                             method="POST",
                             body=transaction_body,
                             headers=headers)
        else:
            # synchronous
            conn = httplib.HTTPSConnection(self.GATEWAY_TEST if test else self.GATEWAY_LIVE,
                                           timeout=10)
            conn.request("POST", "/transaction/v12", transaction_body, headers)
            response = conn.getresponse().read()

            if verbose:
                print dict(url="https://" + (self.GATEWAY_TEST if test else self.GATEWAY_LIVE) + "/transaction/v12",
                           transaction_body=transaction_body,
                           headers=headers,
                           response=response)

            try:
                data = json.loads(response)
                return data
            except ValueError:
                raise FirstDataError(response)

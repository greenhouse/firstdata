from hashlib import sha1
from time import gmtime, strftime
import base64
import hmac
import json
import httplib
import decimal
import datetime
import os
import urlparse

version = '0.4'
__version__ = '0.4'


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

    def process(self, httpclient=None, callback=None, test=False, verbose=None, retry_on_bmc=1):
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
                print json.dumps(dict(url="https://" + (self.GATEWAY_TEST if test else self.GATEWAY_LIVE) + "/transaction/v12",
                                      transaction_body=transaction_body,
                                      headers=headers,
                                      response=response))
                print response

            if type(retry_on_bmc) is int and 0 < retry_on_bmc < 4 and response == "Unauthorized Request. Bad or missing credentials.":
                """
                When FDs servers return "Unauthorized Request. Bad or missing credentials."
                which happend quite often for ABSOLUTLY no reason. We will try the request again.
                3 attempts will be made if this error occurs.
                I have contacted their support about this issue...sometime ago.
                """
                if verbose:
                    print json.dumps(dict(attempt=retry_on_bmc, source="First Data Unauthorized Request"))
                return self.process(httpclient, callback, test, verbose, retry_on_bmc+1)
            else:
                try:
                    return json.loads(response)
                except ValueError:
                    """FirstData sometimes sends back a http-args not a json argument...ugh.
                    """
                    return dict(urlparse.parse_qsl(response))

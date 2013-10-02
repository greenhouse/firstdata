from hashlib import sha1
from time import gmtime, strftime
import base64
import hmac
import json
import requests
import decimal
import datetime
import os
import urlparse

__version__ = version = VERSION = '0.9'


def JSONHandler(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.datetime):
        return str(obj)


class FirstData(object):
    """
    https://firstdata.zendesk.com/entries/407571-first-data-global-gateway-e4sm-web-service-api-reference-guide
    """
    GATEWAY_TEST = "api.demo.globalgatewaye4.firstdata.com"
    GATEWAY_LIVE = "api.globalgatewaye4.firstdata.com"

    def __init__(self, key, secret, **payment_arguments):
        self._key, self._secret = str(key), str(secret)
        self._arguments = {}
        self._arguments.update(payment_arguments)
        self._callback = None
        self._httpclient = None
        self._verbose = False
        self._test = False

    def process(self, httpclient=None, callback=None, test=False, verbose=None, retry_on_bmc=1):
        """Send the transaction out to First Data
        """
        if verbose is None:
            self._verbose = bool(os.environ.get('FIRSTDATA_VERBOSE', False) == 'TRUE')

        self._test = test
        self._retry_on_bmc = retry_on_bmc
        assert type(self._test) is bool, "Invalid test value, must be type boolean"

        gge4_date = strftime("%Y-%m-%dT%H:%M:%S", gmtime()) + 'Z'
        transaction_body = json.dumps(self._arguments, default=JSONHandler)
        content_digest = sha1(transaction_body).hexdigest()
        headers = {'Content-Type': "application/json",
                   'Accept': "application/json",
                   'X-GGe4-Content-SHA1': content_digest,
                   'X-GGe4-Date': gge4_date,
                   'Authorization': 'GGE4_API ' + self._key + ':' + base64.b64encode(hmac.new(self._secret, "POST\napplication/json\n"+content_digest+"\n"+gge4_date+"\n/transaction/v12", sha1).digest())}

        if httpclient is not None:
            # Asyncronous for Tornado AsyncHTTPClient requests
            assert hasattr(callback, "__call__"), "Callback must be callable"
            self._callback = callback
            self._httpclient = httpclient
            httpclient.fetch(("https://" + (self.GATEWAY_TEST if self._test else self.GATEWAY_LIVE) + "/transaction/v12"),
                             callback=self.process_repsonse,
                             validate_cert=not self._test,
                             method="POST",
                             body=transaction_body,
                             headers=headers)
        else:
            # Synchronous
            r = requests.post(("https://" + (self.GATEWAY_TEST if self._test else self.GATEWAY_LIVE) + "/transaction/v12"),
                              timeout=20,
                              verify=not self._test,
                              data=transaction_body,
                              headers=headers)
            return self.process_repsonse(r)

    def process_repsonse(self, response):
        if self._httpclient and self._callback:
            response = response.body
        elif isinstance(response, requests.Response):
            response = response.text
        if self._verbose:
            print response
        if type(self._retry_on_bmc) is int and 0 < self._retry_on_bmc < 4 and response == "Unauthorized Request. Bad or missing credentials.":
            """When FDs servers return "Unauthorized Request. Bad or missing credentials."
            which happend quite often for ABSOLUTLY no reason. We will try the request again.
            3 attempts will be made if this error occurs.
            I have contacted their support about this issue...sometime ago.
            """
            if self._verbose:
                print json.dumps(dict(attempt=self._retry_on_bmc, source="First Data Unauthorized Request"))
            return self.process(httpclient=self._httpclient,
                                callback=self._callback,
                                test=self._test,
                                verbose=self._verbose,
                                retry_on_bmc=self._retry_on_bmc+1)
        else:
            try:
                json_response = json.loads(response)
                if self._callback:
                    self._callback(json_response)
                else:
                    return json_response
            except:
                """FirstData sometimes sends back a http-args not a json argument...ugh.
                """
                try:
                    urlargs = dict(urlparse.parse_qsl(response))
                    if len(urlargs)==0:
                        raise ValueError("Move to text...")
                    if self._callback:
                        self._callback(urlargs)
                    else:
                        return urlargs
                except:
                    """FirstData also sends back string errors.
                    """
                    # make my own FirstData Error
                    error = {"transaction_approved":0,"bank_message":response,"amount":self._arguments.get('amount',0),"fraud_suspected":None,"success":False,"reference_3":None,"cvd_presence_ind":0,"bank_resp_code":None,"partial_redemption":0,"card_cost":None,"exact_message":response,"logon_message":None,"secure_auth_result":None,"payer_id":None,"transaction_type":self._arguments.get('transaction_type'),"cc_verification_str2":None,"ecommerce_flag":None,"reference_no":self._arguments.get('reference_no'),"cavv":None,"previous_balance":None,"error_description":None,"tax2_number":None,"exact_resp_code":None,"secure_auth_required":None,"amount_requested":None,"client_email":None,"cc_verification_str1":None,"language":None}
                    if self._callback:
                        self._callback(error)
                    else:
                        return error

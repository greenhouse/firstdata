[![Build Status](https://secure.travis-ci.org/stevepeak/firstdata.png)](http://travis-ci.org/stevepeak/firstdata)

> **IMPORTANT** This project is no longer maintained by @stevepeak. If you would like ownership over this repo I will transfer it. Thanks!

## Unofficial First Data's Global Gateway e4 Python Handler

> This project is not endourced by myself or First Data. Please read disclaimer before use. Thanks

## Install
`pip install firstdata`

## Usage
```python
import firstdata

fd = firstdata.FirstData(key, secret,
    gateway_id=gateway_id,
    password=password,
    transaction_type="01",
    amount="1.00",
    cardholder_name="Customer",
    cc_number="41111111111111111",
    cc_expiry="1215")

result = fd.process(test=use['test'])

# dict of results: result['transaction_approved'], result['authorization_num'], ....
```

## Link
* [FirstData API Guide](https://firstdata.zendesk.com/entries/407571-First-Data-Global-Gateway-e4-Web-Service-API-Reference-Guide)

## License
Licensed under the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html).
   
## Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

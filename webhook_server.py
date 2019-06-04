from flask import Flask, jsonify, request
import os
import base64
import hashlib
import hmac
from private_app import PrivateApp


consumer_key = os.getenv('CONSUMER_KEY')
if not consumer_key:
    raise EnvironmentError('Environment variable CONSUMER_KEY not found. How to run: \
    $ CONSUMER_KEY=<your consumer key> python test.py')


with open(os.path.abspath('privatekey.pem')) as f:
    private_key = f.read()

client = PrivateApp(private_key, consumer_key)
print('Instance created:', client)


webhook_key = os.getenv('WEBHOOK_KEY')
app = Flask('MyApp')


@app.route('/')
def index():
    return jsonify(Hello='World')


@app.route('/webhook', methods=['POST'])
def webhook():
    req_data = request.json
    if not len(req_data['events']):  # assume this is intent to receive request
        hashed = hmac.new(bytes(webhook_key, 'utf8'), request.data, hashlib.sha256)
        signature = base64.b64encode(hashed.digest()).decode('utf-8')
        if request.headers.get('X-Xero-Signature') == signature:
            return '', 200
        return '', 401

    process_events(req_data['events'])
    return '', 200


def process_events(events):
    for event in events:
        if event['eventCategory'] == 'INVOICE':
            invoice = client.invoices(id=event['resourceId'])
            if invoice['Status'] == 'PAID':
                print('NEW PAID INVOICE:')
                print(invoice, '\n\n')
            else:
                print(f'Received a non-paid invoice {event["eventType"]}: {invoice["InvoiceID"]}')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4567', debug=True)
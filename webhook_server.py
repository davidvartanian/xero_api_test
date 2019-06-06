from flask import Flask, jsonify, request
import os
import base64
import hashlib
import hmac
from pprint import pprint
from private_app import PrivateApp
from dotenv import load_dotenv
load_dotenv()


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


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify(Hello='World', Host=request.host), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    provided_signature = request.headers.get('X-Xero-Signature')
    hashed = hmac.new(bytes(webhook_key, 'utf8'), request.data, hashlib.sha256)
    generated_signature = base64.b64encode(hashed.digest()).decode('utf-8')
    if provided_signature != generated_signature:
        return '', 401
    req_data = request.json
    if len(req_data['events']):  # assume this is intent to receive request
        process_events(req_data['events'])
    return '', 200


def process_events(events):
    for event in events:
        if event['eventCategory'] == 'INVOICE':
            invoice = client.invoices(id=event['resourceId'])
            if invoice['Status'] == 'PAID':
                print('NEW PAID INVOICE:')
                pprint(invoice, '\n\n')
            else:
                pprint(f'Received a non-paid invoice {event["eventType"]}: {invoice["InvoiceID"]}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4567', debug=True)
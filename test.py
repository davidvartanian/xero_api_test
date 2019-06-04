#How to run:
# $ CONSUMER_KEY=<your consumer key> python test.py

from private_app import PrivateApp
from itertools import islice
from pprint import pprint
import os


consumer_key = os.getenv('CONSUMER_KEY')
if not consumer_key:
    raise EnvironmentError('Environment variable CONSUMER_KEY not found. How to run: \
    $ CONSUMER_KEY=<your consumer key> python test.py')


with open(os.path.abspath('privatekey.pem')) as f:
    private_key = f.read()

app = PrivateApp(private_key, consumer_key)
print('Instance created:', app)

smalldict = lambda x, keys: {k: v for k, v in x.items() if k in keys}
keys = ['PaymentID', 'Date', 'Status', 'Amount']
print('\nFilter response dictionaries to keys:', keys)

print('\nGet all payments')
g = app.payments()
print(f'Length of response: {len(g)}')
print('Available keys:', g.keys)

print('\nIterate 5 elements')
for r in islice(g, 5):
    pprint(smalldict(r, keys))

print('\nNext element:')
pprint(smalldict(next(g), keys))

print('\nGet an element by ID (all keys):')
payment_id = 'dac50c7a-d12b-440c-b907-fae1bbbc36a1'
payment = app.payments(id=payment_id)
pprint(payment)

print('\nFilter by IsReconciled=False:')
g = app.payments(IsReconciled=False)
print(f'\nLength of response: {len(g)}')

print('\nFilter by invalid field:')
r = app.payments(InvalidField=1)
print(type(r), len(r))

print('\nFilter by invalid ID:')
r = app.payments(id='invalid-id')
print(type(r))
print('\nPayments Done.\n\n')

print('Get all invoices')
g = app.invoices()
keys = ['InvoiceID', 'Type', 'InvoiceNumber', 'Reference', 'Payments', 'AmountDue', 'AmountPaid', 'Date', 'Status',
        'Total', 'CurrencyCode']
print(f'Length of response: {len(g)}')
print('Available keys:', g.keys)

print('\nIterate 5 elements')
for r in islice(g, 5):
    pprint(smalldict(r, keys))

print('\nGet invoices with Status PAID:')
g = app.invoices(Status='PAID')
for row in g:
    pprint(smalldict(row, keys))

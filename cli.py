from argparse import ArgumentParser
from private_app import PrivateApp
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    consumer_key = os.getenv('CONSUMER_KEY')
    if not consumer_key:
        raise EnvironmentError('Environment variable CONSUMER_KEY not found. How to run: \
        $ CONSUMER_KEY=<your consumer key> python test.py')

    with open(os.path.abspath('privatekey.pem')) as f:
        private_key = f.read()

    app = PrivateApp(private_key, consumer_key)
    argparser = ArgumentParser()
    argparser.add_argument('entity', type=str, help='Entity name. Valid values: invoices, payments.')
    argparser.add_argument('id', type=str, help='ID related to the specified entity.')
    args = vars(argparser.parse_args())
    if args['entity'] not in ['invoices', 'payments']:
        raise ValueError(f'Invalid entity {args["entity"]}. Valid options: invoices, payments.')
    document = getattr(app, args['entity'])(args['id'])
    pprint(document)

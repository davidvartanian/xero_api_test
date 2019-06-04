# Xero API Test
Playing around with Xero API Python SDK

## Create Xero Private Application
Create an app here: https://developer.xero.com/.
You will need the consumer key provided when you create an app.

## Setup virtual environment
If you use Anaconda:
* `$ conda create -n venv pip setuptools`
* `$ conda activate venv`

If you use virtualenv:
* `$ python -m venv venv`
* `$ source venv/bin/activate`

Then:
* `$ pip install requirements.txt`


## How to run CLI test
`$ CONSUMER_KEY=<your consumer key> python test.py`

## How to run Webhook test
* Setup ngrok to run on a port of your choice (see [how to setup ngrok](https://ngrok.com/)):
  * `$ ngrok http 4567`
* `$ WEBHOOK_KEY=<your webhook key> CONSUMER_KEY=<your consumer key> python webhook_server.py`
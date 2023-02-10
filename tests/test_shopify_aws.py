
from .. import ShopifyAwsLambda
import json
import logging
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
ENV = os.getenv('ENV')

def test_shopify_aws(caplog):

    caplog.set_level(logging.DEBUG) if ENV == 'development' else caplog.set_level(logging.INFO)

    with open('tests/order.json', 'r') as f:
        paid_event = json.load(f)

        response = ShopifyAwsLambda.lambda_handler(paid_event, None)

    logging.debug(response)

    assert response.status_code == 200

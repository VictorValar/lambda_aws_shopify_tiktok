
from .. import ShopifyAwsLambda
import json

def test_shopify_aws(caplog):
    with open('tests/order.json', 'r') as file:
        paid_event = json.load(file)

        response = ShopifyAwsLambda.lambda_handler(paid_event, None)

    # logging.debug(response)

    assert response.get('code') == 0 # Tiktok custom 200 response code

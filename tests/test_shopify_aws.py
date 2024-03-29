
from .. import app
import json

def test_shopify_aws(caplog):
    with open('tests/order.json', 'r', encoding='utf-8') as file:
        paid_event = json.load(file)

        response = app.lambda_handler(paid_event, None)

    # logging.debug(response)

    assert response.get('code') == 0 # Tiktok custom 200 response code

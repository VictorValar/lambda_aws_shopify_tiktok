## AWS Lambda function to process Shopify webhooks.
## If you want to use this function, you need to create a .env file with the following variables:
## META_ACCESS_TOKEN
## PIXEL_ID
## SHOPIFY_ACCESS_TOKEN
## TEST_EVENT_CODE

## Any suggestions or improvements are welcome! Feel free to contribute to this project or provide feedback.
from pytt_events.auth import TikTokAuth
from pytt_events.event import Event
from pytt_events.properties import Properties
from pytt_events.context import Context, Ad, Page, User
from pytt_events.properties import Content, ContentType
from pytt_events.tiktok_events_api import TikTokEventsApi
import logging
import traceback
import time, datetime
import json
from requests import Response

def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging.debug(msg='funcall: lambda_handler')
    paylod = event.get('detail').get('payload')
    logging.info(msg='payload: ' + json.dumps(paylod, indent=4, sort_keys=True))

    try:
        tiktok_response = main(payload=paylod)

        # error code handling is done by the TikTok Events API wrapper
        return tiktok_response

    except Exception as excp:
        traceback.print_exc()
        logging.error(excp)
        return {
            'statusCode': 400 if type(excp) == ValueError else 500,
            'body': 'event not sent: ' + str(excp) + ' ' + str(traceback.format_exc())
        }

def main(payload) -> Response:
    """
    Sends events to TikTok Pixel
    """
    for item in payload.get('note_attributes'):
        if item["name"] == "ttclidCookie":
            ttclid = item["value"]
        elif item["name"] == "ttpCookie":
            ttp = item["value"]
        elif item["name"] == "userAgent":
            userAgent = item["value"]
        elif item["name"] == "userIP":
            userIP = item["value"]
        elif item["name"] == "Link de pedido":
            event_source_url = payload.get("order_status_url")

    if ttclid == 'Not Found':
        ttclid = None
    if ttp == 'Not Found':
        ttp = None

    api = TikTokEventsApi()
    auth = TikTokAuth()

    # print(payload.get('customer'))

    context = Context(
        user_agent=userAgent,
        ip=userIP,
        ad=Ad(callback=ttclid),
        page=Page(
            url=event_source_url,
            referrer=event_source_url,
        ),
        user=User(
            external_id=payload.get('customer').get('id'),
            email=payload.get('customer')['email'],
            phone_number=payload.get('phone'),
            ttp=ttp
        ))

    items = payload.get('line_items')
    contents: list[Content] = []

    for item in items:
        content = Content(
            content_id=item.get('product_id'),
            content_name=item.get('name'),
            content_category=item.get('vendor'),
            price=item.get('price'),
            quantity=item.get('quantity'),
            content_type="product"

        )
        contents.append(content)

    properties = Properties(
        currency='BRL', # ISO 4217
        value=float(payload.get('total_price')),
        description="Payment status",
        query='none',
        contents=contents,
        # content_type="product"
    )
    event = Event(
        pixel_code=auth.TIKTOK_PIXEL_ID,
        test_event_code=auth.TIKTOK_TEST_EVENT_CODE,
        event='CompletePayment',
        event_id=f"{str(time.time())}.{userIP}",
        timestamp=payload.get('created_at', datetime.datetime.now()),
        context=context,
        properties=properties,
    )

    logging.debug('event created')


    response = api.post_event(
        event=event,
        auth=auth
    )


    return response.json()


#!/bin/bash

clear
echo "Set Lambda environment variables for GL_TIKTOK_SHOPIFY_DOCKER..."

# Read environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Send environment variables to AWS Lambda
echo "Set Lambda environment variables for GL_TIKTOK_SHOPIFY_DOCKER..."
aws lambda update-function-configuration --function-name GL_TIKTOK_SHOPIFY_DOCKER --environment Variables="{TIKTOK_ACCESS_TOKEN=$TIKTOK_ACCESS_TOKEN,TIKTOK_PIXEL_ID=$TIKTOK_PIXEL_ID,TIKTOK_TEST_EVENT_CODE=$TIKTOK_TEST_EVENT_CODE,TIKTOK_API_VERSION=$TIKTOK_API_VERSION,ENV=$ENV}"

echo "Vars: $TIKTOK_ACCESS_TOKEN, $TIKTOK_PIXEL_ID, $TIKTOK_TEST_EVENT_CODE, $TIKTOK_API_VERSION, $ENV"

echo "Set Lambda environment variables for LOOD_TIKTOK_SHOPIFY_DOCKER..."

# Read environment variables from lood.env file
export $(grep -v '^#' lood.env | xargs)

# Send environment variables to AWS Lambda
aws lambda update-function-configuration --function-name LOOD_TIKTOK_SHOPIFY_DOCKER --environment Variables="{TIKTOK_ACCESS_TOKEN=$TIKTOK_ACCESS_TOKEN,TIKTOK_PIXEL_ID=$TIKTOK_PIXEL_ID,TIKTOK_TEST_EVENT_CODE=$TIKTOK_TEST_EVENT_CODE,TIKTOK_API_VERSION=$TIKTOK_API_VERSION,ENV=$ENV}"

echo "Vars: $TIKTOK_ACCESS_TOKEN, $TIKTOK_PIXEL_ID, $TIKTOK_TEST_EVENT_CODE, $TIKTOK_API_VERSION, $ENV"

echo "Done!"

#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]
then
  export $(grep -v '^#' upload.env | xargs)
fi

clear
echo "Building docker image..."
docker build -t ${DOCKER_TAG} .

echo 'Tagging image...'
docker tag ${DOCKER_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_TAG}

echo "Pushing image to AWS ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_TAG}

echo "Updating GL Lambda function..."
aws lambda update-function-code --function-name ${GL_LAMBDA_FUNCTION} --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_TAG}:latest

echo "Updating LOOD Lambda function..."
aws lambda update-function-code --function-name ${LOOD_LAMBDA_FUNCTION} --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_TAG}:latest

echo "Done!"

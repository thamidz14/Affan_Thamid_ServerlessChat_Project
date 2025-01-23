import json
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Check if 'httpMethod' is in the event
    if 'httpMethod' not in event:
        logger.error("Invalid request: Missing httpMethod")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request: Missing httpMethod')
        }

    if event['httpMethod'] == 'POST':
        try:
            # Store a new message
            body = json.loads(event['body'])
            message_id = str(datetime.now().timestamp())
            table.put_item(Item={
                'MessageID': message_id,
                'Username': body['username'],
                'Message': body['message'],
                'Timestamp': message_id
            })
            logger.info("Message stored successfully")
            return {
                'statusCode': 200,
                'body': json.dumps('Message stored successfully')
            }
        except Exception as e:
            logger.error("Error storing message: %s", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps('Error storing message')
            }
    elif event['httpMethod'] == 'GET':
        try:
            # Retrieve messages
            response = table.scan()
            logger.info("Messages retrieved successfully")
            return {
                'statusCode': 200,
                'body': json.dumps(response['Items'])
            }
        except Exception as e:
            logger.error("Error retrieving messages: %s", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps('Error retrieving messages')
            }
    else:
        logger.error("Unsupported method: %s", event['httpMethod'])
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported method')
        }
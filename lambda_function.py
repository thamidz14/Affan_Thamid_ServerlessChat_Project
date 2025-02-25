import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('ChatMessages', 'ChatMessages')  # Fallback to 'ChatMessages' if not set
table = dynamodb.Table(TABLE_NAME)

def validate_message(body):
    """Validate the message payload"""
    required_fields = ['username', 'message']
    for field in required_fields:
        if field not in body:
            raise ValueError(f"Missing required field: {field}")
        if not body[field] or not isinstance(body[field], str):
            raise ValueError(f"Invalid {field}")
    if len(body['message']) > 1000:  # Limit message length
        raise ValueError("Message too long")
    return True

def get_cors_headers():
    """Get CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',  # Configure this based on your requirements
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }

def store_message(username, message):
    """Store a new message"""
    message_id = str(datetime.now().timestamp())
    table.put_item(Item={
        'MessageID': message_id,
        'Username': username,
        'Message': message,
        'Timestamp': message_id
    })
    logger.info("Message stored successfully")
    return message_id

def get_messages(last_evaluated_key=None, limit=50):
    """Retrieve messages with pagination"""
    scan_params = {
        'Limit': min(limit, 100)  # Cap at 100 items per request
    }
    if last_evaluated_key:
        scan_params['ExclusiveStartKey'] = last_evaluated_key

    response = table.scan(**scan_params)
    
    result = {
        'items': response['Items'],
        'last_evaluated_key': response.get('LastEvaluatedKey')
    }
    return result

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Handle different types of API Gateway integrations
    if 'requestContext' in event and 'http' in event['requestContext']:
        # HTTP API (v2)
        http_method = event['requestContext']['http']['method']
    elif 'requestContext' in event and 'httpMethod' in event['requestContext']:
        # REST API (v1)
        http_method = event['requestContext']['httpMethod']
    elif 'httpMethod' in event:
        # Direct integration
        http_method = event['httpMethod']
    else:
        logger.error("Invalid request: Missing httpMethod")
        return {
            'statusCode': 400,
            'headers': get_cors_headers(),
            'body': json.dumps('Invalid request: Missing httpMethod')
        }

    headers = get_cors_headers()
    headers['Content-Type'] = 'application/json'

    # Handle OPTIONS request for CORS
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight request successful'})
        }

    try:
        if http_method == 'POST':
            # Get the request body
            if isinstance(event.get('body'), str):
                body = json.loads(event['body'])
            else:
                body = event.get('body', {})

            if not body:
                raise ValueError("Missing request body")
            
            validate_message(body)
            message_id = store_message(body['username'], body['message'])
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Message stored successfully', 'id': message_id})
            }

        elif http_method == 'GET':
            # Get pagination parameters
            query_params = event.get('queryStringParameters', {}) or {}
            last_evaluated_key = query_params.get('lastEvaluatedKey')
            limit = int(query_params.get('limit', '50'))
            
            result = get_messages(
                last_evaluated_key=json.loads(last_evaluated_key) if last_evaluated_key else None,
                limit=limit
            )
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'messages': result['items'],
                    'lastEvaluatedKey': result['last_evaluated_key']
                }, default=str)  # Handle datetime serialization
            }
        else:
            logger.error(f"Unsupported method: {http_method}")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': f'Unsupported method: {http_method}'})
            }
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': str(ve)})
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

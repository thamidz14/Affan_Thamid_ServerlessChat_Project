import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

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

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Check if 'httpMethod' is in the event
    if 'httpMethod' not in event:
        logger.error("Invalid request: Missing httpMethod")
        return {
            'statusCode': 400,
            'headers': get_cors_headers(),
            'body': json.dumps('Invalid request: Missing httpMethod')
        }

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if event['httpMethod'] == 'POST':
        try:
            # Store a new message
            if not event.get('body'):
                raise ValueError("Missing request body")
            body = json.loads(event['body'])
            validate_message(body)
            
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
                'headers': headers,
                'body': json.dumps({'message': 'Message stored successfully', 'id': message_id})
            }
        except ValueError as ve:
            logger.error("Validation error: %s", str(ve))
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': str(ve)})
            }
        except Exception as e:
            logger.error("Error storing message: %s", str(e))
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    elif event['httpMethod'] == 'GET':
        try:
            # Get pagination parameters
            last_evaluated_key = event.get('queryStringParameters', {}).get('lastEvaluatedKey')
            limit = int(event.get('queryStringParameters', {}).get('limit', '50'))
            
            # Build scan parameters
            scan_params = {
                'Limit': min(limit, 100)  # Cap at 100 items per request
            }
            if last_evaluated_key:
                scan_params['ExclusiveStartKey'] = json.loads(last_evaluated_key)

            # Retrieve messages with pagination
            response = table.scan(**scan_params)
            
            result = []
            for item in response['Items']:
                responseItem = {
                    'MessageID': item['MessageID'],
                    'Username': item['Username'],
                    'Message': item['Message'],
                    'Timestamp': float(item['Timestamp'])
                }
                result.append(responseItem)
            
            # Include pagination token if more results exist
            if 'LastEvaluatedKey' in response:
                result = {'items': result, 'lastEvaluatedKey': json.dumps(response['LastEvaluatedKey'])}
            else:
                result = {'items': result}

            logger.info("Messages retrieved successfully")
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        except Exception as e:
            logger.error("Error retrieving messages: %s", str(e))
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    else:
        logger.error("Unsupported method: %s", event['httpMethod'])
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Unsupported method'})
        }

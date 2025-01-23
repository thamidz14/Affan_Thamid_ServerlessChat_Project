# Affan_Thamid_ServerlessChat_Project

# Step 1: Set Up Your Development Environment</span> 
  1. Install Node.js and npm: Ensure you have Node.js and npm installed on your machine. You can download them from nodejs.org.

# MacOS Users
Download and install fnm:
curl -o- https://fnm.vercel.app/install | bash

Download and install Node.js:
fnm install 23

Verify the Node.js version:
node -v # Should print "v23.6.0".

Verify npm version:
npm -v # Should print "10.9.2".

# Windows Users

Download and install fnm:
winget install Schniz.fnm

Download and install Node.js:
fnm install 22

Verify the Node.js version:
node -v # Should print "v22.13.0".

Verify npm version:
npm -v # Should print "10.9.2".


# Install AWS CLI: Download and install the AWS Command Line Interface from AWS CLI.

Install or update the AWS CLI
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /

   which aws
   aws --version

# Configure AWS CLI: Run aws configure and enter your AWS access key, secret key, region, and output format.

Create AWS Account - Free Tier Version
Go to AWS Identity and Access Management
Create IAM User

# Install Serverless Framework: Use npm to install the Serverless Framework globally:

   npm install -g serverless

# Step 2: Create a New Serverless Project 

Initialize a Serverless Project:

   serverless create --template aws-nodejs --path serverless-chat-app
   cd serverless-chat-app

Install Dependencies:

   npm init -y
   npm install aws-sdk uuid

# Step 3: Set Up AWS Services

  1. Create a DynamoDB Table: Go to the AWS Management Console and create a DynamoDB table named ChatMessages with a primary key messageId.
  2. Define Serverless Functions: Open serverless.yml and define your Lambda functions and DynamoDB table

```
   service: serverless-chat-app

   provider:
     name: aws
     runtime: nodejs14.x
     region: us-east-1

   functions:
     createMessage:
       handler: handler.createMessage
       events:
         - http:
             path: messages
             method: post

  getMessages:
       handler: handler.getMessages
       events:
         - http:
             path: messages
             method: get

   resources:
     Resources:
       ChatMessages:
         Type: AWS::DynamoDB::Table
         Properties:
           TableName: ChatMessages
           AttributeDefinitions:
             - AttributeName: messageId
               AttributeType: S
           KeySchema:
             - AttributeName: messageId
               KeyType: HASH
           ProvisionedThroughput:
             ReadCapacityUnits: 1
             WriteCapacityUnits: 1
```
# Step 4: Implement Lambda Functions
   
1. Create handler.js: Implement the logic for creating and retrieving messages.

```
const AWS = require('aws-sdk');
const uuid = require('uuid');

const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.createMessage = async (event) => {
  const data = JSON.parse(event.body);
  const params = {
    TableName: 'ChatMessages',
    Item: {
      messageId: uuid.v4(),
      text: data.text,
      createdAt: new Date().toISOString(),
    },
  };

  try {
    await dynamoDb.put(params).promise();
    return {
      statusCode: 200,
      body: JSON.stringify(params.Item),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Could not create message' }),
    };
  }
};

module.exports.getMessages = async () => {
  const params = {
    TableName: 'ChatMessages',
  };

  try {
    const result = await dynamoDb.scan(params).promise();
    return {
      statusCode: 200,
      body: JSON.stringify(result.Items),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Could not retrieve messages' }),
    };
  }
};
```


# Step 1: Create an S3 Bucket**:
This will host your static files (HTML, CSS, JavaScript).
Enable static website hosting in the bucket properties.

  # 1. Create an S3 Bucket:
`aws s3api create-bucket --bucket thamidaffan-bucket --region us-east-1`
  - Stuck on configuring affan s3 bucket thamidaffan-bucket to my aws account

  # 2. Create a DynamoDB Table: -  Step Completed 
  Name it ChatMessages
  Set a primary key, e.g., MessageID (String).

  # 3. Create an IAM Role:

This role will be used by your Lambda function.
Attach policies for DynamoDB access and CloudWatch logs.

# Step 2: Develop the Backend with AWS Lambda

  # 1. Create a Lambda Function

Use Python as the runtime.
Assign the IAM role created earlier.

This function will handle storing and retrieving chat messages.

python:lambda_function.py

```
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Store a new message
        body = json.loads(event['body'])
        message_id = str(datetime.now().timestamp())
        table.put_item(Item={
            'MessageID': message_id,
            'Username': body['username'],
            'Message': body['message'],
            'Timestamp': message_id
        })
        return {
            'statusCode': 200,
            'body': json.dumps('Message stored successfully')
        }
    elif event['httpMethod'] == 'GET':
        # Retrieve messages
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported method')
        }
```
```
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Store a new message
        body = json.loads(event['body'])
        message_id = str(datetime.now().timestamp())
        table.put_item(Item={
            'MessageID': message_id,
            'Username': body['username'],
            'Message': body['message'],
            'Timestamp': message_id
        })
        return {
            'statusCode': 200,
            'body': json.dumps('Message stored successfully')
        }
    elif event['httpMethod'] == 'GET':
        # Retrieve messages
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported method')
        }
```

# Step 3: Set Up API Gateway

1. **Create a REST API**:
 Create a new resource, e.g., `/chat`.
 Create two methods: `POST` and `GET`.

2. Integrate with Lambda**:
   For both methods, set the integration type to Lambda Function.
   Select the Lambda function you created.

3. Deploy the API:
   Create a new stage and deploy your API.

  **Step-by-Step Guide to Integrate Lambda with API Gateway**
---
`Open the AWS Management Console:
- Navigate to the AWS Management Console.

Go to API Gateway:
- In the AWS Management Console, search for "API Gateway" and select it.

Create a New API:
- Click on "Create API".
- Choose "REST API" and select "Build".

Configure the API:
- Enter a name for your API, e.g., "ChatAPI".
- Provide a description if desired.
- Choose "Regional" for the endpoint type.
- Click "Create API".

Create a Resource:
- In the left-hand pane, click on "Resources".
- Click "Actions" and select "Create Resource".
- Enter a resource name, e.g., "chat".
- Click "Create Resource".

Create Methods:
- Select the newly created resource (e.g., /chat). 
- Click "Actions" and select "Create Method". 
- Choose POST from the dropdown and click the checkmark. 
- Repeat the process to create a GET method.

Integrate with Lambda:
- For each method (POST and GET):
- Select the method (e.g., POST).
- In the "Integration type" section, choose "Lambda Function".
- Check "Use Lambda Proxy integration".
- In the "Lambda Function" field, start typing the name of your Lambda function and select it from the dropdown.
- Click "Save".
- You may be prompted to add permissions for API Gateway to invoke your Lambda function. Click "OK".

Deploy the API:
- Click on "Actions" and select "Deploy API".
- Create a new deployment stage, e.g., "prod".
- Click "Deploy".

Note the Invoke URL:
- After deployment, you'll see an "Invoke URL" for your API. This is the URL you'll use in your frontend code to interact with the API.`
---

# Step 4: Develop the Frontend
1. **Create HTML/JavaScript Files**:
   
   - These files will be uploaded to your S3 bucket.

```html:index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Serverless Chat App</title>
    <style>
        /* Add some basic styling */
    </style>
</head>
<body>
    <h1>Chat Application</h1>
    <div id="chat-box"></div>
    <input type="text" id="username" placeholder="Username">
    <input type="text" id="message" placeholder="Message">
    <button onclick="sendMessage()">Send</button>

    <script>
        const apiUrl = 'https://hbbfrex8m8.execute-api.us-east-1.amazonaws.com/prod';

        async function sendMessage() {
            const username = document.getElementById('username').value;
            const message = document.getElementById('message').value;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, message })
            });

            if (response.ok) {
                loadMessages();
            }
        }

        async function loadMessages() {
            const response = await fetch(apiUrl);
            const messages = await response.json();
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = messages.map(msg => `<p><strong>${msg.Username}:</strong> ${msg.Message}</p>`).join('');
        }

        // Load messages on page load
        loadMessages();
    </script>
</body>
</html>
```
# Step 5: Deploy the Frontend

1. Upload Files to S3:
Upload your index.html and any other static files to the S3 bucket.
Make sure the files are publicly accessible.

2. Access the Application:
Use the S3 bucket URL to access your chat application.

# Step 6: Test the Application
Open the S3 URL in a browser.
Test sending and receiving messages.

aws sts assume-role --role-arn arn:aws:iam::301570629804:role/testhamidaffansync --role-session-name testSessionName

aws sts assume-role --role-arn arn:aws:iam::954976328760:role/Affan_Thamid_ServerlessChat_Project --role-session-name testSessionName

   unset AWS_ACCESS_KEY_ID
   unset AWS_SECRET_ACCESS_KEY
   unset AWS_SESSION_TOKEN

   aws sts assume-role --role-arn arn:aws:iam::301570629804:role/testhamidaffansync --role-session-name testSessionName1

   export AWS_ACCESS_KEY_ID=NEW_TEMP_ACCESS_KEY_ID
   export AWS_SECRET_ACCESS_KEY=NEW_TEMP_SECRET_ACCESS_KEY
   export AWS_SESSION_TOKEN=NEW_TEMP_SESSION_TOKEN

# Steps to deploy Lambda Function Code to AWS Lambda

   zip function.zip lambda_function.py

   aws lambda create-function --function-name your-function-name \
   --zip-file fileb://function.zip --handler lambda_function.lambda_handler \
   --runtime python3.8 --role your-iam-role-arn --region us-east-1

Modify the function name to AffanThamidServerlessChatProject
Modify the role to arn:aws:iam::954976328760:role/Affan_Thamid_ServerlessChat_Project
Modify the region to us-east-1
```
   aws lambda create-function --function-name AffanThamidServerlessChatProject \
   --zip-file fileb://function.zip --handler lambda_function.lambda_handler \
   --runtime python3.8 --role arn:aws:iam::954976328760:role/Affan_Thamid_ServerlessChat_Project --region us-east-1
```

Modify the function name to AffanThamidServerlessChatProject
Modify the region to us-east-1
```
   aws lambda update-function-code --function-name AffanThamidServerlessChatProject \
   --zip-file fileb://function.zip --region us-east-1

   aws lambda invoke --function-name AffanThamidServerlessChatProject \
   --payload '{"httpMethod": "GET"}' response.json \
   --cli-binary-format raw-in-base64-out --region us-east-1

   aws lambda invoke --function-name AffanThamidServerlessChatProject \
   --payload '{"httpMethod": "POST"}' response.json \
   --cli-binary-format raw-in-base64-out --region us-east-1

   aws lambda delete-function --function-name AffanThamidServerlessChatProject --region us-east-1
```

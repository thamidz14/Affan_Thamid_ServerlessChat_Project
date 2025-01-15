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

# Step 4: Implement Lambda Functions
   
1. Create handler.js: Implement the logic for creating and retrieving messages.

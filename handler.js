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

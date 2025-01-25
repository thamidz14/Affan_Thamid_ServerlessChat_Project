# To Add Files To a Repository:
```
git add serverless.yml
git commit -m "Added serverless.yml"
git push origin main
```
```
git add CLI-Commands.md
git commit -m "Added CLI-Commands.md"
git push origin main
```

Merge / Rebase
```
git pull --no-rebase
git pull --rebase
git pull --ff-only
aws s3 cp index.html s3://thamidaffan-bucket/index.html

git push -u origin main
git fetch origin

```
# To Set Up Development Environment

**Mac Users**
```
Download and install fnm: curl -o- https://fnm.vercel.app/install | bash
Download and install Node.js: fnm install 23
Verify the Node.js version: node -v # Should print "v23.6.0".
Verify npm version: npm -v # Should print "10.9.2".

```
**Windows Users**
```
Download and install fnm: winget install Schniz.fnm
Download and install Node.js: fnm install 22
Verify the Node.js version: node -v # Should print "v22.13.0".
Verify npm version: npm -v # Should print "10.9.2".
```
```
aws lambda invoke --function-name your-function-name1 --payload '{"httpMethod": "GET"}' response.json --cli-binary-format raw-in-base64-out --region us-east-1

aws lambda add-permission --function-name <your function name> --statement-id APIGatewayInvokePermission --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:us-east-1:<your_account_id>:<api-id>/*/POST/chat

aws lambda add-permission --function-name your-function-name1 --statement-id APIGatewayInvokePermission94 --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:us-east-1:954976328760:26pp853315/*/POST/chat

aws lambda add-permission --function-name your-function-name1 --statement-id APIGatewayInvokePermission94 --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:us-east-1:954976328760:26pp853315/*/GET/chat
```

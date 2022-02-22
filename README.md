<h1>Dining Concierge Assistant </h1>
Customer Service is a core service for a lot of businesses around the world
and it is getting disrupted at the moment by Natural Language Processing-
powered applications. In this first assignment you will implement a
serverless, microservice-driven web application. Specifically, you will
build a Dining Concierge chatbot that sends you restaurant suggestions given
a set of preferences that you provide the chatbot with through conversation.

<h3>In this project, I have followed several steps:</h3>
<ol>
  <li>Build and deploy the frontend of the application in an AWS S3 bucket</li>  
  <li>Use API Gateway to setup thr API swagger file and create a Lambda function 0 to communicate with the frontend</li>
  <li>Build a Dining Concierge chatbot using Amazon Lex</li>
  <li>Use the Yelp API to collect 5,000+ random restaurants from Manhattan. Store the restaurants in DynamoDB </li>
  <li>Create an ElasticSearch instance using the AWS ElasticSearch Service.</li> 
  <li>Create a new Lambda function (LF2) that acts as a queue worker. Whenever it is invoked it 1. pulls a message from the SQS queue (Q1) 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and DynamoDB, 3. formats them and 4. sends them over text message to the phone number included in the SQS message, using SNS and set up a CloudWatch event trigger that runs every minute </li>  
</ol>



<img width="721" alt="image" src="https://user-images.githubusercontent.com/90934485/155042098-5b2e4848-30cf-48be-9fdc-c57e1dae9716.png">

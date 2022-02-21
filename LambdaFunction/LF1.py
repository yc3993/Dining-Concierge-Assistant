import json
import boto3
import logging


def send_sqs_message(QueueName, MessageAttributes):
    """

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    QueueName = 'sqs'

    sqs_client = boto3.client('sqs')
    sqs_queue_url = sqs_client.get_queue_url(
        QueueName=QueueName)['QueueUrl']

    msg = sqs_client.send_message(QueueUrl=sqs_queue_url, DelaySeconds=10, MessageAttributes=MessageAttributes,
                                  MessageBody=('Information about user preferred restaurant.'))

    return msg


def lambda_handler(event, context):
    # TODO implement

    City = event["currentIntent"]["slots"]["City"]
    Cuisine = event["currentIntent"]["slots"]["Cuisine"]
    Date = event["currentIntent"]["slots"]["Date"]
    Num = event["currentIntent"]["slots"]["Num"]
    Phone = event["currentIntent"]["slots"]["Phone"]
    Time = event["currentIntent"]["slots"]["Time"]
    Zip = event["currentIntent"]["slots"]["Zip"]

    MessageAttributes = {
        'City': {
            'DataType': 'String',
            'StringValue': City
        },
        'Cuisine': {
            'DataType': 'String',
            'StringValue': Cuisine
        },
        'NumberOfAttendence': {
            'DataType': 'String',
            'StringValue': Num
        },
        'Date': {
            'DataType': 'String',
            'StringValue': Date
        },
        'Time': {
            'DataType': 'String',
            'StringValue': Time
        },
        'PhoneNumber': {
            'DataType': 'String',
            'StringValue': Phone
        },
        'Zip': {
            'DataType': 'String',
            'StringValue': Zip
        },
    }

    QueueName = 'sqs'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Send some SQS messages

    msg = send_sqs_message(QueueName, MessageAttributes)
    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

    response = {
        "dialogAction":
            {"type": "Close",
             "fulfillmentState": "Fulfilled",
             "message": {
                 "contentType": "PlainText",
                 "content": "You’re all set. Expect my suggestions shortly! Have a good day."
             }
             }
    };
    return response


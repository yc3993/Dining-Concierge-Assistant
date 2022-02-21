import json
import boto3
from botocore.exceptions import ClientError
import requests
from requests_aws4auth import AWS4Auth


def lookup_es(cuisine):
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://search-restaurants-fqptc3egov4fgxc4bdyy4qzt44.us-east-1.es.amazonaws.com'
    index = cuisine
    url = host + '/' + index + '/_search'
    query = {
        "size": 3,
        "query": {
            "multi_match": {
                "query": index,
                "fields": ["_index"]
            }
        }
    }
    headers = { "Content-Type": "application/json" }

    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    response['body'] = r.text
    return response


def lookup_dynamo(key, table='yelp'):
    db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        return response['Item']


def get_data(queue_url):
    sqs = boto3.client('sqs')

    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return message

def lambda_handler(event, context):

    # get from sqs
    message = get_data('https://sqs.us-east-1.amazonaws.com/415613607679/Restaurants')
    city = message['MessageAttributes']['City']['StringValue']
    cuisine = message['MessageAttributes']['Cuisine']['StringValue'].lower()
    date = message['MessageAttributes']['Date']['StringValue']
    email = message['MessageAttributes']['Email']['StringValue']
    num = message['MessageAttributes']['NumberOfAttendence']['StringValue']
    time = message['MessageAttributes']['Time']['StringValue']


    # get from elastic search
    id = []
    data = lookup_es(cuisine)

    for item in json.loads(data["body"])["hits"]["hits"]:
        id.append(item["_source"]["restaurant_id"])


    # get from dynamo
    name = []
    address = []
    for i in id:
        info = lookup_dynamo({'restaurant_id':i})
        name.append(info['name'])
        address.append(info['address'])

    #send email
    SENDER = "Dining Concierge Assistant <rz41314131@gmail.com>"

    RECIPIENT = email

    CONFIGURATION_SET = "ConfigSet"

    AWS_REGION = "us-east-1"

    SUBJECT = "YOUR PERSONALIZED RESTAURANT SUGGESTIONS"

    BODY_TEXT = ("")

    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>YOUR PERSONALIZED RESTAURANT SUGGESTIONS</h1>
      <p>Hello! Here are my {} restaurant suggestions for {} people, for {}
      at {}: 1. {}, located at {} 2. {}, located at {} 3. {}, located at {}.
      </p>
    </body>
    </html>
            """.format(cuisine,num,date,time,name[0],address[0],name[1],address[1],name[2],address[2])

    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,

        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


    return

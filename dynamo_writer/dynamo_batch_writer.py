import boto3
import csv
import json


def lambda_handler(event):
    region = 'us-east-1'
    record_list = []

    try:
        s3 = boto3.client('s3')

        dynamodb = boto3.client('dynamodb', region_name=region)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print('Bucket', bucket, 'key', key)

        csv_file = s3.get_object(Bucket=bucket, Key=key)
        print(0)

        record_list = csv_file['Body'].read().decode('utf-8').split('\n')

        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"')

        for row in csv_reader:
            resid = row[0]
            name = row[1]
            restaurant_type = row[2]
            address = row[3]
            num_of_reviews = row[4]
            rating = row[5]
            zip_code = row[6]
            lati = row[7]
            longi = row[8]
            # print('RestaurantID: ', resid)
            add_to_db = dynamodb.put_item(
                TableName='yelp-restaurants',
                Item={
                    'resid': {'S': str(resid)},
                    'name': {'S': str(name)},
                    'restaurant_type': {'S': str(restaurant_type)},
                    'address': {'S': str(address)},
                    'num_of_reviews': {'S': str(num_of_reviews)},
                    'rating': {'S': str(rating)},
                    'zip_code': {'S': str(zip_code)},
                    'lati': {'S': str(lati)},
                    'longi': {'S': str(longi)}
                })
            print('Success!')




    except Exception as e:
        print(str(e))
event={
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "testcytcyt",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::example-bucket"
        },
        "object": {
          "key": "restaurant.csv",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}
lambda_handler(event,)
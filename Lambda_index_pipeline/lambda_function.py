import json
import boto3
import requests
from datetime import datetime


def lambda_handler(event, context):
    
    un = 'anil'
    pw = 'NYUBatman71!'
    
    bucket=event['Records'][0]['s3']['bucket']['name']

    key = event['Records'][0]['s3']['object']['key']

    
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket': bucket,'Name': key}}, MaxLabels=10)

    labels = []
    for i in response['Labels']:
        labels.append(i['Name'])
    
    index={'objectKey':key, 'bucket':bucket, 'createdTimeStamp':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'labels':labels}
    print(index)
    host = 'https://search-photos-ao5sabg6eempm4zwt5lse4zljy.us-east-1.es.amazonaws.com'
    path = '/photos/Photo/'
    url = host + path
    r = requests.post(url, auth=(un,pw), json=index)
        
    print('success')
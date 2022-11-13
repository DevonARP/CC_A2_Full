import boto3
import json
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
        
aws_access_key_id = '' 
aws_secret_access_key = ''

def lambda_handler(event, context):
    
    print(event)
    message = event["queryStringParameters"]["q"]
    print(message)
    client = boto3.client('lex-runtime')
    botName = "SearchQueries"
    botAlias = "SeaA"
    userId = "User"
    response = client.post_text(botName = botName, botAlias = botAlias, userId = userId, inputText = message)
    primary = response['slots']['Primary']
    secondary = response['slots']['Secondary']

    host = 'search-photos-ao5sabg6eempm4zwt5lse4zljy.us-east-1.es.amazonaws.com' #I spent too much time not realizing the https:// is the problem
    path = '/photos/Photo/'
    region = 'us-east-1'
    service= 'es'
    session = boto3.Session(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, service)
    client = OpenSearch(hosts = [{'host': host, 'port': 443}], http_auth = awsauth, use_ssl = True, verify_certs = True, connection_class = RequestsHttpConnection)

    names = []
    if secondary:
        query = client.search(index="photos", 
                        body = {
                        "query":{
                            "bool":{
                                "must": [
                                    {
                                        "match" : {
                                            "labels": primary
                                        }
                                    }
                                ],
                                "should" : [
                                    {
                                        "match" : {
                                            "labels": secondary
                                        }
                                    }
                                ]}}})

        hits=query['hits']['hits']
        names = []
        for i in hits:
            names.append('https://b2a2.s3.amazonaws.com/' + i['_source']['objectKey'])

        print(primary + ' and ' + secondary)
        print(names)
        return{
            'statusCode': 200,
            'body': json.dumps({
                'text':names
            })
        }
    else:
        query = client.search(index="photos", 
                        body = {
                        "query":{
                            "match" : {
                                "labels": primary
                            }
                        }})

        hits=query['hits']['hits']
        names = []
        for i in hits:
            names.append('https://b2a2.s3.amazonaws.com/' + i['_source']['objectKey'])

        print(primary)
        print(names)
        return{
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'text':names
            })
        }
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
# Access your table using the resource
table = dynamodb.Table('Avis')

def getItemFromTableAndID(nameTable, key):
    table = dynamodb.Table(nameTable)
    response = table.get_item(Key=key)
    print(response)

def getItemFromTableAndIndex(nameTable, index, value):
    table = dynamodb.Table(nameTable)
    resp = table.query(
        # Add the name of the index you want to use in your query.
        IndexName=index,
        KeyConditionExpression=Key(index).eq(value),
    )
    print(resp)
    
    
getItemFromTableAndID('Avis', {'idAvis' : 0})
getItemFromTableAndIndex('Avis', 'idArtisan', 0)
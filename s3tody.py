import boto3
import uuid
import datetime

from datetime import datetime

s3_client = boto3.client("s3")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('s3-csv')

def check_date(sale_date):
    try:
        res = bool(datetime.strptime(sale_date, "%d-%b-%y"))
    except ValueError:
        res = False
    return "Valid" if res == True else "Invalid"

def lambda_handler(event,context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    sales = data.split("\n")
    del sales[0]
    for sale in sales:
        print(sale)
        sale_data = sale.split(",")
        try:
            table.put_item(
            Item = {
                "uuid": str(uuid.uuid1()),
                "SaleDate" : sale_data[0],
                "Saleitem" : sale_data[1],
                "Country" : sale_data[2],
                "Quantity" : sale_data[3],
                "FileName": s3_file_name,
                "Status": check_date(sale_data[0])
                }
            )
        except Exception as e:
            print(e)



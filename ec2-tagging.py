import json
import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='us-east-2')
    response = ec2_client.describe_instances()
    instances = response['Reservations']
    
    instance_ids = []
    for i in range(len(instances[0])):
        print(instances[0]['Instances'][i]['Tags'][0]['Key'])
        #print(instances[0]['Instances'][i]['KeyName'], instances[0]['Instances'][i]['InstanceId'])
        # if instances[0]['Instances'][i]['Tags'][0]['Key'] == 'Name':
        #     instance_ids.append(instances[0]['Instances'][i]['InstanceId'])

    # response = ec2_client.create_tags(
    # Resources = instance_ids,
    # Tags=[
    #     {
    #         'Key': 'Name',
    #         'Value': 'Instance'
    #     },
    # ])
    # print(instance_ids)

lambda_handler('','null')
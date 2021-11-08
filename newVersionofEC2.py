import boto3
import json
import csv
import os
def analyse(response):
    ec2_list = []
    ec2_dict = {}
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    arn = boto3.client('sts').get_caller_identity().get('Arn')
    for reservation in (response['Reservations']):
        instance = reservation['Instances'][0]
        tags = instance['Tags']
        xxx_flag=False
        for tag in tags:
            if tag['Key']=="Name":
                instance_name = tag['Value']
            if tag['Key']=="Env":
                xxx_tag = tag['Key']
                current_value = tag['Value']
                xxx_flag=True
        
        if xxx_flag:
            ec2_dict['Account ID'] = account_id
            ec2_dict["Instance ID"] = instance['InstanceId']
            ec2_dict["Instance Name"] = instance_name
            ec2_dict["xxx Tag"] = xxx_tag
            ec2_dict["Current Value"] = current_value
            ec2_dict["New Value"] = ""
            print(ec2_dict)
        
        if bool(ec2_dict):
            ec2_list.append(ec2_dict)
            ec2_dict = {}
    
    return ec2_list
        
def write_csv(instances, file_name):
    keys = instances[0].keys()
    with open('/tmp/' + file_name , 'w') as out:
        dict_writer = csv.DictWriter(out, keys)
        dict_writer.writeheader()
        dict_writer.writerows(instances)
def write_to_s3(bucket_name, file_name):
    s3=boto3.client('s3')
    with open('/tmp/' + file_name, 'rb') as f:
        s3.upload_fileobj(f,bucket_name, file_name)
def lambda_handler(event, context):
    bucket_name = 'myawesomebucketcoolname123'
    file_name = 'ec2_instance.csv'
    ec2 = boto3.client("ec2")
    
    response = ec2.describe_instances()
    instances = analyse(response)
    write_csv(instances, file_name)
    write_to_s3(bucket_name, file_name)
    return instances
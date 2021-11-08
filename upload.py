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
            if tag['Key']=="Demo":
                xxx_tag= tag['Key']
                current_value = tag['Value']
                xxx_flag=True
        
        if xxx_flag:
            ec2_dict['Account ID'] = account_id
            ec2_dict["Instance ID"] = instance['InstanceId']
            ec2_dict["Instance Name"] = instance_name
            ec2_dict["xxx Tag"] = xxx_tag
            ec2_dict["Current Value"] = current_value
            ec2_dict["New Value"] = ""
        
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
def read_from_s3(bucket_name, file_name):
    s3=boto3.client('s3')
    csv_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    csv_list = csv_string.split("\r\n")
    headers, data = csv_list[0].split(","), csv_list[1:-1]
    data = {j:{headers[i]:data[j].split(",")[i] for i in range(len(headers))} for j in range(len(data))}
    return data
def update_ec2_tags(ec2, input_dict):
    print(input_dict)
    response = ec2.create_tags(Resources=[input_dict['Instance ID']], Tags=[{'Key':input_dict['xxx Tag'], 'Value':input_dict['New Value']}])
    if response['ResponseMetadata']['HTTPStatusCode']==200:
        return "Update successful for {}".format(input_dict['Instance Name'])
    else:
        return "Update not successful for {}. Reason - ".format(input_dict['Instance Name'],response['ResponseMetadata']['HTTPStatusCode'])
    
def lambda_handler(event, context):
    
    bucket_name = 'myawesomebucketcoolname'
    file_name = 'ec2_instance.csv'
    
    if "AWS_REGION" in os.environ:
        ec2 = boto3.client("ec2", region_name=os.environ["AWS_REGION"])
    else:
        ec2 = boto3.client("ec2")
    
    csv_input = read_from_s3(bucket_name,file_name)
    for _ in csv_input:
        print(update_ec2_tags(ec2, csv_input[_]))
    
    response = ec2.describe_instances()
    instances = analyse(response)
    write_csv(instances, file_name)
    write_to_s3(bucket_name, file_name)
    return instances
import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    # Filtering ec2 instances by Tags name and value
    for instance in ec2.instances.all():
      for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == 'Else':
          ec2.create_tags(
            Resources = [instance.id],
            Tags=[{
                    'Key': 'Name',
                    'Value': 'Else2'
                },]
            )

lambda_handler('', '')
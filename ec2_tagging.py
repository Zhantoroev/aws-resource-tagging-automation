import json
import boto3



def create_tags(key, value):
    ec2 = boto3.resource('ec2')
    instance_ids = []

    # Filtering ec2 instances by Tags name and value
    for instance in ec2.instances.all():
      for tag in instance.tags:
        if tag['Key'] == 'Env' and 'SmthElse' in tag['Value']:
          instance_ids.append(instance.id)

    # Creating tags
    if len(instance_ids) >= 1:        # Checking for mathing instances
        ec2.create_tags(
        Resources = instance_ids,
        Tags=[{
                'Key': 'Env',
                'Value': 'Dev'
              },
              
              ]
        )
    print(instance_ids)

lambda_handler('', '')
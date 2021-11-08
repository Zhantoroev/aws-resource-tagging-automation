import boto3

s3_client = boto3.client('s3', region_name='us-east-1',)
s3_client.get_object_tagging(
    Bucket='myawesomebucketcoolname12',
    Key='tmp',
)

s3_client.put_object_tagging(
    Bucket='your-bucket-name',
    Key='tmp',    
    Tagging={
        'TagSet': [
            {
                'Key': 'tag-key',
                'Value': 'tag-value'
            },
        ]
    }
)
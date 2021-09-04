import os
import boto3
import wget
from botocore.exceptions import ClientError


def build_fileurl(bucket_name,region,folder,filename):
    url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{folder}{filename}"
    return url

def upload_to_s3(from_url,id_key,access_secret,bucket_name,region,folder):

    filename = wget.download(from_url)
    print(filename)

    client_s3 =  boto3.client(
        's3',
        aws_access_key_id = id_key,
        aws_secret_access_key = access_secret 
    )

    data_file_folder= os.getcwd()

    try:
        print('uploading '+ filename +' to bucket')
        client_s3.upload_file(
            os.path.join(data_file_folder,filename),
            bucket_name,
            filename
        )
    except ClientError as e:
        print('credentials incorrect')
        print(e)
        return e
    except Exception as e:
        print(e)
        return e
    
    return build_fileurl(bucket_name,region,folder,filename)
    





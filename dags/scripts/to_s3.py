import datetime
import boto3
import os
import json


def load_aws_credentials():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    config_folder = os.path.join(script_folder, 'config')
    aws_config_path = os.path.join(config_folder, 'aws_config.json')

    with open(aws_config_path, 'r') as aws_config_file:
        aws_credentials = json.load(aws_config_file)
        return aws_credentials


def upload_to_s3():
    aws_credentials = load_aws_credentials()
    s3 = boto3.client('s3', aws_access_key_id=aws_credentials['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=aws_credentials['AWS_SECRET_ACCESS_KEY'])

    filename = f"flight_data_{datetime.datetime.now().strftime('%Y_%m_%d')}.json"

    with open(filename, 'rb') as file:
        s3.upload_fileobj(file, 'data_lake', filename)


if __name__ == "__main__":
    upload_to_s3()
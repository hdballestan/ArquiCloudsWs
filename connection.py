import boto3
import environment as E

sns_client = boto3.client("sns", aws_access_key_id=E.AWS_ACCESS_KEY_ID_, 
             aws_secret_access_key=E.AWS_SECRET_ACCESS_KEY_,
             region_name=E.REGION_)

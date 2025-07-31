import boto3
from pprint import pprint
from datetime import datetime
import json
import pandas as pd
import uuid
import os

# ingestion_bucket = os.getenv("S3_INGESTION_BUCKET")#os.environ["S3_INGESTION_BUCKET"]
# transform_bucket = os.getenv("S3_TRANSFORM_BUCKET")

ingestion_bucket = "tfl-extract-bucket"
transform_bucket = "tfl-transform-bucket"

def get_s3_client():
    s3_client = boto3.client("s3")
    return s3_client


def get_latest_s3_object(s3_client, obj_key, bucket):
    
    s3_obj = s3_client.get_object(Bucket = ingestion_bucket, Key = obj_key)
   
    s3_obj_bytes = s3_obj["Body"].read()
    s3_obj_dict = json.loads(s3_obj_bytes.decode('utf-8'))
    return s3_obj_dict


def convert_s3_obj_to_df(obj):
    
    df = pd.DataFrame(obj)
    return df   
    

def create_fact_line_status(df):
    #data = convert_s3_obj_to_df()
    data_copy = df.copy()
    
    fact_line = data_copy.drop(columns=["modified","time_created","line_mode","line_id"])
        
    dim_line = create_dim_line()
    dim_time = create_dim_time()
    status_id = uuid.uuid4()
    fact_line["status_id"] = status_id
    fact_line["line_id"] = dim_line["line_id"]
    fact_line["time_id"] = dim_time["time_id"]
    
    
def create_dim_time(df):
    #data = convert_s3_obj_to_df()
    data_copy = df.copy()
    
    dim_time = data_copy.drop(columns=["line_id","line_mode","status_severity","status_severity_description","time_created","reason"])
    
    dim_time = dim_time.rename(columns={"modified":"time_id"})
    dim_time["time_id"] = pd.to_datetime(dim_time["time_id"])
    
    dim_time['date'] = dim_time['time_id'].dt.date
    dim_time["date"] = pd.to_datetime(dim_time["date"])

    dim_time['time'] = dim_time['time_id'].dt.time
    dim_time["day_of_week"] = dim_time['time_id'].dt.day_name()
    
    
    dim_time["time_id"] = dim_time["time_id"].astype(str)
    
    
    return dim_time    

def create_dim_line(df):
    #data = convert_s3_obj_to_df()
    data_copy = df.copy()
    dim_line = data_copy.drop(columns=["modified", "status_severity","status_severity_description","time_created","reason"])
    dim_line["line_name"] = dim_line["line_id"]
    
    return dim_line


if __name__ == '__main__':
    print(ingestion_bucket)
    print(transform_bucket)
    # api_status = fetch_tfl_status()
    # extracted_status = extract_tfl_status(api_status)
    # #pprint(extracted_status)
   
    # client = get_s3_client()
    # s3_obj_list = get_s3_extract_objects_list(client)
    # latest_key = fetch_latest_s3_object_key(s3_obj_list)
    # latest_s3_status = get_latest_s3_object(client, latest_key, bucket)
    # uploaded_status = upload_latest_status_to_s3(extracted_status, latest_s3_status)
    # #print(uploaded_status)
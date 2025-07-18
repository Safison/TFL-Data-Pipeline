import boto3
from pprint import pprint
from datetime import datetime
import json
import pandas as pd

def get_s3_extract_objects_list():
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket='tfl-extract-bucket')
    return response

def fetch_latest_s3_object_key():
    response = get_s3_extract_objects_list()
    raw_response = response.get("Contents",[])
    object_timestamp_list = []
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    for i in range(len(raw_response)):
        object_key = raw_response[i]["Key"]
        short_key = object_key[:26]
        object_key_date = object_key[:10]
        object_key_time = object_key[11:19]
        key_timestamp = datetime_object = datetime.strptime(short_key, date_format)
        object_timestamp_list.append(key_timestamp)
    max_timestamp = max(object_timestamp_list)
    object_key = str(max_timestamp) + '_tfl_lines_status.json'
    return object_key

def get_latest_s3_object():
    object_key = fetch_latest_s3_object_key()
    s3_client = boto3.client('s3')
    s3_obj = s3_client.get_object(Bucket = 'tfl-extract-bucket', Key = object_key)
    
    s3_obj_bytes = s3_obj["Body"].read()
    s3_obj_dict = json.loads(s3_obj_bytes.decode('utf-8'))
    return s3_obj_dict


def convert_s3_obj_to_df():
    data = get_latest_s3_object()
    df = pd.DataFrame(data)
    #print(df.head())
    return df   
    

def create_fact_line_status():
    pass

def create_dim_time():
    data = convert_s3_obj_to_df()
    data_copy = data.copy()
    time_id = data_copy["modified"].head()
    print(type(time_id))
    #print(time_id)
    
    

def create_dim_line():
    data = convert_s3_obj_to_df()
    data_copy = data.copy()
    dim_line = data_copy.drop(columns=["modified", "status_severity","status_severity_description","time_created","reason"])
    dim_line["line_name"] = dim_line["line_id"]
    
    #print(dim_line.head())
    


#convert_s3_obj_to_df()
create_dim_time()


#get_latest_s3_object()
#'Key': '2025-07-14 10:37:53.526180_tfl_lines_status.json'

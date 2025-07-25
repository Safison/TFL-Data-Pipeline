import requests
from datetime import datetime, timezone
from pprint import pprint
import boto3
import json
import sys

sys.path.append("src/src_extract")
tfl_api = "https://api.tfl.gov.uk/Line/Mode/tube,dlr,overground,elizabeth-line/Status"
bucket_name = "tfl-extract-bucket"

'''
    1 - fetch api tfl line status
    2 - extract api status
    3 - get maximum fromDate, toDate, modified from api status 
    4 - fetch s3 latest status
    5 - get maximum fromDate, toDate, modified from s3 status 
    6 - compare fromDate, toDate, modified in api status with s3 status:
        if one of api status values > s3 status values:
        
            upload api status to s3
            return api status list of dicts
        else
            return false
'''

def fetch_tfl_status():
    tfl_status = requests.get(url=tfl_api)
    dict_tfl_status = tfl_status.json()
    #pprint(dict_tfl_status)
    return dict_tfl_status
    
def extract_tfl_status(tfl_status):
   
    line_list = []
    line_dict = {}

    for line in tfl_status:
        line_dict["line_id"] = line["id"]
        line_dict["line_mode"] = line["modeName"]
        line_dict["modified"] = line["modified"]
        line_status = line.get("lineStatuses")
       
        for status in line_status:
            line_dict["status_severity"] = status.get("statusSeverity","null")
            line_dict["status_severity_description"] = status.get("statusSeverityDescription","null")
            line_dict["time_created"] = status.get("created","null")
            line_dict["reason"] = status.get("reason",'null')
            validity_periods = status.get("validityPeriods","null")
        
            if line_dict["reason"] != 'null':
                for period in validity_periods:
                    line_dict["fromDate"] = period["fromDate"]
                    line_dict["toDate"] = period["toDate"]
                    line_dict["isNow"] = period["isNow"]
                  
            line_list.append(dict(line_dict))
    #pprint(line_list)
    return line_list
   
def get_s3_client():
    s3_client = boto3.client("s3")
    return s3_client

def get_s3_extract_objects_list(s3_client):
   
    response = s3_client.list_objects_v2(Bucket='tfl-extract-bucket')
    return response

def fetch_latest_s3_object_key(response):
   
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

def get_latest_s3_object(s3_client, obj_key, bucket):
    
    s3_obj = s3_client.get_object(Bucket = bucket, Key = obj_key)
   
    s3_obj_bytes = s3_obj["Body"].read()
    s3_obj_dict = json.loads(s3_obj_bytes.decode('utf-8'))
    return s3_obj_dict

    
def upload_latest_status_to_s3(api_status, s3_status):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    modified_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    
    latest_from_date = datetime(1900, 1, 1)
    latest_to_date = datetime(1900, 1, 1)
    latest_modified_date = datetime(1900, 1, 1)

    for i in range(len(api_status)):
        from_date_str = api_status[i].get("fromDate")
        to_date_str = api_status[i].get("toDate")
        modified_date_str = api_status[i].get("modified")
        if from_date_str:
            from_date_date = datetime.strptime(from_date_str, date_format)
            if from_date_date > latest_from_date:
                latest_from_date = from_date_date
        if to_date_str:
            to_date_date = datetime.strptime(to_date_str, date_format)
            if to_date_date > latest_to_date:
                latest_to_date = to_date_date
        if modified_date_str:
            modifed_date_date = datetime.strptime(modified_date_str, modified_format)
            if modifed_date_date > latest_modified_date:
                latest_modified_date = modifed_date_date
    
    
    # print(latest_from_date)
    # print(latest_to_date)
    # print(latest_modified_date)
    
    
def upload_tfl_status_to_s3(status, bucket_name=bucket_name):
    file_name = f'{datetime.now()}_tfl_lines_status.json'
    file_content = json.dumps(status) + "\n"
    s3_client = boto3.client("s3")
    s3_client.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
    
   
if __name__ == '__main__':
    api_status = fetch_tfl_status()
    extracted_status = extract_tfl_status(api_status)
   
    client = get_s3_client()
    s3_obj_list = get_s3_extract_objects_list(client)
    latest_key = fetch_latest_s3_object_key(s3_obj_list)
    latest_s3_status = get_latest_s3_object(client, latest_key, bucket_name)
    uploaded_status = upload_latest_status_to_s3(extracted_status, latest_s3_status)
   
 
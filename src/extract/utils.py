import requests
from datetime import datetime
from pprint import pprint
import boto3
import json

tfl_api = "https://api.tfl.gov.uk/Line/Mode/tube,dlr,overground,elizabeth-line/Status"

def fetch_tfl_status():
    tfl_status = requests.get(url=tfl_api)
    dict_tfl_status = tfl_status.json()
    return dict_tfl_status
    

def extract_tfl_status():
    line_list = []
    line_dict = {}

    general_tfl_status = fetch_tfl_status()
    
   
    for line in general_tfl_status:
        line_id = line["id"]
        line_mode = line["modeName"]
        modified = line["modified"]
        line_status = line["lineStatuses"]
        line_dict["line_id"] = line_id
        line_dict["line_mode"] = line_mode
        line_dict["modified"] = modified
        
        for status in line_status:
            status_severity = status.get("statusSeverity")
            status_severity_description = status.get("statusSeverityDescription")
            time_created = status.get("created")
           
            reason = status.get("reason",'null')
            line_dict["status_severity"] = status_severity
            line_dict["status_severity_description"] = status_severity_description
            line_dict["time_created"] = time_created
          
            
            line_dict["reason"] = reason
          
            line_list.append(dict(line_dict))
   
    return line_list
   


def upload_tfl_status_to_s3(status, bucket_name):
    file_name = f'{datetime.now()}_tfl_lines_status.json'
    s3_client = boto3.client("s3")
    s3_client.put_object(Body=status, Bucket=bucket_name, Key=file_name)
    return file_name
   



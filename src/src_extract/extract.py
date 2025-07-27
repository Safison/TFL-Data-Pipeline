import os
from datetime import datetime
from pprint import pprint
from utils import *
import sys

sys.path.append("src/src_extract")
bucket_name = "tfl-extract-bucket"

def lambda_handler(event, context,bucket_name=bucket_name):
    # dict_tfl_status = fetch_tfl_status()
    # line_status_list = extract_tfl_status(dict_tfl_status)
    # upload_status = upload_tfl_status_to_s3(line_status_list)
    api_status = fetch_tfl_status()
    extracted_status = extract_tfl_status(api_status)
    #pprint(extracted_status)
   
    client = get_s3_client()
    s3_obj_list = get_s3_extract_objects_list(client)
    latest_key = fetch_latest_s3_object_key(s3_obj_list)
    latest_s3_status = get_latest_s3_object(client, latest_key, bucket_name)
    uploaded_status = upload_latest_status_to_s3(extracted_status, latest_s3_status)
    return uploaded_status
     
    
    
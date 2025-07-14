import os
from datetime import datetime
from utils import (
    fetch_tfl_status,
    extract_tfl_status,
    upload_tfl_status_to_s3
)
import sys

sys.path.append("src/src_extract")
bucket_name = "tfl-extract-bucket"

def lambda_handler(event, context,bucket_name=bucket_name):
    dict_tfl_status = fetch_tfl_status()
    extrac_tfl_status = extract_tfl_status(dict_tfl_status)
    upload_status = upload_tfl_status_to_s3(extrac_tfl_status)
     
    
    
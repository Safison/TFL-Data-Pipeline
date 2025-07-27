import boto3
from pprint import pprint
from datetime import datetime
import json
import pandas as pd
import uuid


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


create_fact_line_status()
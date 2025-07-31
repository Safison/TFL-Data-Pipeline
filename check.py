import boto3

client = boto3.client("lambda", region_name="us-east-1")

response = client.list_layer_versions(
    LayerName="AWSSDKPandas-Python310"
)

print(response)
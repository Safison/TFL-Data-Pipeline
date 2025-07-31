data "archive_file" "extract_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/extract/function.zip"
  source_dir = "${path.module}/../src/src_extract"
}

data "archive_file" "transform_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/transform/function.zip"
  source_dir = "${path.module}/../src/src_transform"
}

resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "tfl-data-pipeline-code-"
}

resource "aws_s3_object" "lambda_code" {
  for_each = toset([var.extract_lambda, var.transform_lambda])
  bucket   = aws_s3_bucket.code_bucket.bucket
  key      = "${each.key}/function.zip"
  source   = "${path.module}/../packages/${each.key}/function.zip"
  etag     = filemd5("${path.module}/../packages/${each.key}/function.zip")
}


resource "aws_lambda_function" "workflow_extract_lambda" {
  function_name    = var.extract_lambda
  source_code_hash = data.archive_file.extract_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.extract_lambda}/function.zip"
  role             = aws_iam_role.lambda_role.arn
  handler          = "${var.extract_lambda}.lambda_handler"
  runtime          = "python3.10"
  timeout          = var.default_timeout
  layers           = [aws_lambda_layer_version.dependencies.arn]
  depends_on       = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.ingestion_bucket.id
    }
  }
}


resource "aws_s3_object" "lambda_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "layer/layer.zip"
  source = data.archive_file.layer_code.output_path
  # etag   = filemd5(data.archive_file.layer_code.output_path)
  #  depends_on = [ data.archive_file.layer_code ]
}


#added pandas layer from aws layers source to the transform lambda
resource "aws_lambda_function" "transform_lambda" {
  function_name    = var.transform_lambda
  source_code_hash = data.archive_file.transform_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.transform_lambda}/function.zip"
  role             = aws_iam_role.lambda_role.arn
  handler          = "${var.transform_lambda}.lambda_handler"
  runtime          = "python3.10"
  timeout          = var.default_timeout
  layers           = [aws_lambda_layer_version.dependencies.arn, "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python310:25"/*  */]
  depends_on       = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
  environment {
    variables = {
      S3_BUCKET_NAME_INGESTION = aws_s3_bucket.ingestion_bucket.id,
      S3_BUCKET_NAME_TRANSFORMED = aws_s3_bucket.transform_bucket.id
    }
  }
}


# data "aws_lambda_layer_version" "pandas" {
#   layer_name     = "AWSSDKPandas-Python310"
#   version = 25
# }
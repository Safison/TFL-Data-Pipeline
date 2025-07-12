data "archive_file" "extract_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/extract/function.zip"
  source_dir = "${path.module}/../src/src_extract"
}

resource "aws_lambda_function" "workflow_extract_lambda" {
  function_name    = var.extract_lambda
  source_code_hash = data.archive_file.extract_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.extract_lambda}/function.zip"
  role             = aws_iam_role.lambda_role.arn
  handler          = "${var.extract_lambda}.lambda_handler"
  runtime          = "python3.12"
  timeout          = var.default_timeout
  layers           = [aws_lambda_layer_version.dependencies.arn]
  depends_on       = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.ingestion_bucket.id
    }
  }
}

resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "tfl-data-pipeline-code-"
}

resource "aws_s3_object" "lambda_code" {
  for_each = toset([var.extract_lambda])
  bucket   = aws_s3_bucket.code_bucket.bucket
  key      = "${each.key}/function.zip"
  source   = "${path.module}/../packages/${each.key}/function.zip"
  etag     = filemd5("${path.module}/../packages/${each.key}/function.zip")
}

resource "aws_s3_object" "lambda_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "layer/layer.zip"
  source = data.archive_file.layer_code.output_path
  etag   = filemd5(data.archive_file.layer_code.output_path)
  depends_on = [ data.archive_file.layer_code ]
}
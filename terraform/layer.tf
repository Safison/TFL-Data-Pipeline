#install requirements
resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../requirements.txt -t ${path.module}/../dependencies/python"
  }

  triggers = {
    dependencies = filemd5("${path.module}/../requirements.txt")
  }
}

#zip the layer into layer.zip
data "archive_file" "layer_code" {
  type        = "zip"
  output_path = "${path.module}/../packages/layer/layer.zip"
  source_dir  = "${path.module}/../dependencies"
}

#layer version
resource "aws_lambda_layer_version" "dependencies" {
  layer_name = "requests_library_layer"
  s3_bucket  = aws_s3_object.lambda_layer.bucket
  s3_key     = aws_s3_object.lambda_layer.key
}

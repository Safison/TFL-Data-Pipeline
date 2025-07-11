resource "aws_s3_bucket" "ingestion_bucket" {
  bucket_prefix = "ingestion-tfl-data-"
}

resource "aws_s3_bucket" "transform_bucket" {
  bucket_prefix = "transfrom-tfl-data-"
}


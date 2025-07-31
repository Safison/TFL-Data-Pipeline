resource "aws_iam_role" "lambda_role" {
  name_prefix        = "role-tfl-lambdas-"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    EOF
}


data "aws_iam_policy_document" "s3_document" {
  statement {

    actions = ["s3:PutObject",
                "s3:Get*",
                "s3:List*",
                "s3:Describe*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"]

    resources = ["${aws_s3_bucket.ingestion_bucket.arn}",
    "${aws_s3_bucket.ingestion_bucket.arn}/*",
        "${aws_s3_bucket.transform_bucket.arn}",
       "${aws_s3_bucket.transform_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "s3_policy" {
  name_prefix = "s3-policy-tfl-lambda-"
  policy      = data.aws_iam_policy_document.s3_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}
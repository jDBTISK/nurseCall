# IAM Role
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role

# lambda を実行するための必要最小限の権限に加えて SNS を利用するための権限を付与
resource "aws_iam_role" "lambda" {
  name               = "LambdaRoleForSNS"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda.json
}

# IAM Policy Document
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document

data "aws_iam_policy_document" "assume_role_lambda" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# IAM Role Policy Attachment
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "sns" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

resource "aws_iam_role_policy_attachment" "ses" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}

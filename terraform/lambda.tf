# Lambda Function
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function

resource "aws_lambda_function" "app" {
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  function_name = "nurseCall"
  description   = "IoT ボタンをナースコール代わりにして SMS 通知を行うための Lambda Function"
  handler       = "main.handler"
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.8"
  timeout       = 60

  environment {
    variables = {
      NOTICE_EMAIL = var.email
    }
  }
}

# https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/archive_file
# Lambda Function のソースコードを zip にする
# ソースに変更があった場合 apply 時に差分扱いとなり新規 zip ファイルが作成される
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../lambda/src"
  output_path = "../lambda/deploy_package.zip"
}

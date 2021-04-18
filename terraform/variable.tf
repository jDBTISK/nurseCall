# .tfvars で定義を外に出したいやつだけ variable で定義
variable "aws_access_key" {}
variable "aws_secret_key" {}

# SES でメール通知を行うメールアドレス
variable "email" {}

# .tfvars に書く必要ないやつは local values
locals {
  # 東京リージョン
  region = "ap-northeast-1"
}

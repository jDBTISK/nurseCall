# AWS on ナースコール

## Overview

`SORACOM LTE-M Button powered by AWS` + `AWS IoT 1-Click` + `AWS Lambda` + `AWS SNS` を用いたナースコールの実装

## Description

`SORACOM LTE-M Button powered by AWS` は[こちら](https://soracom.jp/store/5208/)

この IoT ボタン押下によって `AWS` の `IoT 1-Click` というサービスを経由して `Lambda` を叩くことが出来るので、  
その中で `SNS` の SMS送信機能を使って通知が必要な人間に対して通知を送るだけです。

開発のきかっけが、「祖父に持たせてボタン押すだけで自分と父に通知行けばナースコールボタンの代わりになるんじゃね??」  
と思ったからなのでナースコールと名付けていますが、内容的にはただ「SMS送信ボタン」でしかないです。

## Setup

### 1. terraform 環境変数の設定

`terraform/terraform.tfvars.example` を参考に `terraform/terraform.tfvars` を作ってください。

### 2. terraform 実行

```sh
cd terraform
terraform init # 初回のみ
terraform apply
```

これで

- `IAM Role`
- `Lambda Function`

が作成され、`lambda/src` 直下のソースコードがデプロイされます。  
以降、 `lambda/src` に変更があった場合は `terraform apply` でデプロイ出来ます。

`lambda/.env` はローカルで実行したい場合のみ必要になる(詳細は後述)ので、デプロイ時には必須ではありません。

### 3. SORACOM LTE-M Button powered by AWS の登録

`https://users.soracom.io/ja-jp/guides/iot-devices/lte-m-button-aws/register/`

ここの手順通りに作業する。

### 4. AWS IoT 1-Click プロジェクト作成

1. AWS コンソールから `IoT 1-Click` のページに行き、新規プロジェクト作成
2. 先程作成した `Lambda Function` を紐付け

適当にググったらたぶん詳しい方法が出る！

## Lambda Function

ソースコードの doc コメント部分に書いてあるようなパラメータが `IoT 1-Click` から送られてくるので、  
必要な情報を抜き取って `SNS` による SMS送信を行っているだけのものになります。

### Test

ローカルでテストしたい場合には、 `lambda` ディレクトリ直下で以下の `docker` コマンドで実行出来ます。

本番環境では `function` 自体に `SNS` のロールを与えているのでアクセスキーの指定は不要ですが、  
ローカルでの実行時は `.env` に `SNS` を実行するために必要な権限を持ったアクセスキーを設定しておいてください。

また、 `test` ディレクトリにある `example.json` を参考に、適当なテストパラメータを設定した `json` を用意してください。  
本番環境における `lambda` 実行時の `event` に渡される値になります。

```sh
docker run --rm -v "$PWD"/src:/var/task --env-file .env lambci/lambda:python3.8 main.handler $(printf '%s' $(cat test/1.json))
```
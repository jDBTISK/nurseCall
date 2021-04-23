from datetime import datetime, timedelta
import logging

import boto3


# logging 設定
logger = logging.getLogger(__name__)
log_format = "%(asctime)s [%(levelname)s] %(name)s : %(message)s"
logging.basicConfig(format=log_format)
logging.getLogger(__name__).setLevel(level=logging.DEBUG)

sns = boto3.client("sns")
ses = boto3.client("ses")


def handler(event, context):
    """lambda handler

    Parameters
    ----------
    event : dict
        {
            "deviceInfo": {
                # デバイス識別子
                "deviceId": "XXX",
                "type": "button",
                # 残り充電量
                "remainingLife": 99.9,
                "attributes": {
                    "projectRegion": "ap-northeast-1",
                    "projectName": "cherry",
                    "placementName": "sendSMSPlacement",
                    "deviceTemplateName": "sendSMS"
                }
            },
            "deviceEvent": {
                "buttonClicked": {
                    "clickType": "SINGLE",
                    "reportedTime": "2021-04-12T03:40:41.263Z" # UTC時刻
                }
            },
            "placementInfo": {
                "projectName": "cherry",
                "placementName": "sendSMSPlacement",
                "attributes": {
                    # 送信電話番号(カンマ区切り)
                    "phone_numbers": "+81",
                    # メッセージ本文
                    "body": "",
                    # 送信者
                    "sender": "",
                    # 通知先メールアドレス
                    "email": ""
                },
                "devices": {
                    "sendSMS": "XXX" # デバイス識別子
                }
            }
        }
    context : None

    Returns
    -------
    list[dict]
    """
    logger.debug(f"parameters: {event}")
    attributes = event["placementInfo"]["attributes"]
    phone_numbers = attributes["phone_numbers"].split(",")
    life = event["deviceInfo"]["remainingLife"]

    click_event = event["deviceEvent"]["buttonClicked"]
    click_type = click_event["clickType"]

    # クリック時刻を日本時刻でフォーマット
    click_datetime = click_event["reportedTime"].replace("Z", "")
    utc_time = datetime.fromisoformat(click_datetime)
    jst_time = (utc_time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    # メッセージ本文の作成
    body_lines = [attributes.get("body", "")]
    body_lines += [
        f"ボタンクリック時刻: {jst_time}",
        f"充電残量: {life}",
        f"クリックタイプ: {click_type}"
    ]
    body = "\n".join(body_lines)

    logger.debug(f"phone_numbers: {phone_numbers}")
    logger.debug(f"sender: {attributes['sender']}")
    logger.debug(f"body: {body}")

    res = [
        sns.publish(
            PhoneNumber=phone_number,
            Message=body,
            MessageAttributes={
                "AWS.SNS.SMS.SenderID": {
                    "DataType": "String",
                    # 通知者表示に使用される送信者ID
                    "StringValue": attributes["sender"]
                }
            }
        ) for phone_number in phone_numbers]
    logger.info(res)

    # SMS 送信結構な割合で失敗するので結局メール送信もすることにした
    mail = attributes["email"]
    send_email(mail, mail, body_lines[0], body)
    return res


def send_email(source, to, subject, body):
    """SES を用いたメール送信

    Parameters
    ----------
    source : str
    to : str
    subject : str
    body : str

    Returns
    -------
    dict
    """
    return ses.send_email(
        Source=source,
        Destination={
            "ToAddresses": [to]
        },
        Message={
            "Subject": {
                "Data": "Subject"
            },
            "Body": {
                "Text": {
                    "Data": body
                }
            }
        }
    )

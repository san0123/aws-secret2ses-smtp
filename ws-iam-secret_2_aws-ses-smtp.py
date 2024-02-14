#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
발송자 및 수신자 메일 주소를 입력해야 한다.
"""

from_email = ""
to_email = ""
[root@instance-20220428-0332 ses-smtp]# cat aws-iam-secret_2_aws-ses-smtp.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import hmac
import hashlib
import base64
import argparse
import smtplib
import email.utils
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def smtp_test(frommail, tomail, acckey, seckey, region):
    SENDERNAME = 'PySender'
    SENDER = frommail
    RECIPIENT = tomail
    USERNAME_SMTP = acckey
    PASSWORD_SMTP = seckey
    HOST = "email-smtp." + region + ".amazonaws.com"
    PORT = 587
    print("SMTP: email-smtp." + region + ".amazonaws.com:"+str(PORT))
    print("AUTH: ID="+acckey+"    PW="+seckey)
    print("From: "+SENDER+"    To: "+RECIPIENT)
    SUBJECT = 'AWS SES 메일 테스트'
    BODY_TEXT = """Amazon SES SMTP Email 테스트
현재 이메일은 Amazone SES 를 통해 발송 되었으며 Python 언어의 smtplib 라이브러리를 사용합니다."""
    BODY_HTML = """<html>
<head></head><body>
  <h1>Amazon SES SMTP Email 테스트</h1>
  <p>현재 이메일은 Amazone SES 를 통해 발송 되었으며
    <a href='https://www.python.org/'>Python</a> 언어의
    <a href='https://docs.python.org/3/library/smtplib.html'>smtplib</a> 라이브러리를 사용합니다.
  </p>
</body></html>"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(SUBJECT, 'utf-8')
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    msg.attach(MIMEText(BODY_TEXT, 'plain', 'utf-8'))
    msg.attach(MIMEText(BODY_HTML, 'html', 'utf-8'))
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
        res = "Email sent!"
    except Exception as e:
        res = "Error: " + e
    return res

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def calculate_key(secret_access_key, region):
    SMTP_REGIONS = ['us-east-1', 'us-east-2', 'us-west-2', 'us-gov-west-1', 'sa-east-1',
                    'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-south-1',
                    'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2']
    if region not in SMTP_REGIONS:
        raise ValueError("The "+region+" Region doesn't have an SMTP endpoint.")

    signature = sign(("AWS4" + secret_access_key).encode('utf-8'), "11111111")
    signature = sign(signature, region)
    signature = sign(signature, "ses")
    signature = sign(signature, "aws4_request")
    signature = sign(signature, "SendRawEmail")
    signature_and_version = bytes([0x04]) + signature
    if sys.version_info[0] == 2:
        signature_and_version = '\x04'.encode('utf-8') + signature
    smtp_password = base64.b64encode(signature_and_version)
    return smtp_password.decode('utf-8')

def config_check(fe, te):
    if fe is None or fe == "" or te is None or te == "":
        read = 'N'
    else:
        read = 'ask'
    return read

def main():
    parser = argparse.ArgumentParser(description='AWS IAM Secret Access Key to SMTP password.')
    parser.add_argument('AccessKEY', help='AWS IAM - Access Key ID')
    parser.add_argument('SecretKEY', help='AWS IAM - Secret Access Key')
    parser.add_argument('REGION', help='AWS SES - Region - us-west-2, ap-south-1, etc...')
    args = parser.parse_args()
    seskey = calculate_key(args.SecretKEY, args.REGION)
    print('make SMTP Password complet.')

    print("AWS-SES ID: " + args.AccessKEY)
    print("AWS-SES PW: " + seskey)

    read = config_check(config.from_email, config.to_email)
    if read == 'N':
        pass
    else:
        print('testing send e-mail? (Y/n) ')
        read = str(sys.stdin.readline())
        if read in ('Y\n', 'y\n'):
            print(smtp_test(config.from_email, config.to_email, args.AccessKEY, seskey, args.REGION))

if __name__ == '__main__':
    main()

exit(0)

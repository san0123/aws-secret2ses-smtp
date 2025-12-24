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

def smtp_test(frommail, tomail, acckey, seckey, region, smtpport):
    SENDERNAME = 'PySender'
    SENDER = frommail
    RECIPIENT = tomail
    USERNAME_SMTP = acckey
    PASSWORD_SMTP = seckey
    HOST = f"email-smtp.{region}.amazonaws.com"
    PORT = smtpport
    print(f"\n📡 연결 정보:")
    print(f"   호스트: {HOST}:{PORT}")
    print(f"   인증 ID: {acckey[:8]}***")
    print(f"   발신자: {SENDER}")
    print(f"   수신자: {RECIPIENT}")
    SUBJECT = 'AWS SES 메일 테스트'
    BODY_TEXT = """Amazon SES SMTP Email 테스트
현재 이메일은 Amazon SES 를 통해 발송 되었으며 Python 언어의 smtplib 라이브러리를 사용합니다."""
    BODY_HTML = """<html>
<head></head><body>
  <h1>Amazon SES SMTP Email 테스트</h1>
  <p>현재 이메일은 Amazon SES 를 통해 발송 되었으며
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
        if PORT == 465:
            server = smtplib.SMTP_SSL(HOST, PORT)
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
        elif PORT in [25, 587, 2587]:
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
        else:
            raise ValueError(f"지원되지 않는 포트입니다: {PORT}")
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
        return "✅ 이메일 발송 성공!"
    except smtplib.SMTPAuthenticationError as e:
        return f"❌ 인증 실패: SMTP 자격증명을 확인하세요\n   상세: {str(e)}"
    except smtplib.SMTPRecipientsRefused as e:
        return f"❌ 수신자 거부: 이메일 주소를 확인하세요\n   상세: {str(e)}"
    except smtplib.SMTPConnectError as e:
        return f"❌ 연결 실패: SMTP 서버에 연결할 수 없습니다\n   상세: {str(e)}"
    except Exception as e:
        return f"❌ 연결 오류: {type(e).__name__}: {str(e)}"

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def calculate_key(secret_access_key, region):
    SMTP_REGIONS = ['us-east-1', 'us-west-2', 'us-gov-east-1', 'eu-west-1', 'eu-central-1',
                    'eu-central-2', 'eu-south-1', 'eu-north-1', 'ap-northeast-1', 'ap-northeast-2',
                    'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ap-southeast-3',
                    'ap-south-1', 'ap-south-2', 'me-south-1', 'me-central-1', 'il-central-1', 'af-south-1']
    if region not in SMTP_REGIONS:
        raise ValueError(f"❌ {region} 리전은 SMTP 엔드포인트를 지원하지 않습니다.")
    print("🔄 SMTP 패스워드 변환 중...")
    # AWS SES SMTP 변환용 고정값들
    DATE_STAMP = "11111111"
    SERVICE = "ses"
    REQUEST_TYPE = "aws4_request"
    ALGORITHM = "SendRawEmail"
    signature = sign(("AWS4" + secret_access_key).encode('utf-8'), DATE_STAMP)
    signature = sign(signature, region)
    signature = sign(signature, SERVICE)
    signature = sign(signature, REQUEST_TYPE)
    signature = sign(signature, ALGORITHM)
    signature_and_version = bytes([0x04]) + signature
    if sys.version_info[0] == 2:
        signature_and_version = '\x04'.encode('utf-8') + signature
    smtp_password = base64.b64encode(signature_and_version)
    print("✅ 변환 완료!")
    return smtp_password.decode('utf-8')

def get_email_config(from_email=None, to_email=None):
    """이메일 테스트를 위한 설정 입력받기"""
    print("\n📧 이메일 테스트 설정")
    print("=" * 40)
    if not from_email:
        from_email = input("발신자 이메일 주소: ").strip()
    if not to_email:
        to_email = input("수신자 이메일 주소: ").strip()
    if not from_email or not to_email:
        print("⚠️  이메일 주소가 입력되지 않아 테스트를 건너뜁니다.")
        return None, None
    return from_email, to_email

def main():
    parser = argparse.ArgumentParser(
        description='AWS IAM Secret Access Key를 SES SMTP 패스워드로 변환합니다.',
        epilog="지원 리전:\n  "
        + 'us-east-1, us-west-2, us-gov-east-1, il-central-1, af-south-1,\n  '
        + 'eu-west-1, eu-central-1, eu-central-2, eu-south-1, eu-north-1,\n  '
        + 'ap-northeast-1, ap-northeast-2, ap-northeast-3, ap-south-1, ap-south-2,\n  '
        + 'ap-southeast-1, ap-southeast-2, ap-southeast-3, me-south-1, me-central-1',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('AccessKEY', help='AWS IAM Access Key ID')
    parser.add_argument('SecretKEY', help='AWS IAM Secret Access Key')
    parser.add_argument('REGION', help='AWS 리전 (us-east-1, ap-northeast-2, etc.)')
    parser.add_argument('--from-email', '-f', help='발신자 이메일 (테스트용)')
    parser.add_argument('--to-email', '-t', help='수신자 이메일 (테스트용)')
    parser.add_argument('--no-test', action='store_true', help='테스트 건너뛰기')
    if len(sys.argv) < 4:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    try:
        # 키 변환
        seskey = calculate_key(args.SecretKEY, args.REGION)
        print("\n" + "="*50)
        print("✅ AWS IAM → SES SMTP 변환 완료")
        print("="*50)
        print(f"Access Key ID: {args.AccessKEY}")
        print(f"SMTP Password: \033[33;1m{seskey}\033[0m")
        print("="*50)
        # 테스트 실행
        if not args.no_test:
            from_email = args.from_email
            to_email = args.to_email
            if not from_email or not to_email:
                test_confirm = input("\n📧 이메일 발송 테스트를 하시겠습니까? (Y/n): ").strip()
                if test_confirm.lower() in ('y', 'yes', ''):
                    from_email, to_email = get_email_config(from_email, to_email)
            if from_email and to_email:
                print(f"\n🧪 이메일 테스트 실행 중...")
                result = smtp_test(from_email, to_email, args.AccessKEY, seskey, args.REGION, 587)
                print(f"결과: {result}")
    except ValueError as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 중단되었습니다.")
        sys.exit(0)

if __name__ == '__main__':
    main()

exit(0)
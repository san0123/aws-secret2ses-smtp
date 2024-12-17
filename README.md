# aws-secret2ses-smtp
> make AWS SES SMTP password from AWS-IAM-SecretKey
### 목적
> AWS IAM 에서 발급된 AccessKey, SecretKey 를 입력해서 AWS의 SES(Simply Email Service)에서 사용이 가능한 패스워드(STARTTLS)로 변경한다.
### 클론
> ```bash
> ~]$ git clone https://github.com/san0123/aws-secret2ses-smtp.git
> ```
### 도움말
> ```bash
> ~]$ cd ./aws-secret2ses-smtp
> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py -h
> ```
### 사용 방법
> ```bash
> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py [AccessKEY] [SecretKEY] [REGION]
> ```
### smtp 패스워드 생성 후 메일 발송 테스트
> 사전에 config.py 파일에 발신자 메일 주소 및 수신자 메일 주소를 입력해두면 변환 이후 아래와 같이 발송테스트를 할지 묻는다.
>> ```bash
>> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py AAAAAAAAAAAAAAAAAAAA YOURKEYrrpg/JHpyvtStUVcAV9177EAKKmDP37P us-east-1
>> make SMTP Password complet.
>> AWS-SES ID: AAAAAAAAAAAAAAAAAAAA
>> AWS-SES PW: BNSPZY0jlomEr4Z6voxNGBKDK4qcWk6/DsLPMg466vEX
>> testing send e-mail? (Y/n)
>> ```
# 출처
> AWS 공식 메뉴얼: https://repost.aws/ko/knowledge-center/ses-rotate-smtp-access-keys

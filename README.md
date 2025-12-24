### 목적
> AWS IAM 에서 발급된 AccessKey, SecretKey 를 입력해서 AWS의 SES(Simply Email Service)에서 사용이 가능한 패스워드(STARTTLS)로 변경한다.
> ```text
> SECRETKEY: YOURKEYrrpg/JHpyvctStUVcAV9177EAKKmDP37P
> STARTTLS:  BMhffn64jm4OuEUDmfVEXtEw5UhnjY3aorRUGNtjn/WK
> ```
> AWS IAM의 SecretKey 는 40 byte 의 길이를 가지고 STARTTLS 는 44 byte 의 길이를 가진다.
> 
> 변환 후 선택적으로 이메일 발송 테스트를 수행할 수 있다.
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
#### 기본 사용법
> ```bash
> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py [AccessKEY] [SecretKEY] [REGION]
> ```

#### 명령행 옵션
> ```bash
> # 이메일 주소를 미리 지정하여 테스트
> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py [AccessKEY] [SecretKEY] [REGION] -f sender@domain.com -t recipient@domain.com
> 
> # 테스트 건너뛰기 (키 변환만 수행)
> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py [AccessKEY] [SecretKEY] [REGION] --no-test
> 
> # 옵션 설명
> -f, --from-email    발신자 이메일 주소 (테스트용)
> -t, --to-email      수신자 이메일 주소 (테스트용)
> --no-test           이메일 테스트 건너뛰기
> ```
### 이메일 발송 테스트
> 키 변환 후 이메일 발송 테스트를 선택할 수 있습니다.

#### 대화형 테스트
> 기본 실행 시 테스트 여부를 묻고, 이메일 주소를 입력받습니다.
>> ```bash
>> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py AAAAAAAAAAAAAAAAAAAA YOURKEYrrpg/JHpyvctStUVcAV9177EAKKmDP37P us-east-1
>> 🔄 SMTP 패스워드 변환 중...
>> ✅ 변환 완료!
>> 
>> ==================================================
>> ✅ AWS IAM → SES SMTP 변환 완료
>> ==================================================
>> Access Key ID: AAAAAAAAAAAAAAAAAAAA
>> SMTP Password: BMhffn64jm4OuEUDmfVEXtEw5UhnjY3aorRUGNtjn/WK
>> ==================================================
>> 
>> 📧 이메일 발송 테스트를 하시겠습니까? (Y/n): Y
>> 
>> 📧 이메일 테스트 설정
>> ========================================
>> 발신자 이메일 주소: noreply@domain.com
>> 수신자 이메일 주소: mail-receiver@domain.com
>> 
>> 🧪 이메일 테스트 실행 중...
>> 
>> 📡 연결 정보:
>>    호스트: email-smtp.us-east-1.amazonaws.com:587
>>    인증 ID: AAAAAAAA***
>>    발신자: noreply@domain.com
>>    수신자: mail-receiver@domain.com
>> 결과: ✅ 이메일 발송 성공!
>> ```

#### 명령행으로 이메일 지정
> ```bash
>> ~]$ ./aws-iam-secret_2_aws-ses-smtp.py AAAAAAAAAAAAAAAAAAAA YOURKEYrrpg/JHpyvctStUVcAV9177EAKKmDP37P us-east-1 -f noreply@domain.com -t recipient@domain.com
>> ```
### 사용 예시

#### 1. 키 변환만 수행
```bash
~]$ ./aws-iam-secret_2_aws-ses-smtp.py AKIA... SECRET... us-east-1 --no-test
```

#### 2. 대화형 테스트
```bash
~]$ ./aws-iam-secret_2_aws-ses-smtp.py AKIA... SECRET... us-east-1
# 실행 후 이메일 주소 입력
```

#### 3. 이메일 주소 미리 지정
```bash
~]$ ./aws-iam-secret_2_aws-ses-smtp.py AKIA... SECRET... us-east-1 -f sender@domain.com -t recipient@domain.com
```

### 주의사항
> - 발신자 이메일은 AWS SES에서 검증된 이메일이어야 합니다
> - 샌드박스 모드에서는 검증된 이메일로만 발송 가능합니다
> - 프로덕션 모드에서는 모든 이메일로 발송 가능합니다

# 출처
> AWS 공식 메뉴얼: https://repost.aws/ko/knowledge-center/ses-rotate-smtp-access-keys

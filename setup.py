import json
import sys
import os
from Crypto.Cipher import AES
import boto3

ZAPPA_DEFAULT_SETTING = {
    "dev": {
        "app_function": "main.app",
        "profile_name": None,
        "project_name": "day1_placeholder",
        "runtime": "python3.9",
        "s3_bucket": "day1_placeholder"
    }
}

ZAPPA_SETTINGS_FILE = 'zappa_settings.json'

ALLOWED_STUDENTS = [
    "10220",
    "10515",
    "10210",
    "10526",
    "10516",
    "10616",
    "10512",
    "10114",
    "10105",
    "10521",
    "10611",
    "10917",
    "21113",
    "10816",
    "10505",
    "10503"
]

if __name__ == '__main__':
    student_id = input('학번 입력: ')
    if student_id not in ALLOWED_STUDENTS:
        raise ValueError('Unknown Student ID!')
        sys.exit(1)
    ZAPPA_DEFAULT_SETTING['dev']['project_name'] = f"day1_{student_id}"
    ZAPPA_DEFAULT_SETTING['dev']['s3_bucket'] = f"ym-swm-2022-day1-{student_id}"
    with open(ZAPPA_SETTINGS_FILE, 'wt') as f:
        f.write(json.dumps(ZAPPA_DEFAULT_SETTING))
    print('Zappa setting 완료!')

    raw_key = input('Key 입력: ').replace('-', '').strip()
    if len(raw_key) < 32 + 16:
        raise ValueError('Key 검증 실패!')
    key = raw_key[:32].encode()
    iv = raw_key[32:48].encode()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open('credentials.enc', 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data_str = decrypted_data.decode().rstrip('\x00')
        if not decrypted_data_str.startswith('[default]'):
            raise ValueError('Decryption failed!')
            sys.exit(1)
        
        os.makedirs(os.path.join(os.environ.get('USERPROFILE'), '.aws'), exist_ok=True)
        with open(os.path.join(os.environ.get('USERPROFILE'), '.aws', 'credentials'), 'wt') as decrypted_file:
            decrypted_file.write(decrypted_data_str)
            decrypted_file.write('aws_region = ap-northeast-2')
    print('AWS Credential setting 완료!')

    client = boto3.client('sts')
    resp = client.get_caller_identity()
    if resp['Arn'] != "arn:aws:iam::811150413773:user/student":
        raise ValueError('Returned ARN mismatch!')
    print('AWS Credential 검증 완료!')
    sys.exit(0)
    
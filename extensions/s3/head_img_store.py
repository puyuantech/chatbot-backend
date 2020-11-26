
import os
import requests
import traceback
import uuid

from bases.globals import settings
from extensions.s3.s3_client import S3Connector


class HeadImgStore:

    store_path = settings['TEMP_PATH']
    bucket_name = settings['AWS_PUBLIC_BUCKET_NAME']

    @classmethod
    def load_from_wechat(cls, head_img_url, file_path):
        r = requests.get(head_img_url)
        with open(file_path, 'wb') as f:
            f.write(r.content)

    @classmethod
    def load_from_user(cls, file_obj, file_path):
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

    @classmethod
    def upload_to_s3(cls, file_path, file_key):
        s3 = S3Connector.get_conn()
        s3.meta.client.upload_file(file_path, cls.bucket_name, file_key, ExtraArgs={'ContentType': 'image/jpeg'})

        obj_acl = s3.ObjectAcl(cls.bucket_name, file_key)
        obj_acl.put(ACL = 'public-read')

    @staticmethod
    def clear_temp_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @classmethod
    def store_head_img_from_wechat(cls, user_id, head_img_url):
        if not head_img_url or not cls.bucket_name:
            return False, f'missing head_img_url/bucket_name (head_img_url){head_img_url} (bucket_name){cls.bucket_name}'

        try:
            file_path = os.path.join(cls.store_path, f'image_from_wechat_{user_id}')
            file_key = f'head_img/image_from_wechat_{user_id}'

            cls.load_from_wechat(head_img_url, file_path)
            cls.upload_to_s3(file_path, file_key)
            cls.clear_temp_file(file_path)

            return True, f'https://{cls.bucket_name}.s3.cn-northwest-1.amazonaws.com.cn/{file_key}'

        except:
            return False, traceback.format_exc()

    @classmethod
    def store_head_img_from_user(cls, user_id, file_obj, suffix=''):
        if not file_obj or not cls.bucket_name:
            return False, f'missing bucket_name (bucket_name){cls.bucket_name}'

        try:
            file_path = os.path.join(cls.store_path, f'image_from_user_{user_id}{suffix}')
            file_key = f'head_img/image_from_user_{user_id}{suffix}'

            cls.load_from_user(file_obj, file_path)
            cls.upload_to_s3(file_path, file_key)
            cls.clear_temp_file(file_path)

            return True, f'https://{cls.bucket_name}.s3.cn-northwest-1.amazonaws.com.cn/{file_key}'

        except:
            return False, traceback.format_exc()

    @classmethod
    def store_brand_image_from_user(cls, user_id, file_obj, suffix=''):
        if not file_obj or not cls.bucket_name:
            return False, f'missing bucket_name (bucket_name){cls.bucket_name}'

        try:
            image_id = uuid.uuid1().hex
            file_path = os.path.join(cls.store_path, f'image_from_user_{user_id}{suffix}')
            file_key = f'brand_img/{user_id}_{image_id}{suffix}'

            cls.load_from_user(file_obj, file_path)
            cls.upload_to_s3(file_path, file_key)
            cls.clear_temp_file(file_path)

            return True, f'https://{cls.bucket_name}.s3.cn-northwest-1.amazonaws.com.cn/{file_key}'

        except:
            return False, traceback.format_exc()

    @classmethod
    def store_head_img_from_business_card(cls, user_id, file_obj):
        return cls.store_head_img_from_user(user_id, file_obj, '_business_card')


if __name__ == '__main__':
    HeadImgStore().store_head_img_from_wechat(1, '')


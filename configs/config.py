
SECRET_KEY = '\x19r<\xb8\x82\xe9e\xc9\xf1\xaf\xe4\x8f\x86Dx]%\x123\xcd\x91\xac'

# redis
REDIS_URL = 'redis://:{}@{}:{}/{}'.format(
    '',
    '39.98.109.26',
    6379,
    0,
)

# mysql设置
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    '',
    '',
    'robo-test.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn',
    3306,
    'tapp',
)
# SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# 日志相关设置
LOG_PATH = '../log'
LOG_PATH_FILE = 'server.log'
LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10
TEMP_PATH = '../temp'

# AWS 相关
AWS_REGION_NAME = 'cn--1'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = '+lOx/1qBc'
AWS_PUBLIC_BUCKET_NAME = 'chat--'
AWS_PRIVATE_BUCKET_NAME = 'r'


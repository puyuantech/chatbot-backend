from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from models import *

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('--username', dest='username', help='admin username', default='chat_bot')
@manager.option('--password', dest='password', help='admin password', default='bot_password')
def init_admin(username, password):

    # create admin
    user_info = User(
        nick_name=username,
        role_id=1,
    )
    user_info = user_info.save()

    user_login = UserLogin(
        user_id=user_info.id,
    )
    user_login.username = username
    user_login.password = password
    user_login.save()
    print('\033[32m {} 创建成功！！！'.format(username))


@manager.command
def init_es():
    from extensions.es.es_rebuilder import re_build
    re_build()
    print('\033[32m es 创建成功！！！')


if __name__ == '__main__':
    manager.run()



# chatbot-backend

- 开发启动：python manager.py runserver -h ()  -p () --debug
- 启动项目：gunicorn -w 1 -k gevent -b 127.0.0.1:8003 manager:app
---

### 创建管理员
- python manager.py init_admin --username () --password ()

### config:
- 在configs/__init__.py 中，可以加local.py 重置路径

### 数据库迁移：
- 1.python 文件 db init
- 2.python 文件 db migrate -m"版本名(注释)"
- 3.python 文件 db upgrade (将表结构更新到数据库)
- 4.根据需求修改模型
- 5.python 文件 db migrate -m"新版本名(注释)"
- 6.python 文件 db upgrade 然后观察表结构
- 7.若返回版本,则利用 python 文件 db history查看版本号
- 8.python 文件 db downgrade(upgrade) 版本号

### 路由：
- router/v1.py 中注册路由

### 逻辑：
- 视图层都在apps内

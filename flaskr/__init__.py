# -*- coding: utf-8 -*-
# @Time : 2021/1/26 0026 15:44
# @Author : Niklaus
# @File : __init__.py.py
# @Software: PyCharm


import os

from flask import Flask


def create_app(test_config=None):
    # 创建和配置app, __name__当前模块名称，instance_relative_config告诉应用配置文件时相对路径
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(  # 应用缺省配置
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # 加载配置实例
        app.config.from_pyfile('config.py', silent=True)  # 用于设置一个正式的SECRET_KEY
    else:
        # 加载测试文件
        app.config.from_mapping(test_config)

    # 确保配置文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # HelloWorld
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 注册数据库实例
    from . import db
    db.init_app(app)

    # 注册蓝图实例
    from . import auth
    app.register_blueprint(auth.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
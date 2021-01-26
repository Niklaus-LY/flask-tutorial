# -*- coding: utf-8 -*-
# @Time : 2021/1/26 0026 15:58
# @Author : Niklaus
# @File : db.py
# @Software: PyCharm


import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # 告诉连接返回类似字典的行，可以通过列名操作数据

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # 定义一个命令行，名为 init-db
@with_appcontext
def init_db_command():
    """清除已有数据，并创建新的tables"""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """在应用实例中注册close_db和init_db_command"""
    app.teardown_appcontext(close_db)  # 返回响应后进行清理的时候调用此函数
    app.cli.add_command(init_db_command)  # 添加一个新的可以与flask一起工作的命令


if __name__ == '__main__':
    pass

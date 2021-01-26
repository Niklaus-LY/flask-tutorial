# -*- coding: utf-8 -*-
# @Time : 2021/1/26 0026 16:20
# @Author : Niklaus
# @File : auth.py
# @Software: PyCharm


import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# 创建名为auth的Blueprint，并把url_prefix添加到蓝图相关的URL前面
bp = Blueprint('auth', __name__, url_prefix='auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # 如果用户提交表单，则验证用户的输入内容
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)  # 使用占位符可以防止SQL注入
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))  # 数据库存储密文
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)  #  flash() 用于储存在渲染模块时可以调用的信息。

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']  # 查询用户并放在会话对象中
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_request  # 注册一个运行在视图函数之前的
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """注销"""
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)  # ?
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

if __name__ == '__main__':
    pass

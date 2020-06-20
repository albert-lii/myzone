# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 9:44 
"""
import arrow
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user

from app.bp_auth.models import User, Role
from app.extensions import login_manager
from app.response.maker import make_response_ok, make_response_error
from app.response.status import Status
from app.utils.checkers import (
    check_username_valid,
    check_username_existed,
    check_useremail_existed,
    check_email_valid,
)
from app.utils.emails import send_register_mail, send_forgetpwd_mail
from app.utils.flashutil import flash_ok, flash_error
from app.utils.security import (
    encrypt_password,
    validate_password,
    generate_randint_captcha,
)
from app.utils.urlutil import redirect_back
from . import auth_bp
from .forms import LoginForm, RegisterForm, ForgetPwdForm


@login_manager.user_loader
def load_user(user_id: int):
    """flask-login 的 user_loader 回调函数"""
    user = User.query_by_id(user_id)
    if user:
        cur_user = user
        cur_user.id = int(user_id)
        return cur_user


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        # 如果用户已登录，却导航到 login URL 处，则直接重定向到主页面
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        account = form.account.data
        password = form.password.data
        remember_me: bool = form.remember_me.data
        user: User = User.query_by_account(account)
        if user:
            if validate_password(user.password, password):
                user.update_login_time()
                login_user(user, remember=remember_me)
                flash_ok(u"登录成功")
                return redirect_back()
            else:
                flash_error(u"密码错误")
        else:
            flash_error(u"用户不存在")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout/", methods=["GET", "POST"])
def logout():
    """退出登录"""
    logout_user()
    return redirect(url_for("main.index"))


@auth_bp.route("/register/", methods=["GET", "POST"])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        # 如果用户已登录，却导航到 register URL 处，则直接重定向到主页面
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        submit_time = arrow.utcnow().timestamp
        username = form.username.data
        email = form.email.data
        captcha = form.captcha.data
        password = form.password.data
        old_captcha = session.get(email)
        if old_captcha:
            old_captcha_arr = old_captcha.split(",")
            if old_captcha_arr[0] != str(captcha):
                flash_error(u"验证码错误")
            else:
                diff_time = submit_time - int(old_captcha_arr[1])
                if diff_time > 0 and (diff_time / 60) <= 10:
                    if check_username_existed(username):
                        flash_error(u"该用户名已被使用，请选用其他名称")
                    elif check_useremail_existed(email):
                        flash_error(u"该邮箱已被使用，请选用其他邮箱")
                    else:
                        role: Role = Role.query_by_id(1)  # 普通用户角色
                        user = User()
                        user.username = username
                        user.password = encrypt_password(password)
                        user.email = email
                        if form.site:
                            user.personal_site = form.site.data
                        user.role_id = role.id
                        user.role = role
                        user.insert_single()
                        flash_ok(u"注册成功")
                        return redirect(url_for(".login"))
                else:
                    # 如果时间间隔相差 10 分钟，则验证码失效
                    flash_error(u"验证码已过期，请重新获取验证码")
        else:
            flash_error(u"验证码错误")
    return render_template("auth/register.html", form=form)


@auth_bp.route("/forget-password/", methods=["GET", "POST"])
def forget_password():
    """忘记密码"""
    if current_user.is_authenticated:
        # 如果用户已登录，却导航到 register URL 处，则直接重定向到主页面
        return redirect(url_for("main.index"))
    form = ForgetPwdForm()
    if form.validate_on_submit():
        submit_time = arrow.utcnow().timestamp
        email = form.email.data
        captcha = form.captcha.data
        password = form.password.data
        user = User.query_by_email(email)
        if user:
            old_captcha = session.get(email)
            if old_captcha:
                old_captcha_arr = old_captcha.split(",")
                if old_captcha_arr[0] != str(captcha):
                    flash_error(u"验证码错误")
                else:
                    diff_time = submit_time - int(old_captcha_arr[1])
                    if diff_time > 0 and (diff_time / 60) <= 10:
                        user.password = encrypt_password(password)
                        user.update()
                        flash_ok(u"密码重置成功")
                        return redirect(url_for(".login"))
                    else:
                        # 如果时间间隔相差 10 分钟，则验证码失效
                        flash_error(u"验证码已过期，请重新获取验证码")
            else:
                flash_error(u"验证码错误")
        else:
            flash_error(u"用户不存在")
    return render_template("auth/forgetPwd.html", form=form)


@auth_bp.route("/captcha/", methods=["POST"])
def send_captcha():
    """发送验证码"""
    args = request.json
    captcha_type: int = args.get("captcha_type")  # 1-注册 2-忘记密码
    name: str = args.get("name")
    email: str = args.get("email")

    if captcha_type == 1:
        if not name:
            return make_response_error(Status.ERROR_INVALID_USERNAME).to_json()

        # if not check_username_valid(name):
        #     return make_response_error(Status.ERROR_INVALID_USERNAME).to_json()

        if len(name) > 64:
            return make_response_error(Status.ERROR_INVALID_USERNAME).to_json()

        if check_username_existed(name):
            return make_response_error(Status.ERROR_USERNAME_EXISTED).to_json()

    if not email:
        return make_response_error(Status.ERROR_INVALID_EMAIL).to_json()

    if not check_email_valid(email):
        return make_response_error(Status.ERROR_INVALID_EMAIL).to_json()

    if captcha_type == 1:
        if check_useremail_existed(email):
            return make_response_error(Status.ERROR_EMAIL_EXISTED).to_json()

    captcha: str = generate_randint_captcha()  # 获取随机生成的 6 位验证码
    if captcha_type == 1:
        send_register_mail(email, captcha)
    else:
        send_forgetpwd_mail(email, captcha)
    session[email] = "{captcha},{timestamp}".format(
        captcha=captcha, timestamp=arrow.utcnow().timestamp
    )  # 缓存邮箱地址和验证码
    return make_response_ok(u"验证码已发送").to_json()

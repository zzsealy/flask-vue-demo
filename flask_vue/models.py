from flask_vue import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
import base64
from datetime import datetime, timedelta
import os


class PaginatedAPIMixin(object):
    @staticmethod  # 静态方法
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):  # endpoint传入的应该是端点
        resources = query.paginate(page, per_page, False)
        data = {
            # 返回的列表，每个值是一个字典。
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)  # 索引和禁止重复
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 存储密码的哈希值
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User{}>'.format(self.username)

    # 设置密码 储存的是哈希值
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码，储存的哈希值调用函数检查
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id)  # 指向自己的链接。
            }
        }
        if include_email:
            data['email'] = self.email  # 请求自己的数据的时候才返回邮箱
        return data

    # 前端发送过来的JSON对象，需要转换成User对象。  可能用来修改密码和邮箱等操作
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # 如果token没过期，返回token。 而且无论如何斗更新token。
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    # 使token过期
    def remove_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # 如果过期返回空
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

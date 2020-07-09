from flask_vue import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app
import base64
from datetime import datetime, timedelta
import os
import jwt
from hashlib import md5


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
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    rember_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def get_jwt(self, expires_in=600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'name': self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))
    
    def avatar(self, size):
        ''' 头像 '''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

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
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'rember_since': self.rember_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id),  # 指向自己的链接。
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email  # 请求自己的数据的时候才返回邮箱
        return data

    # 前端发送过来的JSON对象，需要转换成User对象。  可能用来修改密码和邮箱等操作
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me']:
            if field in data:

                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    

from flask_vue import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True) # 索引和禁止重复
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 存储密码的哈希值

    def __repr__(self):
        return '<User{}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id':self.id,
            'username': self.username,
            '_links':{
                'self': url_for('api.get_user', id=self.id) # 指向自己的链接。
            }
        }
        if include_email:
            data['email'] = self.email  # 请求自己的数据的时候才返回邮箱
        return data


class PaginatedAPIMixin(object):
    @staticmethod  # 静态方法
    def to_collection_dict(query, page, per_page, endpoint, **kwargs): # endpoint传入的应该是端点
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],  # 返回的列表，每个值是一个字典。
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
    

    


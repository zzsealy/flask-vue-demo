from flask_vue.api import bp

@bp.route('/users', methods=['POST'])
def create_user():
    '''注册一个新用户'''
    pass

@bp.route('/users', methods=['GET'])
def get_users():
    '''返回所有用户的集合'''
    return 'hello world!'

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    '''返回一个用户'''
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update(id):
    '''修改一个用户'''
    pass

@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    '''删除一个用户'''
    pass
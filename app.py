from flask import Flask, request, redirect, send_from_directory
from flask_login.utils import login_required 
from flask_restful import Resource, Api
from db.db import get_mainpage, get_user_profiles, get_current_user, change_invites, ban_user, invites_str, closed_acess
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, login_user
import os 
# from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)
app.config['WTF_CSRF_ENABLED'] = False 
cors = CORS(app)
# login_manager = LoginManager(app)
# jwt = JWTManager(app)

todos = {}

# class UserLogin():
#     def fromDB(self, user_id):
#         self.__user = get_user_site(user_id)
#         return self

#     def create(self, user):
#         self.__user = user
#         return self 

#     def is_authenticated(self):
#         return True
 
#     def is_active(self):
#         return True
 
#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         return str(self.__user['id'])


# @login_manager.user_loader
# def load_user(user_id):
#     return UserLogin().fromDB(user_id)

class MainPage(Resource):
    # @login_required
    @cross_origin()
    def get(self):
        return get_mainpage()

class AllUsers(Resource):
    @cross_origin()
    def get(self):
        return get_user_profiles()

class GetUser(Resource):
    @cross_origin()
    # @login_required
    def get(self, id):
        return get_current_user(id)

class ChangeInvites(Resource):
    @cross_origin()
    # @login_required
    def post(self, id, count):
        return change_invites(id, count)

class Ban(Resource):
    @cross_origin()
    # @login_required
    def post(self, invite):
        return ban_user(invite)

class Invites(Resource):
    @cross_origin()
    # @login_required
    def get(self):
        return invites_str()

class ClosedAcess(Resource):
    @cross_origin()
    # @login_required
    def get(self):
        return closed_acess()


class Photos(Resource):
    @cross_origin()
    def get(self, name):
        uploads = os.path.join(app.root_path, 'photos')

        return send_from_directory(directory=uploads, path=os.path.join(uploads, name), filename=name)

class Rules(Resource):
    @cross_origin()
    def get(self):
        path = os.path.join(app.root_path, 'politics.docx')
        return send_from_directory(directory=app.root_path, path=path, filename='politics.docx')

# class Login(Resource):
#     @cross_origin()
#     def post(self, login, password):
#         form = LoginForm()                                                                                                                                                     
#     if form.validate_on_submit():                                                                                                                                                                                                                                                 
#         if form.username.data == 'Login' and form.password.data == 'Password':                                          
#             flash('Вы вошли')                                                                                                                                              
#             return redirect('/index')                                  

api.add_resource(MainPage, '/')
api.add_resource(AllUsers, '/users')
api.add_resource(GetUser, '/getuser/<int:id>')
api.add_resource(ChangeInvites, '/change_invites/<int:id>/<int:count>')
api.add_resource(Ban, '/ban/<string:invite>')
api.add_resource(Invites, '/invites')
api.add_resource(ClosedAcess, '/closed_acess')
api.add_resource(Photos, '/file/<string:name>')
api.add_resource(Rules, '/politics')

# api.add_resource(Login, '/login')


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
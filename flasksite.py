from flask import Flask, request
from flask_restful import Resource, Api
from db.db import get_user_profiles, get_current_user, change_invites, ban_user, invites_str, closed_acess

app = Flask(__name__)
api = Api(app)

todos = {}

class MainPage(Resource):
    def get(self):
        return get_user_profiles()

class GetUser(Resource):
    def get(self, id):
        return get_current_user(id)

class ChangeInvites(Resource):
    def post(self, id, count):
        return change_invites(id, count)

class Ban(Resource):
    def post(self, invite):
        return ban_user(invite)

class Invites(Resource):
    def get(self):
        return invites_str()

class ClosedAcess(Resource):
    def get(self, token):
        return closed_acess(token)


api.add_resource(MainPage, '/')
api.add_resource(GetUser, '/getuser/<int:id>' )
api.add_resource(ChangeInvites, '/change_invites/<int:id>/<int:count>')
api.add_resource(Ban, '/ban/<string:invite>')
api.add_resource(Invites, '/invites')
api.add_resource(ClosedAcess, '/closed_acess/<string:token>')


if __name__ == '__main__':
    app.run(debug=True)
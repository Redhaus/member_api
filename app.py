from flask import Flask, request, jsonify
from database import get_db
from member import Member
from functools import wraps

app = Flask(__name__)

api_username = 'redhaus'
api_password = 'password'


# set up decorator function
# use functtools wrap decorator to keep function data
# decorated function accepts wildcard params
# checks authentication
# returns function if authorized error if not
# return decorated funnction without calling it ()
def protected(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return {"message": "authentication failed"}, 403

    return decorated


# GET ALL MEMBERS DONE

@app.route('/member', methods=['GET'])
@protected
def get_members():
    all_members = Member.get_all_members()

    username = request.authorization.username
    password = request.authorization.password

    return all_members


# GET MEMBER BY ID DONE
@app.route('/member/<int:member_id>', methods=['GET'])
@protected
def get_member(member_id):
    one_member = Member.get_member_by_id(member_id)
    return one_member


# GET MEMBER BY NAME DONE
@app.route('/member/name/<string:name>', methods=['GET'])
@protected
def get_member_name(name):
    one_member = Member.get_member_by_name(name)
    return one_member


# ADD NEW MEMBERS DONE
@app.route('/member', methods=['POST'])
@protected
def add_member():
    data = request.get_json()

    name = data['name']
    email = data['email']
    level = data['level']

    # creating new member instance
    new_member = Member(name, email, level)
    # adding member to db and return json of new member added
    mem_data = new_member.add_member()
    return mem_data


# UPDATE MEMBERS
@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
@protected
def edit_member(member_id):
    data = request.get_json()
    # return jsonify(data)
    update = Member.update_member(data, member_id)

    return update


# DELETE MEMBERS
@app.route('/member/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    return Member.delete_member_by_id(member_id)


# pass


if __name__ == '__main__':
    app.run(debug=True)

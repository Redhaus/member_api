from flask import jsonify

from database import get_db


class Member(object):

    def __init__(self, name: str, email: str, level: str, id=None):
        self.name = name
        self.email = email
        self.level = level
        self.id = id


    # GET ALL MEMBERS
    @classmethod
    def get_all_members(cls):

        # create an empty list to hold member
        all_members = []

        db = get_db()
        db.execute('''select * from members''')

        for member in db.fetchall():
            # create a member obj
            db_member_obj = cls(**member)

            # use that obj to format json data
            all_members.append(db_member_obj.json())

        # return  array of json member objects
        return jsonify(all_members)


    # GET ONE MEMBER BY ID
    @classmethod
    def get_member_by_id(cls,id):
        # make connection to db
        db = get_db()

        # execute and fetch data
        db.execute('''select * from members where id = %s''', (id,))
        member = db.fetchone()

        # convert data into class obj and return
        member_obj = cls(**member)
        return member_obj.json()


    # GET ONE MEMBER BY NAME
    @classmethod
    def get_member_by_name(cls, name):
        # connect to db
        db = get_db()

        # execute query and fetch data / query caseinsensitive lower
        db.execute('''select * from members where lower(name) = %s''', (name,))
        member = db.fetchone()

        # create class obj to return
        new = cls(**member)

        return new.json()



    # ADD MEMBER
    def add_member(self):
        db = get_db()

        # formating member data
        name = self.name
        email = self.email
        level = self.level

        # saving member to db
        db.execute('''insert into members (name, email, level) 
                      values (%s, %s, %s)''', (name, email, level))

        # retrieving formatted json from just added with new db with added id
        member = Member.get_member_by_name(name)

        # returing formatted member obj
        return member


    # EDIT MEMBER BY ID
    @staticmethod
    def update_member(data, id):

        # organize data provided
        name = data['name']
        email = data['email']
        level = data['level']

        # conn to db and update data
        db = get_db()
        db.execute('''update members 
                    set name = %s, email = %s, level = %s 
                    where id = %s ''', (name, email, level, id))

        updated_member = Member.get_member_by_id(id)
        return updated_member



    # EDIT MEMBER BY ID
    @staticmethod
    def put_member(data, id):
        # organize data provided
        name = data['name']
        email = data['email']
        level = data['level']

        # conn to db and update data
        db = get_db()
        db.execute('''update members 
                    set name = %s, email = %s, level = %s 
                    where id = %s ''', (name, email, level, id))

        # fetch and return updated member data
        updated_member = Member.get_member_by_id(id)
        return updated_member


    # DELETE MEMBER
    @staticmethod
    def delete_member_by_id(id):
        db = get_db()
        db.execute('delete from members where id = %s', (id, ))
        return {'deleted' : f'Member {id} has been deleted'}



    # FORMAT JSON OBJECT FROM OBJ CLASS
    def json(self):
        return {
            'name': self.name,
            'email': self.email,
            'level': self.level,
            'id': self.id
        }

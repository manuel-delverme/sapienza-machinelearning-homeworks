import pymongo
import os
import json


class User:
    def __init__(self, user_dict):
        self.user_dict = user_dict

    @property
    def name(self):
        return self.user_dict['name']

    @name.setter
    def name(self, value):
        self.user_dict['name'] = value

    @property
    def tid(self):
        return self.user_dict['tid']

    def __repr__(self):
        return repr(self.user_dict)


class Gaia_db:
    def __init__(self, name="mariadb"):
        from sshtunnel import SSHTunnelForwarder
        host = os.popen("grep -A15 blobchuck ~/.ssh/config | grep HostName | awk '{print $2}'").read()
        user = os.popen("grep -A15 blobchuck ~/.ssh/config | grep User | awk '{print $2} | head -n 1'").read()
        self.SSHTunnel = SSHTunnelForwarder(
            ssh_address_or_host=host,
            ssh_username=user,
            ssh_private_key_or_password="~/.ssh/id_rsa",
            remote_bind_address=('127.0.0.1', 27017),
        )

        self.SSHTunnel.start()

        with open('DB_keys') as f:
            DBKEY,  = [row for row in f.read()[:-1].split("\n") if row[0] != "#"]

        self.uri = DBKEY
        self.client = pymongo.MongoClient('127.0.0.1', self.SSHTunnel.local_bind_port)
        self.db = self.client[name]
        try:
            self.db.create_collection(name='users')
            print('\nCollection created\n')
        except pymongo.errors.CollectionInvalid:
            print('\nCollection exists\n')
        try:
            self.db.create_collection(name='open_questions')
            print('\nCollection created\n')
        except pymongo.errors.CollectionInvalid:
            print('\nCollection exists\n')

    def insert(self, users):
        for user in users.values():
            self.insert_one(user)

    def insert_one(self, user):
        if isinstance(user, User):
            user = user.user_dict
        try:
            self.db.users.insert_one(user)
            print('Adding', user, '\n')
        except pymongo.errors.DuplicateKeyError:
            print('Employee', user, 'yet present\n')

    def update_one(self, user):
        user = user.user_dict
        self.db.users.find_one_and_update({'_id': user['_id']}, {"$set": user})
        print('updating', user, '\n')

    def remove(self, value):
        return User(self.db.users.remove({'name': value.lower()}, 1))

    def find_by_tid(self, value):
        user_dict = self.db.users.find_one({'tid': value})
        if user_dict:
            return User(user_dict)
        else:
            return None

    def find(self, parameters):
        response = self.db.knowledge.find(parameters)
        return list(response)

    def find_by_job(self, value):
        user_dict = self.db.users.find({'job': value.lower()})
        if user_dict:
            return User(user_dict)
        else:
            return None

    def get_open_question(self, domain):
        question = self.db.open_questions.find_one({
            'answered': False,
            'domain': domain,
        })
        if not question:
            return "NO_RELATION", "NO_QUESTION"
        else:
            return question['relation'], question['question']

    def close_open_question(self, relation, question):
        question = self.db.open_questions.find_one({
            'answered': False,
            'relation': relation,
            'question': question,
        })
        return question['relation'], question['question']

    def add_open_question(self, question):
        self.db.open_questions.insert({
            'question': question,
            'answered': False
        })

class Fake_db:
    def __init__(self):
        print("USING FAKE DB!")
        pass

    def insert(self, users):
        for user in users.values():
            self.insert_one(user)

    def insert_one(self, user):
        raise NotImplementedError()

    def update_one(self, user):
        raise NotImplementedError()

    def remove(self, value):
        raise NotImplementedError()

    def find_by_tid(self, value):
        return User({'tid': value})

    def get_open_question(self, domain):
        return "relation", "question"

    def close_open_question(self, relation, question):
        raise NotImplementedError()

    def add_open_question(self, question, relation=None):
        raise NotImplementedError()

    def find(self, parameters):
        print("DB NOT INMPLEMENTED!!!")
        return []

if __name__ == "__main__":
    pass

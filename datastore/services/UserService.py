import base64
import json
import string
import random
from django.db import transaction
from datastore.models.User import User


def getAllUser():
    user = User.objects.all()
    userList = []
    for found_user in user:
        newUser = {}
        keys = base64.b64decode(found_user.broker_key).decode('utf-8')
        if keys != "":
            keys = json.loads(keys)
        newUser['id'] = found_user.user_id
        newUser['key'] = keys
        newUser['token'] = found_user.token
        userList.append(newUser)
    if len(userList) != 0:
        return {'list': userList}
    return {'list': []}


def getUser(user_id):
    found_user = User.objects.filter(user_id=user_id)
    if len(found_user) == 0:
        return None
    newUser = {}
    keys = base64.b64decode(found_user[0].broker_key).decode('utf-8')
    if keys != "":
        keys = json.loads(keys)
    newUser['id'] = found_user[0].user_id
    newUser['key'] = keys
    newUser['token'] = found_user[0].token

    return newUser


@transaction.atomic
def addUser(user_id, password):
    user = User.objects.filter(user_id=user_id)
    if len(user) > 0:
        return False

    user = User(user_id=user_id, password=hash(password))
    user.save()
    return True


@transaction.atomic
def updateUser(user_id, password):
    old_user = User.objects.filter(user_id=user_id)
    if len(old_user) == 0:
        return False

    User.objects.filter(user_id=str(user_id)).update(password=hash(password))
    return True


@transaction.atomic
def deleteUser(user_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) != 0:
        user[0].delete()
        return True
    return False


def getUserKeys(user_id):
    found_user = User.objects.filter(user_id=user_id)
    if len(found_user) == 0:
        return None
    keys = base64.b64decode(found_user[0].broker_key).decode('utf-8')
    if keys == "":
        return None

    return json.loads(keys)


@transaction.atomic
def updateUserKeys(user_id, broker_keys):
    old_user = User.objects.filter(user_id=user_id)
    if len(old_user) == 0:
        return False

    User.objects.filter(user_id=str(user_id)).update(broker_key=base64.b64encode(broker_keys))
    return True


@transaction.atomic
def deleteUserKeys(user_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) != 0:
        User.objects.filter(user_id=user_id).update(broker_key="")
        return True
    return False


@transaction.atomic
def login(user_id, pwd):
    user = User.objects.filter(user_id=user_id)
    if len(user) == 0:
        return None
    if user[0].password != str(hash(pwd)):
        return None

    token = user[0].token
    if token != "":
        return token
    while True:
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
        connected_user = User.objects.filter(token=token)
        if len(connected_user) == 0:
            break
    User.objects.filter(user_id=user_id).update(token=token)
    return token


@transaction.atomic
def getUserFromToken(token):
    user = User.objects.filter(token=token)
    if len(user) == 0:
        return None
    return user[0].user_id


@transaction.atomic
def getAllUsersConnected():
    user = User.objects.all()
    userList = []
    for found_user in user:
        newUser = {}
        token = found_user.token
        if token != "":
            newUser['id'] = found_user.user_id
            newUser['token'] = found_user.token
            userList.append(newUser)
    if len(userList) != 0:
        return {'list': userList}
    return None


def getUserObject(user_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) == 0:
        return None
    return user[0]
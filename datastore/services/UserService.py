import base64
import json
from django.db import transaction
from datastore.models import User


def getAllUser():
    user = User.objects.all()
    userList = []
    for foundUser in user:
        newUser = {}
        keys = base64.b64decode(foundUser.broker_key).decode('utf-8')
        newUser['id'] = foundUser.user_id
        newUser['key'] = json.loads(keys)
        userList.append(newUser)
    if len(userList) != 0:
        return {'list': userList}
    return None


def getUser(user_id):
    found_user = User.objects.filter(user_id=user_id)
    if len(found_user) == 0:
        return None
    newUser = {}
    keys = base64.b64decode(found_user[0].broker_key).decode('utf-8')
    newUser['id'] = found_user[0].user_id
    newUser['key'] = json.loads(keys)

    return newUser


@transaction.atomic
def addUser(user_id, broker_keys):
    user = User.objects.filter(user_id=user_id)
    if len(user) > 0:
        return False

    user = User(user_id=user_id, broker_key= base64.b64encode(broker_keys))
    user.save()
    return True


@transaction.atomic
def deleteUser(user_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) != 0:
        user[0].delete()
        return True
    return False
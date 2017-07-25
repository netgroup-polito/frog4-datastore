import base64
import json
from django.db import transaction
from rest_framework.parsers import ParseError

from datastore.models.Yang import YANG_Models
from datastore.parsers.YANGtoYIN import create_yin


def getAllYANG_model():
    yang = YANG_Models.objects.all()
    yangList = []
    for foundYang in yang:
        newYANGModel = {}
        model = base64.b64decode(foundYang.yang_model).decode('utf-8')
        newYANGModel['id'] = foundYang.yang_id
        newYANGModel['models'] = model
        yangList.append(newYANGModel)
    if len(yangList) != 0:
        return {'list': yangList}
    return {'list': []}


def getYANG_model(yang_id):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        return None
    model = base64.b64decode(yang[0].yang_model).decode('utf-8')
    return model


def getYINFromYangID(yang_id):
    yang = getYANG_model(yang_id)
    if yang is not None:
        yang = create_yin(str(yang))
    else:
        return None
    return json.loads(yang)


@transaction.atomic
def addYANG_model(yang_id, yang_model):
    if yang_model == {}:
        raise ParseError(detail="no yang was provided") #the empty case is managed in such a way because django don't pass an empty body to the parser
    found_yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(found_yang) > 0:
        return False
    yang = YANG_Models(yang_id=yang_id, yang_model=base64.b64encode(yang_model))
    yang.save()

    return True


@transaction.atomic
def deleteYANG_model(yang_id):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) != 0:
        yang[0].delete()
        return True
    return False


@transaction.atomic
def updateYANG_model(yang_id, yang_model):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        return False
    YANG_Models.objects.filter(yang_id=yang_id).update(yang_model=base64.b64encode(yang_model))
    return True


def getYangModelObj(yang_id):
    model = YANG_Models.objects.filter(yang_id=yang_id)
    if len(model) > 0:
        return model[0]
    return None
from flask import request, jsonify, Response
from dbConnection import userstabel
from bson import json_util
import json
import datetime
from types import SimpleNamespace
import bcrypt
import re
from jwt import encode, decode
import os


passwordpattern = r'[A-Za-z0-9@#$%^&+=]{8,}'
emailpattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

signupresEx = """{'user': {'_id': '63dea711a4852468b7fa0108', 'name': 'bhusdddsmit12',
                        'password': "b'$2b$12$3FGB9kgWf.Z5fX1h43mvWuu8K.Iune3fgLwzZWJA3ezZiMDdW67Pq'", 'email': 'helsddslo@mcail.com', 'createdAt': '2023-02-05 00:12:25.185000'}}"""

print(os.urandom(24))


def authSignup(data=request):

    print(data.json)
    password = bcrypt.hashpw(
        data.json["password"].encode('utf-8'), bcrypt.gensalt())
    if re.fullmatch(emailpattern, data.json["email"]) == None:
        return Response(status=400, response=json.dumps({"message": "enter valid email!"}), content_type="application/json")

    req = {
        "name": data.json["name"],
        "password": password,
        "email": data.json["email"],
        "createdAt": datetime.datetime.now()
    }
    userExist = userstabel.find_one({'name': req["name"]}, )
    emailExist = userstabel.find_one({'email': req["email"]}, )
    checkList = [userExist != None, emailExist != None]
    # print(checkList)
    # print(f"user name match--->{all(check  for check in checkList)}")
    if all(check for check in checkList):

        return Response(status=400, response=json.dumps({"message": "user name / email already exist!"}), content_type="application/json")

    else:
        if re.fullmatch(passwordpattern, data.json["password"]):
            newuser = userstabel.insert_one(req)
            res = userstabel.find_one({'_id': newuser.inserted_id}, )
            res['createdAt'] = str(res['createdAt'])
            res['password'] = str(res['password'])
            res['_id'] = str(res['_id'])

            # del res['_id']
            print({"user": res})
            return Response(status=201, response=json_util.dumps({"user": res}), content_type="application/json")
        else:
            return Response(status=400, response=json_util.dumps({"message": "Password must contains 8 char. 1 uppercase 1 lowercase 1 symbol and 1 number recommended"}), content_type="application/json")

    # print(userstabel.find_one({'_id': newuser.inserted_id}, ))
    # return {"success": newuser.__doc__.index}


def authLogin(data=request):
    print(data.json)
    password = bcrypt.hashpw(
        data.json["password"].encode('utf-8'), bcrypt.gensalt())
    req = {
        "name": data.json["name"],
        "email": data.json["email"],
        "password": password,

    }
    # newuser = userstabel.insert_one(req)

    res = userstabel.find_one({'email': req["email"]}, )
    password = bcrypt.hashpw(
        res['password'], bcrypt.gensalt())

    if bcrypt.checkpw(data.json["password"].encode('utf-8'),  res['password']):
        res['createdAt'] = str(res['createdAt'])
        res['password'] = str(res['password'])
        res['_id'] = str(res['_id'])
        res['accesstoken'] = encode(res, "b'\xe1\x1e\xc6`\xe5\xc5C\xdak>\n\x0b0\xf2tD\x9c\x15k\x02,\xab\xda\x19'",
                                    algorithm='HS256')
        decodeddd = decode(res['accesstoken'], "b'\xe1\x1e\xc6`\xe5\xc5C\xdak>\n\x0b0\xf2tD\x9c\x15k\x02,\xab\xda\x19'",
                           algorithms='HS256')
        print(f"decodedd===>{decodeddd}")
        return Response(status=200, response=json_util.dumps({"user": res}), content_type="application/json")

    else:
        return Response(status=400, response=json_util.dumps({"message": "invalid credentials!"}), content_type="application/json")

    # print(userstabel.find_one({'_id': newuser.inserted_id}, ))
    # return {"success": newuser.__doc__.index}

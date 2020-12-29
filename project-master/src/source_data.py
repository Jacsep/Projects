from error import InputError, AccessError
import auth_token
import random
from datetime import datetime

data = {
    "users": [
    ],
    "channels": [
    ],
    "messages": [
    ],
    "admins": [
    ],
    "resetCodes": [

    ]
}

"""Return a new dictionary that contains the information of the user from the
data dictionary"""


def get_userdata(email):
    users = data["users"]
    user = dict()
    user["existing"] = False
    user["id"] = None
    user["password"] = None
    user["token"] = None
    for x in users:
        if x["email"] == email:
            user["existing"] = True
            user["id"] = x["id"]
            user["password"] = x["password"]
            user["token"] = x["token"]
    return user


# Given a token, return its u_id as an integer.
def token2id(token):
    for i in data["users"]:
        if i.get("token") == token:
            return i.get("id")
    return


def validate_name_length(name_str):
    if len(name_str) < 1 or len(name_str) > 50:
        raise InputError("Invalid last name")


def validate_token(token):
    if token is None:
        raise AccessError("Token invalid")


# Given a channel id, return its information in a dictionary.
def get_channelinfo(channel_id):
    for i in data["channels"]:
        if i.get("channel_id") == channel_id:
            return i
    return {}


def valid_channel(channel_id):
    if not any(channel_id == i.get("channel_id") for i in data["channels"]):
        raise InputError("Invalid channel_id")

# Given a message id, return its information in a dictionary (From the messages dictionary).
def get_messageinfo(message_id):
    for i in data["messages"]:
        if i.get("message_id") == message_id:
            return i
    return {}

def generate_str_handle(name_first, name_last):
    users = data["users"]
    # We combine fname and lname, leaving 4 digit space to add a random 4 digit num, meaning it will always be unique.
    handle_str = name_first.lower() + name_last.lower()
    if len(handle_str) > 15:
        handle_str = handle_str[0:15]
    # Generate random 4 digit number
    random_num = random.randint(1000, 9999)
    # Use flag such that a new number is generated continously until no pre-existing matching handle is found
    flag = False
    while not flag:
        for user in users:
            if user["handle_str"] == handle_str + str(random_num):
                random_num = random.randint(1000, 9999)
        flag = True

    return handle_str + str(random_num)


def find_matching_user_dict_token(token):
    for user in data["users"]:
        if user["token"] == token:
            return user


def find_matching_user_dict_id(u_id):
    for user in data["users"]:
        if user["id"] == u_id:
            return user
    raise InputError("Not a valid user")


def get_auth_resetcode_fromcode(reset_code):
    for code in data["resetCodes"]:
        if code["code"] == reset_code:
            return code
    return False


def get_auth_resetcode_fromemail(email):
    for code in data["resetCodes"]:
        if code["email"] is email:
            return code


def auth_replace_resetcode(email, newcode):
    for code in data["resetCodes"]:
        if code["email"] is email:
            code["code"] = newcode
            code["timestamp"] = datetime.now()


def auth_changepassword(email, newpassword):
    for user in data["users"]:
        if user["email"] == email:
            user["password"] = auth_token.encrypt_password(newpassword)

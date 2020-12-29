import source_data as src
from auth import validate_email
from error import InputError, AccessError


def user_profile(token, u_id):
    src.validate_token(token)
    matching_user_dict = src.find_matching_user_dict_id(u_id)
    return {
        'user': {
            'u_id': matching_user_dict["id"],
            'email': matching_user_dict["email"],
            'name_first': matching_user_dict["fname"],
            'name_last': matching_user_dict["lname"],
            'handle_str': matching_user_dict["handle_str"],
        },
    }
            

def user_profile_setname(token, name_first, name_last):
    src.validate_token(token)
    src.validate_name_length(name_first)
    src.validate_name_length(name_last)
    
    matching = src.find_matching_user_dict_token(token)
    matching["fname"] = name_first
    matching["lname"] = name_last

    return {
    }


def user_profile_setemail(token, email):
    # Check token is valid first
    src.validate_token(token)
    # Check email is valid
    validate_email(email)
    # Check email is not used : Assumption (if email is same as users email allow user to change to same email)
    if src.get_userdata(email)["existing"] and src.get_userdata(email)["token"] != token:
        raise InputError("Email already used")
    # Find user from token and change email to new email
    matching = src.find_matching_user_dict_token(token)
    matching["email"] = email
    return {

    }


def user_profile_sethandle(token, handle_str):
    users = src.data["users"]
    # Check token is valid first
    src.validate_token(token)
    # Check handle_str is correct length
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle_str incorrect length")
    # Check handle_str is not used : Assumption (if handle is same as users handle allow user to change to same handle)
    for user in users:
        if user["handle_str"] is handle_str and user["token"] is not token:
            raise InputError("Handle already used")
    # Find user from token and change handle to new handle
    matching = src.find_matching_user_dict_token(token)
    matching["handle_str"] = handle_str

    return {

    }

import smtplib
import source_data as src
import error
import re
import auth_token
import auth_helper
from datetime import datetime

users = src.data["users"]
all_reset_codes = src.data["resetCodes"]


def valid_email(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.search(regex, email):
        return True
    return False


def validate_email(email):
    if not valid_email(email):
        raise error.InputError("Email invalid")


def auth_login(email, password):
    """Checks required for email, password to ensure they meet specifications"""
    checkDetails = src.get_userdata(email)
    encryptedpw = auth_token.encrypt_password(password)
    validate_email(email)
    if not checkDetails["existing"]:
        raise error.InputError("Email not registered!")
    if checkDetails["password"] != encryptedpw:
        raise error.InputError("Incorrect password!")
    """If user logouts and then logins we need to renew his token"""
    if checkDetails["token"] is None:
        for x in users:
            if x["email"] == email:
                x["token"] = auth_token.generate_token(email)
    return {
        'u_id': src.get_userdata(email)["id"],
        'token': src.get_userdata(email)["token"],
    }


def auth_logout(token):
    """Find token in database and make invalid"""
    is_success = False
    for user in users:
        if token is not None and user["token"] == token:
            user["token"] = None
            is_success = True
    return {
        'is_success': is_success
    }


def auth_register(email, password, name_first, name_last):
    """Checks required for email, password, name_first, name_last to ensure they meet specifications"""
    validate_email(email)
    if src.get_userdata(email)["existing"]:
        raise error.InputError("Email already used")
    if len(password) < 6:
        raise error.InputError("Password too short")
    if 50 >= len(name_first) <= 1:
        raise error.InputError("First name invalid")
    if 50 >= len(name_last) <= 1:
        raise error.InputError("Last name invalid")
    """ First user to be registered is made admin """
    if not users: src.data["admins"].append(0)
    """Add user to database"""
    users.append({"id": len(users),
                  "email": email,
                  "password": auth_token.encrypt_password(password),
                  "fname": name_first,
                  "lname": name_last,
                  "token": None,
                  "handle_str": src.generate_str_handle(name_first, name_last)
                  })
    """Once registered, user is logged in using valid token"""
    return auth_login(email, password)


def auth_passwordreset_request(email):
    """Check if email registered"""
    if not src.get_userdata(email)["existing"]:
        raise error.InputError("Email is not registered!!!")
    message = auth_helper.generate_code()
    """Save message into dictionary with email and code, if email already has code, replace that code with new code"""
    if src.get_auth_resetcode_fromemail(email):
        src.auth_replace_resetcode(email, message)
    else:
        src.data["resetCodes"].append({
            "email": email,
            "code": message,
            "timestamp": datetime.now()
        })
        auth_helper.sendEmail(email, message)


def auth_passwordreset(reset_code, new_password):
    # Checks for new_password
    if len(new_password) < 6:
        raise error.InputError("Password invalid")
    # Checks for valid code : Assumption time-stamp added to invalidate codes after 15minutes
    # Assumption: entry replaced when password changed
    codeDetails = src.get_auth_resetcode_fromcode(reset_code)
    if codeDetails:
        duration = datetime.now() - codeDetails["timestamp"]
        duration_in_secs = duration.total_seconds()
        duration_in_mins = divmod(duration_in_secs, 60)[0]
        if abs(duration_in_mins) < 15:
            src.auth_changepassword(codeDetails["email"], new_password)
            src.auth_replace_resetcode(codeDetails["email"], None)
        else:
            src.auth_replace_resetcode(codeDetails["email"], None)
            raise error.InputError("Reset code expired!")
    else:
        raise error.InputError("Reset code does not exist")

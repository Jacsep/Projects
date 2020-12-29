import pytest

import auth
import other
import source_data
from error import InputError
import datetime

users = source_data.data["users"]


@pytest.fixture()
def test_user():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    auth.auth_register(email, password, "John", "Smith")
    test_user = auth.auth_login(email, password)
    return test_user


def test_register_except():
    other.clear()
    """Testing invalid email"""
    with pytest.raises(InputError):
        auth.auth_register("invalidemail.com", "password123", "John", "Smith")

    """Testing used email address"""
    auth.auth_register("usedemailaddress@hotmail.com", "password123", "John", "Smith")
    with pytest.raises(InputError):
        auth.auth_register("usedemailaddress@hotmail.com", "password123", "Mary", "Smith")

    """Testing bad password"""
    with pytest.raises(InputError):
        auth.auth_register("validemail@hotmail.com", "badpw", "Mary", "Smith")

    """Testing incorrect name_first"""
    with pytest.raises(InputError):
        assert auth.auth_register("validemail@hotmail.com", "password123", "", "Smith")

        """Testing incorrect name_last"""
    with pytest.raises(InputError):
        assert auth.auth_register("validemail@hotmail.com", "password123", "Mary", "")

    other.clear()


def test_logintoken():
    other.clear()
    '''Testing correct {u_id,token} is returned for 3 continuing users'''
    expected = auth.auth_register("validemail@hotmail.com", "goodPassword123", "John", "Smith")
    result = auth.auth_login("validemail@hotmail.com", "goodPassword123")
    assert expected == result
    expected = auth.auth_register("validemail2@hotmail.com", "goodPassword123", "Gary", "Dick")
    result = auth.auth_login("validemail2@hotmail.com", "goodPassword123")
    assert expected == result
    expected = auth.auth_register("validemail3@hotmail.com", "goodPassword123", "Mary", "Smith")
    result = auth.auth_login("validemail3@hotmail.com", "goodPassword123")
    assert expected == result
    other.clear()


def test_login_except():
    users.clear()

    """Testing invalid email"""
    with pytest.raises(InputError):
        auth.auth_login("invalidemail.com", "goodpassword123")

    """Testing email not registered"""
    auth.auth_register("validemail@hotmail.com", "goodPassword123", "John", "Smith")
    with pytest.raises(InputError):
        auth.auth_login("newuser@hotmail.com", "goodPassword123")

    """Testing incorrect password"""
    auth.auth_register("validemail2@hotmail.com", "goodPassword123", "Gary", "Dick")
    with pytest.raises(InputError):
        auth.auth_login("validemail2@hotmail.com", "badPassword123")

    other.clear()


def test_logout_success():
    other.clear()
    """Assuming user logouts we want to assert the correct response is returned"""
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    """Logout should use token to find user successfully and then make token invalid..., and return true"""
    assert auth.auth_logout(token) == {'is_success': True, }
    """Now if we try and logout again, the logout function should fail as token is already invalid, returning false"""
    assert auth.auth_logout(token) == {'is_success': False, }

    other.clear()


def test_authPasswordResetRequest():
    other.clear()
    # Test using invalid email
    with pytest.raises(InputError):
        auth.auth_passwordreset_request("invalidemail@hotmail.com")
    other.clear()


def test_authPasswordResetExcept(test_user):
    # Test using invalid reset_code
    with pytest.raises(InputError):
        auth.auth_passwordreset("fakecode", "newpassword")
    # Test using invalid password, first get valid code
    auth.auth_passwordreset_request("validemail@hotmail.com")
    codeData = source_data.get_auth_resetcode_fromemail("validemail@hotmail.com")
    with pytest.raises(InputError):
        auth.auth_passwordreset(codeData["code"], "badpw")

    other.clear()


def test_authPasswordResetFunc(test_user):
    # Assume user is logged out
    """WHITE-BOX TESTING USED!!!"""
    auth.auth_logout(test_user["token"])
    # Test changing password
    auth.auth_passwordreset_request("validemail@hotmail.com")
    codeData = source_data.get_auth_resetcode_fromemail("validemail@hotmail.com")
    # Using code change password for test_user and save code for future tests
    code1 = codeData["code"]
    auth.auth_passwordreset(codeData["code"], "newpassword")
    # Old password should raise error and login should be successful with new password
    with pytest.raises(InputError):
        auth.auth_login("validemail@hotmail.com", "goodPassword123")
    assert auth.auth_login("validemail@hotmail.com", "newpassword")

    # Test multiple reset_codes and successful password changes for one account
    auth.auth_passwordreset_request("validemail@hotmail.com")
    code2 = codeData["code"]
    # Assert reset code is different, i.e it has changed successfully
    assert code1 != code2
    auth.auth_passwordreset(codeData["code"], "newpassword1")
    # Old password should raise error and login should be successful with new password
    with pytest.raises(InputError):
        auth.auth_login("validemail@hotmail.com", "newpassword")
    assert auth.auth_login("validemail@hotmail.com", "newpassword1")

    # On the topic of white-box test might as well test expiry (15mins)
    auth.auth_passwordreset_request("validemail@hotmail.com")
    # Not elegant but we access the sourceData directly and add 16mins to the timestamp to test if it fails
    code = codeData["code"]
    for codes in source_data.data["resetCodes"]:
        if codes["email"] == "validemail@hotmail.com":
            print("before" + str(codes["timestamp"]))
            codes["timestamp"] = codes["timestamp"] + datetime.timedelta(minutes=16)
            print("after" + str(codes["timestamp"]))
    with pytest.raises(InputError):
        auth.auth_passwordreset(code, "newpassword")

    other.clear()

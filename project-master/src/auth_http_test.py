import requests
import auth
import source_data
import json
from serverurl import url
import pytest
from error import AccessError, InputError

# Create a blueprint user dictionary to test exceptions, replacing each value to correspond to each test
user_blueprint = {
    'email': "userblueprint@hotmail.com",
    'password': "goodpassword",
    'name_first': "blueprint",
    'name_last': "user"
}


def test_auth(url):
    """Tests for auth_register:
     - Invalid email
     - Used email
     - Bad Password
     - Incorrect name_first
     - Incorrect name_last
     """
    user1 = {
        'email': "validemail@hotmail.com",
        'password': "goodpassword",
        'name_first': "John",
        'name_last': "Smith"
    }
    user2 = {
        'email': "validemail1@hotmail.com",
        'password': "goodpassword",
        'name_first': "Mary",
        'name_last': "Smith"
    }
    user3 = {
        'email': "validemail2@hotmail.com",
        'password': "goodpassword",
        'name_first': "Josh",
        'name_last': "Smith"
    }
    # Register 3 users and ensuring the correct token is returned from auth_login
    tkn_register = requests.post(f"{url}/auth/register", json=user1)
    tkn_login = requests.post(f"{url}/auth/login", json={"email": user1["email"], "password": user1["password"]})
    assert tkn_register.json() == tkn_login.json()
    tkn_register = requests.post(f"{url}/auth/register", json=user2)
    tkn_login = requests.post(f"{url}/auth/login", json={"email": user2["email"], "password": user2["password"]})
    assert tkn_register.json() == tkn_login.json()
    tkn_register = requests.post(f"{url}/auth/register", json=user3)
    tkn_login = requests.post(f"{url}/auth/login", json={"email": user3["email"], "password": user3["password"]})
    assert tkn_register.json() == tkn_login.json()

    """Testing invalid email"""
    user_invalid_email = user_blueprint
    user_invalid_email["email"] = "invalidemail.com"
    assert requests.post(f"{url}/auth/register", json=user_invalid_email).json()["code"] == 400

    """Testing used email address, from user1 above, already registered"""
    user_used_email = user_blueprint
    user_used_email["email"] = "validemail@hotmail.com"
    assert requests.post(f"{url}/auth/register", json=user_used_email).json()["code"] == 400

    """Testing bad password"""
    user_bad_pw = user_blueprint
    user_bad_pw["password"] = "badpw"
    assert requests.post(f"{url}/auth/register", json=user_bad_pw).json()["code"] == 400

    """Testing incorrect name_first"""
    user_bad_first = user_blueprint
    user_bad_first["name_first"] = ""
    assert requests.post(f"{url}/auth/register", json=user_bad_first).json()["code"] == 400

    """Testing incorrect name_last"""
    user_bad_last = user_blueprint
    user_bad_last["name_last"] = ""
    assert requests.post(f"{url}/auth/register", json=user_bad_last).json()["code"] == 400

    """
    Exception Tests for auth_login:
         - Invalid email
         - Email not registered
         - Incorrect password
    """
    """Testing invalid email"""
    response = requests.post(f"{url}/auth/login", json={"email": "invalidemail.com", "password": "goodpassword"})
    assert response.json()["code"] == 400

    """Testing email not registered"""
    response = requests.post(f"{url}/auth/login",
                             json={"email": "unregistered@hotmail.com", "password": "goodpassword"})
    assert response.json()["code"] == 400

    """Testing incorrect password/ (from user1 registered in auth_register tests)"""
    response = requests.post(f"{url}/auth/login", json={"email": user1["email"], "password": "thewrongpassword"})
    assert response.json()["code"] == 400

    """Testing auth password reset"""
    """Invalid email for password reset request"""
    response = requests.post(f"{url}/auth/passwordreset/request", json={"email": "invalidemail.com"})
    assert response.json()["code"] == 400

    """invalid reset-code"""
    response = requests.post(f"{url}/auth/passwordreset/reset", json={"reset_code": "fakecode", "new_password": "goodpassword"})
    assert response.json()["code"] == 400
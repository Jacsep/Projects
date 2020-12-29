import auth
import pytest
import channel
import channels
import other
import source_data
import user
from error import *

def test_invalid_first():
    other.clear()
    with pytest.raises(InputError):
        email = "valid@gmail.com"
        password = "Password123"
        auth.auth_register(email, password, "John", "Smith")
        login_dict = auth.auth_login(email, password)
        token = login_dict["token"]
        assert user.user_profile_setname(token, "Ddisjqjsicmnsqwsndjandhsnqjsndkwksjdnqksjdnqikskdskakd", "Josh")

def test_invalid_last():
    other.clear()
    with pytest.raises(InputError):
        email = "valid@gmail.com"
        password = "Password123"
        auth.auth_register(email, password, "John", "Smith")
        login_dict = auth.auth_login(email, password)
        token = login_dict["token"]
        assert user.user_profile_setname(token, "Josh", "Ddisjqjsicmnsqwsndjandhsnqjsndkwksjdnqksjdnqikskdskakd")

def test_valid():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    user.user_profile_setname(token, "William", "Yours")
    user_dict = user.user_profile(token, 0)
    assert ((user_dict["user"])["name_first"] == "William")
    assert ((user_dict["user"])["name_last"] == "Yours")

def test_valid_same():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    user.user_profile_setname(token, "John", "Smith")
    user_dict = user.user_profile(token, 0)
    assert ((user_dict["user"])["name_first"] == "John")
    assert ((user_dict["user"])["name_last"] == "Smith")
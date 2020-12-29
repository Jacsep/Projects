import auth
import pytest
import channel
import channels
import other
import source_data
import user
from error import *

def test_invalid_user():
    other.clear()
    with pytest.raises(InputError):
        email = "valid@gmail.com"
        password = "Password123"
        auth.auth_register(email, password, "John", "Smith")
        login_dict = auth.auth_login(email, password)
        token = login_dict["token"]
        assert user.user_profile(token, 5)

def test_regular():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    returned_dict = user.user_profile(token, 0)
    assert((returned_dict["user"])["u_id"] == 0)
    assert((returned_dict["user"])["email"] == "valid@gmail.com")
    assert((returned_dict["user"])["name_first"] == "John")
    assert((returned_dict["user"])["name_last"] == "Smith")
    # assert(returned_dict["u_id"] == 0)

def test_changed_email():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    returned_dict = user.user_profile(token, 0)
    assert((returned_dict["user"])["email"] == "valid@gmail.com")
    user.user_profile_setemail(token, "anothervalid@gmail.com")
    returned_dict = user.user_profile(token, 0)
    assert((returned_dict["user"])["email"] == "anothervalid@gmail.com")
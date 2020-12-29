import pytest
import auth
import user
from error import InputError, AccessError
import other


@pytest.fixture()
def test_user():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    auth.auth_register(email, password, "John", "Smith")
    test_user = auth.auth_login(email, password)
    return test_user


def test_validhandle(test_user):
    # Test for input error when invalid handle (<3 characters)
    short_handle = "a"
    long_handle = "thisisaverylongbadhandle"
    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user["token"],short_handle)
    # Test for input error when invalid handle (>20 characters)
    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user["token"], long_handle)

    # Test if handle already used
    # Setup to make a new user and give it a custom handle
    handle = "validhandle"
    email = "validemail1@hotmail.com"
    password = "goodPassword123"
    new_user = auth.auth_register(email, password, "Mary", "Smith")
    user.user_profile_sethandle(new_user["token"], handle)
    # Input error when trying to set same handle
    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user["token"], handle)
    other.clear()


def test_set_handle(test_user):
    # Change handle and check handle is changed within profile
    handle = "validhandle"
    user.user_profile_sethandle(test_user["token"], handle)
    user_dict = user.user_profile(test_user["token"], test_user["u_id"])
    assert user_dict["user"]["handle_str"] == handle

    # Check user can change handle again (twice)
    user.user_profile_sethandle(test_user["token"], "new"+handle)
    # Check again handle is correct within profile
    user_dict = user.user_profile(test_user["token"], test_user["u_id"])
    assert user_dict["user"]["handle_str"] == "new" + handle

    other.clear()


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


def test_valid_email(test_user):
    # Test for input error when invalid email
    with pytest.raises(InputError):
        user.user_profile_setemail(test_user["token"], "invalidemail.com.au")

    # Test if email already used
    email = "validemail1@hotmail.com"
    password = "goodPassword123"
    auth.auth_register(email, password, "Mary", "Smith")
    with pytest.raises(InputError):
        user.user_profile_setemail(test_user["token"], "validemail1@hotmail.com")
    other.clear()


def test_set_email(test_user):
    # Change email and check email is changed within profile
    user.user_profile_setemail(test_user["token"], "mynewemail@hotmail.com")
    user_dict = user.user_profile(test_user["token"], test_user["u_id"])
    assert user_dict["user"]["email"] == "mynewemail@hotmail.com"

    # Check user can set back to his old email - "validemail@hotmail.com
    user.user_profile_setemail(test_user["token"], "validemail@hotmail.com")
    # Check again email is correct within profile
    user_dict = user.user_profile(test_user["token"], test_user["u_id"])
    assert user_dict["user"]["email"] == "validemail@hotmail.com"

    other.clear()


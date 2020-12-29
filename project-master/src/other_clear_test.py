import pytest
from other import clear
from source_data import data
from auth import auth_register
from channels import channels_create

""" Testing the use of the clear function on an empty database  """
def test_clear_empty():
    clear()
    for key in data:
        assert len(data[key]) == 0

""" Testing the use of the clear function on a database with a user added """
def test_clear_user_added():
    auth_register("validemail@gmail.com", "somepassword", "Aqib", "Shaikh")
    clear()
    for key in data:
        assert len(data[key]) == 0

""" Testing the use of the clear function on a database with a user and channel added """
def test_clear_channel_added():
    token = auth_register("validemail@gmail.com", "somepassword", "Aqib", "Shaikh")['token']
    channels_create(token, "channel_name", True)
    clear()
    for key in data:
        assert len(data[key]) == 0

if __name__ == '__main__':
    test_clear_empty()
    test_clear_user_added()
    test_clear_channel_added()
    print("All tests passed")

    
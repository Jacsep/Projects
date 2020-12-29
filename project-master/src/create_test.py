import auth
import pytest
import channel
import channels
import source_data
import other
from error import *

# Not sure if I should assert to check if the created channel is in the 
# channels dictionary using listall

def test_name_too_long():
    other.clear()
    with pytest.raises(InputError):
        email = "valid@gmail.com"
        password = "Password123"
        auth.auth_register(email, password, "John", "Smith")
        login_dict = auth.auth_login(email, password)
        token = login_dict["token"]
        assert channels.channels_create(token, "thisnameiswaytoolong123", True)

def test_normal_creation_public():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]

    output = channels.channels_create(token, "channel1", True)
    assert type(next(iter(output.values()))) == int
    list_channels = channels.channels_listall(token)
    assert any("channel1" in d.values() for d in list_channels["channels"])

def test_channel_already_exists():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]

    channels.channels_create(token, "samechannelname", True)
    assert channels.channels_create(token, "samechannelname", True)


def test_normal_creation_private():
    other.clear()
    email = "valid@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    
    output = channels.channels_create(token, "privchannel", False)
    assert type(next(iter(output.values()))) == int
    list_channels = channels.channels_listall(token)
    assert any("privchannel" in d.values() for d in list_channels["channels"])
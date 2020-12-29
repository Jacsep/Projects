import auth
import pytest
import channel
import channels
import other
import source_data
from error import *


def test_empty():
    other.clear()
    email = "validemail@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    
    list_channels = channels.channels_listall(token)
    assert (not list_channels["channels"])


def test_normal():
    other.clear()
    email = "validemail@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]

    channels.channels_create(token, "channel1", True)
    list_channels = channels.channels_listall(token)
    assert any("channel1" in d.values() for d in list_channels["channels"])

    auth.auth_logout(token)
    email = "adiffemail@gmail.com"
    password = "Password123"
    auth.auth_register(email, password, "Lad", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]

    channels.channels_create(token, "diff", True)
    list_channels = channels.channels_listall(token)
    assert any("channel1" in d.values() for d in list_channels["channels"])
    assert any("diff" in d.values() for d in list_channels["channels"])

    channels.channels_create(token, "priv", False)
    list_channels = channels.channels_listall(token)
    assert any("channel1" in d.values() for d in list_channels["channels"])
    assert any("diff" in d.values() for d in list_channels["channels"])
    assert any("priv" in d.values() for d in list_channels["channels"])
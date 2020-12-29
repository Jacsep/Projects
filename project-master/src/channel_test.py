import channel
import channels
import auth
import pytest
import message
from error import InputError
from error import AccessError
import source_data
import other

all_channels = source_data.data["channels"]


def test_channel_invite():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    uid = login_dict["u_id"]

    email2 = "validemail2@hotmail.com"
    password2 = "goodPassword1234"
    login_dict2 = auth.auth_register(email2, password2, "Isaac", "Wadhwa")
    token2 = login_dict2["token"]
    # uid2 = login_dict2["u_id"]

    ''' user 2 is inviting user 1'''
    chan_id = channels.channels_create(token2, "test_channel", True)
    channel.channel_invite(token2, chan_id["channel_id"], uid)

    channel_list = channels.channels_list(token)
    assert any("test_channel" in d.values() for d in channel_list["channels"])


def test_channel_invite_except():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    auth.auth_register(email, password, "John", "Smith")
    login_dict = auth.auth_login(email, password)
    token = login_dict["token"]
    uid = login_dict["u_id"]

    chan_id = channels.channels_create(token, "test_channel", True)

    auth.auth_logout(token)

    email2 = "validemail2@hotmail.com"
    password2 = "goodPassword123"
    login_dict2 = auth.auth_register(email2, password2, "Isaac", "Wadhwa")
    token2 = login_dict2["token"]
    # uid2 = login_dict2["u_id"]

    """ Testing what happens when channel doesnt exist"""
    with pytest.raises(InputError):
        channel.channel_invite(token2, "no_channel", uid)

    """ Testing what happens when user doesnt exist"""
    with pytest.raises(InputError):
        channel.channel_invite(token2, chan_id["channel_id"], "invalid_id")


def test_channel_details():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    uid = login_dict["u_id"]
    chan_id = channels.channels_create(token, "test_channel", True)
    test_dict = {
        'name': 'test_channel',
        'owner_members': [
            {
                'u_id': uid,
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
        'all_members': [
            {
                'u_id': uid,
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
    }
    assert channel.channel_details(token, chan_id["channel_id"]) == test_dict


def test_channel_details_except():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    # uid = login_dict["u_id"]
    # chan_id = channels.channels_create(token, "test_channel", True)

    email2 = "validemail2@hotmail.com"
    password2 = "goodPassword1234"
    login_dict2 = auth.auth_register(email2, password2, "Isaac", "Wadhwa")
    token2 = login_dict2["token"]
    # uid = login_dict2["u_id"]
    chan_id2 = channels.channels_create(token2, "test_channel2", True)

    ''' testing for error msg when invalid channel id'''
    with pytest.raises(InputError):
        channel.channel_details(token, "invalid_channel_id")

    ''' testing for error msg when user isnt part of channel'''
    with pytest.raises(AccessError):
        channel.channel_details(token, chan_id2["channel_id"])


def test_channel_messages():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    chan_details = channels.channels_create(token, "test_channel", True)
    chan_id = chan_details["channel_id"]
    new_msgs = []
    test_dict = {
        'messages': new_msgs,
        'start': 0,
        'end': -1,
    }
    assert channel.channel_messages(token, chan_id, 0) == test_dict

    # add more tests for sent_messages
    msgid1 = message.message_send(token, chan_id, "test_msg1").get("message_id")
    message.message_send(token, chan_id, "test_msg2").get("message_id")
    message.message_send(token, chan_id, "test_msg3").get("message_id")
    chan_msg_dict = channel.channel_messages(token, chan_id, 0)
    chan_messages = chan_msg_dict["messages"]
    # Check 3 messages have been sent, ie. message list has 3 values
    assert (len(chan_messages) == 3)
    # Add some tests for react
    message.message_react(token, msgid1, 1)
    chan_msg_dict = channel.channel_messages(token, chan_id, 0)
    chan_messages = chan_msg_dict["messages"]
    for msgs in chan_messages:
        if msgs["message_id"] == msgid1:
            assert msgs["reacts"][0]["is_this_user_reacted"] is True

def test_channel_messages_except():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    # uid = login_dict["u_id"]
    chan_id = channels.channels_create(token, "test_channel", True)

    email2 = "validemail2@hotmail.com"
    password2 = "goodPassword1234"
    login_dict2 = auth.auth_register(email2, password2, "Isaac", "Wadhwa")
    token2 = login_dict2["token"]
    # uid = login_dict2["u_id"]
    chan_id2 = channels.channels_create(token2, "test_channel2", True)

    ''' tests whether invalid channel returns error'''
    with pytest.raises(InputError):
        channel.channel_messages(token, "invalid_channel_id", 0)

    ''' tests for error when accessing start point past message list total'''
    with pytest.raises(InputError):
        channel.channel_messages(token, chan_id["channel_id"], 1)

    ''' testing for error msg when user isnt part of channel'''
    with pytest.raises(AccessError):
        channel.channel_messages(token, chan_id2["channel_id"], 0)


def test_channel_leave():
    """user1 creates the channel, then leaves the channel"""
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    # uid = login_dict["u_id"]
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    channel.channel_leave(token, channel_id)
    channel.channel_join(token, channel_id)
    channel.channel_leave(token, channel_id)
    assert ((channels.channels_list(token))["channels"] == [])


def test_channel_leave_except():
    """user1 create a public channel, user2 does not join the channel"""
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    # uid1 = login_dict1["u_id"]
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    # uid2 = login_dict2["u_id"]
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]

    """user1 leaves the channel with a wrong channel id"""
    with pytest.raises(InputError):
        channel.channel_leave(token1, channel_id + 1)

    """user2 leaves the channel which he has not joined"""
    with pytest.raises(AccessError):
        channel.channel_leave(token2, channel_id)


def test_channel_join():
    """use1 creates a public channel, user2 joins the channel"""
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    # uid1 = login_dict1["u_id"]
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    # uid2 = login_dict2["u_id"]
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    channel.channel_join(token2, channel_id)
    assert (channels.channels_list(token2))["channels"] == [{'channel_id': channel_id, 'name': 'test_channel'}]


def test_channel_join_except():
    """user1 creates a private channel, user2 does not join the channel"""
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    # uid1 = login_dict1["u_id"]
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    # uid2 = login_dict2["u_id"]
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, False)
    channel_id = channel_id_dict["channel_id"]

    """user2 joins the channel with a wrong channel id"""
    with pytest.raises(InputError):
        channel.channel_join(token2, channel_id + 1)

    """user2 joins the channel but it is private"""
    with pytest.raises(AccessError):
        channel.channel_join(token2, channel_id)

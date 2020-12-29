from datetime import datetime

import pytest

import auth
import channel
import channels
import message
import other
import source_data
from error import AccessError
from error import InputError
from source_data import token2id

all_users = source_data.data["users"]
all_channels = source_data.data["channels"]
all_messages = source_data.data["messages"]


def test_message_send():
    other.clear()
    # Test one user send a message in a channel.
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token1 = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    assert message.message_send(token1, channel_id, message1) == {'message_id': 0}


def test_message_send_except():
    other.clear()
    # User1 create the channel, user2 does not join.
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "A" * 1001
    message2 = "This is first message."
    with pytest.raises(InputError):
        message.message_send(token1, channel_id, message1)

    with pytest.raises(AccessError):
        message.message_send(token2, channel_id, message2)


def test_message_remove():
    other.clear()
    # Test one user remove a message in a channel.
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message2 = "This is second message."

    # Test for the authorised user is the owner of the channel.
    message.message_send(token, channel_id, message1)
    message.message_remove(token, channel_id)
    assert all_messages == []
    assert all_channels[0].get('messages') == []

    # Test for the authorised user sent the message.
    message.message_send(token, channel_id, message2)
    channel.channel_leave(token, channel_id)
    message.message_remove(token, channel_id)
    assert all_messages == []
    assert all_channels[0].get('messages') == []


def test_message_remove_except():
    other.clear()
    # User1 and user2 are registered, no message is sent.
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]

    # Remove a message that no longer exist from a channel.
    with pytest.raises(InputError):
        message.message_remove(token1, 0)

    # Test for the access error.
    message1 = "This is fist message."
    message.message_send(token1, channel_id, message1)
    with pytest.raises(AccessError):
        message.message_remove(token2, 0)


def test_message_edit():
    other.clear()
    # Test one user edit a message in a channel.
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message2 = "This is second message."
    message3 = "This is third message."
    message4 = ""
    message.message_send(token, channel_id, message1)

    # Test for the authorised user is the owner of the channel.
    message.message_edit(token, channel_id, message2)
    assert all_messages[0].get('message') == message2
    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('message') == message2

    # Test for the authorised user edit the message.
    channel.channel_leave(token, channel_id)
    message.message_edit(token, channel_id, message3)
    assert all_messages[0].get('message') == message3
    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('message') == message3

    # Test for edit the message with an empty string.
    message.message_edit(token, channel_id, message4)
    assert all_messages == []
    assert all_channels[0].get('messages') == []


def test_message_edit_except():
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is fist message."
    message.message_send(token1, channel_id, message1)

    # Test for the AccessError.
    with pytest.raises(AccessError):
        message.message_edit(token2, channel_id, "A")


def test_message_sendlater():
    other.clear()
    # Test one user send a message later in a channel.
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    future = int(datetime.now().timestamp() + 86400)
    assert message.message_sendlater(token, channel_id, message1, future) == {'message_id': 0}


def test_message_sendlater_except():
    # User1 create the channel, user2 does not join.
    other.clear()
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message2 = "A" * 1001
    future = int(datetime.now().timestamp() + 86400)
    past = int(datetime.now().timestamp() - 86400)

    # InputError: Invalid Channel_ID.
    with pytest.raises(InputError):
        message.message_sendlater(token1, channel_id + 10, message1, future)

    # InputError: More than 1000 characters.
    with pytest.raises(InputError):
        message.message_sendlater(token1, channel_id, message2, future)

    # InputError: Time in the past.
    with pytest.raises(InputError):
        message.message_sendlater(token1, channel_id, message1, past)

    # AccessError: User not in channel.
    with pytest.raises(AccessError):
        message.message_sendlater(token2, channel_id, message1, future)


def test_message_react():
    other.clear()
    # Test two users react to a message in a channel.
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    u_id1 = token2id(token1)
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    u_id2 = token2id(token2)
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    channel.channel_join(token2, channel_id)
    message1 = "This is first message."
    message.message_send(token1, channel_id, message1)
    message.message_react(token1, 0, 1)
    assert all_messages[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': False}]
    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': False}]
    message.message_react(token2, 0, 1)
    assert all_messages[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1, u_id2], 'is_this_user_reacted': False}]
    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1, u_id2], 'is_this_user_reacted': False}]


def test_message_react_except():
    other.clear()
    # User1 creates the channel and send a message, user2 join the channel.
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    channel.channel_join(token2, channel_id)
    message1 = "This is first message."
    message.message_send(token1, channel_id, message1)

    # Message not in authorised channel.
    with pytest.raises(InputError):
        message.message_react(token1, 1, 1)

    with pytest.raises(InputError):
        message.message_react(token2, 1, 1)

    # Invalid message_id.
    with pytest.raises(InputError):
        message.message_react(token1, 0, 0)

    with pytest.raises(InputError):
        message.message_react(token2, 0, 2)

    # Already reacted.
    message.message_react(token1, 0, 1)
    with pytest.raises(InputError):
        message.message_react(token1, 0, 1)


def test_message_unreact():
    other.clear()
    # Test two users unreact to a message in a channel.
    email1 = "validemail@hotmail.com"
    email2 = "validemail1@hotmail.com"
    password1 = "goodPassword123"
    password2 = "goodPassword1234"
    login_dict1 = auth.auth_register(email1, password1, "John", "Smith")
    token1 = login_dict1["token"]
    u_id1 = token2id(token1)
    login_dict2 = auth.auth_register(email2, password2, "Justin", "Bieber")
    token2 = login_dict2["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    channel.channel_join(token2, channel_id)
    message1 = "This is first message."
    message.message_send(token1, channel_id, message1)
    message.message_react(token1, 0, 1)
    message.message_react(token2, 0, 1)
    message.message_unreact(token2, 0, 1)
    # User2 unreacts.
    assert all_messages[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': False}]

    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('reacts') == [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': False}]

    # User1 unreacts.
    message.message_unreact(token1, 0, 1)
    assert all_messages[0].get('reacts') == [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}]

    messages_list = all_channels[0].get('messages')
    assert messages_list[0].get('reacts') == [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}]


def test_message_unreact_except():
    other.clear()
    # User creates a channel and reacts to a message.
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token1 = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token1, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message2 = "This is second message."
    message.message_send(token1, channel_id, message1)
    message.message_send(token1, channel_id, message2)
    message.message_react(token1, 0, 1)

    # Invalid message_id.
    with pytest.raises(InputError):
        message.message_unreact(token1, 2, 1)

    with pytest.raises(InputError):
        message.message_unreact(token1, 3, 1)

    # Invalid react_id.
    with pytest.raises(InputError):
        message.message_unreact(token1, 0, 0)

    with pytest.raises(InputError):
        message.message_unreact(token1, 0, 2)

    # Message does not contain active react.
    with pytest.raises(InputError):
        message.message_unreact(token1, 1, 1)


def test_message_pin():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message_ids = message.message_send(token, channel_id, message1)
    message_id = message_ids['message_id']
    message.message_pin(token, message_id)
    assert all_messages[0].get('is_pinned') == True


def test_message_unpin_except():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message.message_send(token, channel_id, message1)
    message_id = all_messages[0].get('message_id')
    message.message_pin(token, message_id)
    message_id = "invalid ID"
    # test invalid message id
    with pytest.raises(InputError):
        message.message_unpin(token, message_id)
    message_id = all_messages[0].get('message_id')
    message_get = all_messages[0]
    message_get['is_pinned'] = False
    # test if message is already unpinned
    with pytest.raises(InputError):
        message.message_unpin(token, message_id)
    message.message_pin(token, message_id)
    channel.channel_leave(token, channel_id)
    # test invalid channel id
    with pytest.raises(AccessError):
        message.message_unpin(token, message_id)
    channel.channel_join(token, channel_id)
    # test not owner
    with pytest.raises(AccessError):
        message.message_unpin(token, message_id)


def test_message_unpin():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message_ids = message.message_send(token, channel_id, message1)
    message_id = message_ids['message_id']
    message.message_pin(token, message_id)
    message.message_unpin(token, message_id)
    assert all_messages[0].get('is_pinned') == False


def test_message_pin_except():
    other.clear()
    email = "validemail@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "John", "Smith")
    token = login_dict["token"]
    channel_name = "test_channel"
    channel_id_dict = channels.channels_create(token, channel_name, True)
    channel_id = channel_id_dict["channel_id"]
    message1 = "This is first message."
    message.message_send(token, channel_id, message1)
    message_id = "invalid ID"
    # test invalid message id
    with pytest.raises(InputError):
        message.message_pin(token, message_id)
    message_get = all_messages[0]
    message_get['is_pinned'] = True
    message_id = all_messages[0].get('message_id')

    # test if message is already pinned
    with pytest.raises(InputError):
        message.message_pin(token, message_id)
    message_get['is_pinned'] = False
    channel.channel_leave(token, channel_id)
    # test invalid channel id
    with pytest.raises(AccessError):
        message.message_pin(token, message_id)
    channel.channel_join(token, channel_id)
    # test not owner
    with pytest.raises(AccessError):
        message.message_pin(token, message_id)

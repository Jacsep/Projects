import channel
import channels
import auth
import message
import pytest
from error import InputError
from error import AccessError
import source_data
import other

all_users = source_data.data["users"]
all_channels = source_data.data["channels"]
all_messages = source_data.data["messages"]


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
    email = "validemail1@hotmail.com"
    password = "goodPassword123"
    login_dict = auth.auth_register(email, password, "Mary", "Smith")
    token2 = login_dict["token"]
    channel.channel_join(token2, channel_id)
    with pytest.raises(AccessError):
        message.message_pin(token, message_id)

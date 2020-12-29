import requests
import json
from serverurl import url
import pytest
from requests.exceptions import HTTPError
from datetime import datetime

user1 = {
    'email': "validemail@hotmail.com",
    'password': "goodpassword",
    'name_first': "John",
    'name_last': "Smith"
}

user2 = {
    'email': "validemail1@hotmail.com",
    'password': "goodpassword",
    'name_first': "Mary",
    'name_last': "Smith"
}


def test_valid_normal_message_send(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]

    chan_id = channel_create_helper(url, token)
    mess_id1 = message_send_helper(url, token, chan_id, "Kanye West is the best")
    time = int(datetime.now().timestamp())
    message_list = channel_messages_help(url, token, chan_id, 0)

    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
            'is_pinned': False
        }
    ]


def test_message_send_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]

    chan_id = channel_create_helper(url, token1)

    invalid_message = "w" * 1234
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/send", json={
            'token': token1,
            'channel_id': chan_id,
            'message': invalid_message
        }).raise_for_status()

    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/send", json={
            'token': 123451,
            'channel_id': chan_id,
            'message': "Valid message"
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/send", json={
            'token': token2,
            'channel_id': chan_id,
            'message': "Valid message"
        }).raise_for_status()


def test_message_remove_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/remove", json={
            'token': token1,
            'message_id': 1234
        }).raise_for_status()

    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, "Kanye West is the best")

    with pytest.raises(HTTPError):
        requests.delete(f"{url}/message/remove", json={
            'token': "1234",
            'message_id': mess_id1
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    requests.post(f"{url}/channel/join", json={
        'token': token2,
        'channel_id': chan_id
    })

    with pytest.raises(HTTPError):
        requests.delete(f"{url}/message/remove", json={
            'token': token2,
            'message_id': mess_id1
        }).raise_for_status()


def test_valid_normal_message_remove(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    u_id1 = register_user.json()["u_id"]

    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, "Kanye West is the best")
    time = int(datetime.now().timestamp())

    message_list = channel_messages_help(url, token1, chan_id, 0)

    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
            'is_pinned': False
        }
    ]

    requests.delete(f"{url}/message/remove", json={
        'token': token1,
        'message_id': mess_id1
    })

    message_list = channel_messages_help(url, token1, chan_id, 0)

    assert message_list == []


def test_message_edit_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]

    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, "Kanye West is the best")

    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/edit", json={
            'token': "1234",
            'message_id': mess_id1,
            'message': "Kanye West is not the best",
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    requests.post(f"{url}/channel/join", json={
        'token': token2,
        'channel_id': chan_id
    })

    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/edit", json={
            'token': token2,
            'message_id': mess_id1,
            'message': "Kanye West is not the best",
        }).raise_for_status()


def test_normal_valid_message_edit(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    u_id1 = register_user.json()["u_id"]

    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, "Kanye West is the best")
    time = int(datetime.now().timestamp())

    message_list = channel_messages_help(url, token1, chan_id, 0)

    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
            'is_pinned': False
        }
    ]

    requests.put(f"{url}/message/edit", json={
        'token': token1,
        'message_id': mess_id1,
        'message': "Kanye is not the best",
    })

    message_list1 = channel_messages_help(url, token1, chan_id, 0)

    assert message_list1 == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye is not the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
            'is_pinned': False
        }
    ]
    
# Iteration3 tests.
def test_valid_normal_message_sendlater(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]
    msg_str = "Kanye West is the best"
    time_sent = int(datetime.now().timestamp()) + 60
    chan_id = channel_create_helper(url, token)
    mess_id1 = message_sendlater_helper(url, token, chan_id, msg_str, time_sent)
    message_list = channel_messages_help(url, token, chan_id, 0)

    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': msg_str,
            'time_created': time_sent,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
        }
    ]

def test_message_sendlater_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    
    chan_id = channel_create_helper(url, token1)
    valid_message = 'Valid message.'
    invalid_message = "w" * 1234
    time1 = int(datetime.now().timestamp()) + 60
    time2 = int(datetime.now().timestamp()) - 60
    
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/sendlater", json={
            'token': token1,
            'channel_id': chan_id + 100,
            'message': valid_message,
            'time_sent': time1
        }).raise_for_status()

    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/sendlater", json={
            'token': token1,
            'channel_id': chan_id,
            'message': invalid_message,
            'time_sent': time1
        }).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/sendlater", json={
            'token': 123451,
            'channel_id': chan_id,
            'message': valid_message,
            'time_sent': time1
        }).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/sendlater", json={
            'token': token1,
            'channel_id': chan_id,
            'message': valid_message,
            'time_sent': time2
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/send", json={
            'token': token2,
            'channel_id': chan_id,
            'message': "Valid message",
            'time_sent': time1
        }).raise_for_status()

def test_normal_valid_message_react(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    u_id1 = register_user.json()["u_id"]
    msg_str = "Kanye West is the best"
    react_id = 1
    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, msg_str)
    message_react_helper(url, token1, mess_id1, react_id)
    time = int(datetime.now().timestamp())

    message_list = channel_messages_help(url, token1, chan_id, 0)
    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': True}],
            'is_pinned': False
        }
    ]

def test_message_react_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    msg_str = "Kanye West is the best"
    react_id = 1
    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, msg_str)

    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/react", json={
            'token': token1,
            'message_id': mess_id1 + 10,
            'react_id': react_id
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/react", json={
            'token': token2,
            'message_id': mess_id1,
            'react_id': react_id
        }).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/react", json={
            'token': token2,
            'message_id': mess_id1,
            'react_id': react_id + 1
        }).raise_for_status()
    
    message_react_helper(url, token1, mess_id1, react_id)
    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/react", json={
            'token': token1,
            'message_id': mess_id1,
            'react_id': react_id
        }).raise_for_status()
    
def test_normal_valid_message_unreact(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    u_id1 = register_user.json()["u_id"]
    msg_str = "Kanye West is the best"
    react_id = 1
    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, msg_str)
    message_react_helper(url, token1, mess_id1, react_id)
    time = int(datetime.now().timestamp())

    message_list = channel_messages_help(url, token1, chan_id, 0)

    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [u_id1], 'is_this_user_reacted': True}],
            'is_pinned': False
        }
    ]
    
    message_unreact_helper(url, token1, mess_id1, react_id)
    message_list = channel_messages_help(url, token1, chan_id, 0)
    
    assert message_list == [
        {
            'u_id': u_id1,
            'message_id': mess_id1,
            'channel_id': chan_id,
            'message': "Kanye West is the best",
            'time_created': time,
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
            'is_pinned': False
        }
    ]
    
def test_message_unreact_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    msg_str = "Kanye West is the best"
    react_id = 1
    chan_id = channel_create_helper(url, token1)
    mess_id1 = message_send_helper(url, token1, chan_id, msg_str)
    
    message_react_helper(url, token1, mess_id1, react_id)
    
    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/unreact", json={
            'token': token1,
            'message_id': mess_id1 + 10,
            'react_id': react_id
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/unreact", json={
            'token': token2,
            'message_id': mess_id1,
            'react_id': react_id
        }).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/unreact", json={
            'token': token2,
            'message_id': mess_id1,
            'react_id': react_id + 1
        }).raise_for_status()
    
    message_unreact_helper(url, token1, mess_id1, react_id)
    with pytest.raises(HTTPError):
        requests.put(f"{url}/message/unreact", json={
            'token': token1,
            'message_id': mess_id1,
            'react_id': react_id
        }).raise_for_status()


def test_message_pin_except(url):
    requests.delete(f"{url}/clear")
    # Setting up user to perform tests for message pin
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]
    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]
    # Create channel and send a simple message
    chan_id = channel_create_helper(url, token)
    mess_id1 = message_send_helper(url, token, chan_id, "Kanye West is the best")
    # IE: Invalid message_id
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/pin", json={'token': token, "message_id": 1000000}).raise_for_status()
    # AE: User not in channel where message is sent
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/pin", json={'token': token2, "message_id": mess_id1}).raise_for_status()
    # User not owner
    requests.post(f"{url}/channel/join", json={'token': token2, "channel_id": chan_id})
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/pin", json={'token': token2, "message_id": mess_id1}).raise_for_status()
    # IE: Already pinned
    requests.post(f"{url}/message/pin", json={'token': token, "message_id": mess_id1})
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/pin", json={'token': token, "message_id": mess_id1}).raise_for_status()


def test_message_unpin_except(url):
    requests.delete(f"{url}/clear")
    # Setting up user to perform tests for message pin
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]
    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]
    # Create channel and send a simple message
    chan_id = channel_create_helper(url, token)
    mess_id1 = message_send_helper(url, token, chan_id, "Kanye West is the best")
    # IE: Invalid message_id
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/unpin", json={'token': token, "message_id": 1000000}).raise_for_status()
    # AE: User not in channel where message is sent
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/unpin", json={'token': token2, "message_id": mess_id1}).raise_for_status()
    # User not owner
    requests.post(f"{url}/channel/join", json={'token': token2, "channel_id": chan_id})
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/unpin", json={'token': token2, "message_id": mess_id1}).raise_for_status()
    # IE: Already unpinned
    with pytest.raises(HTTPError):
        requests.post(f"{url}/message/unpin", json={'token': token, "message_id": mess_id1}).raise_for_status()


def test_message_pin(url):
    requests.delete(f"{url}/clear")
    # Setting up user to perform tests for message pin
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]
    # Create channel and send a simple message
    chan_id = channel_create_helper(url, token)
    mess_id1 = message_send_helper(url, token, chan_id, "Kanye West is the best")
    # Now pin the message in the channel
    requests.post(f"{url}/message/pin", json={'token': token, "message_id": mess_id1})
    # Using channel message we now check the message was correctly pinned
    message_list = channel_messages_help(url, token, chan_id, 0)
    # Assert messages were cleared and only one message was sent
    assert (len(message_list) == 1)
    # Get the value of is_pinned for the single message in channel and assert it is true
    assert message_list[0]["is_pinned"]
    # Now unpin the message and check the status is False, using same steps
    requests.post(f"{url}/message/unpin", json={'token': token, "message_id": mess_id1})
    message_list = channel_messages_help(url, token, chan_id, 0)
    assert (len(message_list) == 1)
    assert not message_list[0]["is_pinned"]


def channel_create_helper(url, token):
    channel1 = {
        'token': token,
        'name': "valid_channel",
        'is_public': True
    }

    create_channel = requests.post(f"{url}/channels/create", json=channel1)
    chan_id = create_channel.json()["channel_id"]
    return chan_id


def message_send_helper(url, token, chan_id, msg_str):
    message_sent = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': chan_id,
        'message': msg_str
    })
    mess_id1 = message_sent.json()["message_id"]
    return mess_id1
    
def message_sendlater_helper(url, token, chan_id, msg_str, time_sent):
    message_sent = requests.post(f"{url}/message/sendlater", json={
        'token': token,
        'channel_id': chan_id,
        'message': msg_str,
        'time_sent': time_sent,
    })
    mess_id1 = message_sent.json()["message_id"]
    return mess_id1

def message_react_helper(url, token, message_id, react_id):
    requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    return

def message_unreact_helper(url, token, message_id, react_id):
    requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    return

def channel_messages_help(url, token, chan_id, start):
    channel_messages = requests.get(f"{url}/channel/messages", params={
        'token': token,
        'channel_id': chan_id,
        'start': start
    })

    message_list = (channel_messages.json())["messages"]
    return message_list

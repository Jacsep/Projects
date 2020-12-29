import requests
import json
from serverurl import url

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

def test_clear(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]
    

    channel1 = {
        'token': token,
        'name': "valid_channel",
        'is_public': True
    }

    requests.post(f"{url}/channels/create", json=channel1).json()

    requests.delete(f"{url}/clear")

    channels_list = requests.get(f"{url}/channels/listall", params={
        'token': token
    })
    channels_list = channels_list.json()["channels"]
    assert channels_list == []

    user_list = requests.get(f"{url}/users/all", params={
        'token': token
    })
    user_list = user_list.json()["users"]
    assert user_list == []

def test_users_all_multiple(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token1 = register_user.json()["token"]
    id1 = register_user.json()["u_id"]
    profile = requests.get(f"{url}/user/profile", params={
        'token': token1,
        'u_id': id1
    })
    profile_details = profile.json()
    handle1 = (profile_details["user"])["handle_str"]


    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]
    id2 = register_user.json()["u_id"]
    profile = requests.get(f"{url}/user/profile", params={
        'token': token2,
        'u_id': id2
    })
    profile_details = profile.json()
    handle2 = (profile_details["user"])["handle_str"]


    user_list1 = requests.get(f"{url}/users/all", params={
        'token': token1
    })
    user_list1 = user_list1.json()["users"]

    user_list2 = requests.get(f"{url}/users/all", params={
        'token': token2
    })
    user_list2 = user_list2.json()["users"]

    assert user_list1 == user_list2

    assert user_list1 == [
        {
            'u_id': id1,
            'email': "validemail@hotmail.com",
            'name_first': "John",
            'name_last': "Smith",
            'handle_str': handle1
        },
        {
            'u_id': id2,
            'email': "validemail1@hotmail.com",
            'name_first': "Mary",
            'name_last': "Smith",
            'handle_str': handle2
        }
    ]

def test_search_no_matching(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]

    channel1 = {
        'token': token,
        'name': "valid_channel",
        'is_public': True
    }

    create_channel = requests.post(f"{url}/channels/create", json=channel1)
    chan_id = create_channel.json()["channel_id"]

    requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': chan_id,
        'message': "Miami Heat champions 2021"
    }).json()

    requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': chan_id,
        'message': "NBA Youngboy"
    }).json()

    matching_strings = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': "orange"
    })
    matching_strings = matching_strings.json()["messages"]
    assert matching_strings == []

def test_search_matching(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]

    channel1 = {
        'token': token,
        'name': "valid_channel",
        'is_public': True
    }

    create_channel = requests.post(f"{url}/channels/create", json=channel1)
    chan_id = create_channel.json()["channel_id"]

    requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': chan_id,
        'message': "Miami Heat NBA champions 2021"
    }).json()

    requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': chan_id,
        'message': "NBA Youngboy"
    }).json()

    matching_strings = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': "NBA"
    })
    matching_strings = matching_strings.json()["messages"]

    channel_messages = requests.get(f"{url}/channel/messages", params={
        'token': token,
        'channel_id': chan_id,
        'start': 0
    })
    message_list = channel_messages.json()["messages"]



    assert message_list[::-1] == matching_strings
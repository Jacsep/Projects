""" HTTP tests (general and exceptions) for standup functions """
from serverurl import url
import requests
import pytest
import json
import time
from datetime import datetime
from requests.exceptions import HTTPError


def test_standup_start_errors(url):
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    with pytest.raises(HTTPError):
        requests.post(f"{url}/standup/start", json={
            'token': user_data[0]["token"],
            'channel_id': 5,
            'length': 21
        }).raise_for_status()

    standup_start = int(datetime.now().timestamp())
    standup_finish = standup_start + 10

    return_dict = requests.post(f"{url}/standup/start", json={
        'token': user_data[0]["token"],
        'channel_id': 0,
        'length': 10
    })

    time_dict = return_dict.json()

    assert time_dict == {
        'time_finish': standup_finish
    }

    with pytest.raises(HTTPError):
        requests.post(f"{url}/standup/start", json={
            'token': user_data[0]["token"],
            'channel_id': 0,
            'length': 12
        }).raise_for_status()


##################################
### standup_active http tests ###
#################################
# Parameters: (token, channel_id)
# Return: {is_active, time_finish}
# Methods: GET

def test_http_standup_active_general(url):
    """ Tests if function returns whether a standup is active, and what time it finishes """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    resp = requests.post(f"{url}/standup/start", json=standup_start_args)
    time_fin = json.loads(resp.text)["time_finish"]
    
    # If standup is active, expected is that is_active is True and time_finish is return from start
    expected = {
        "is_active": True,
        "time_finish": time_fin
    }

    # User 0 checking if standup is active in channel 0
    standup_active_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/standup/active", params=standup_active_args)
    # Asserting that result was expected
    assert json.loads(resp.text) == expected

def test_http_standup_active_inactive_standup(url):
    """ Tests if function returns None if no standup is currently active """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # If no standup is active, expected is that is_active is False and time_finish is None
    expected = {
        "is_active": False,
        "time_finish": None
    }

    # User 0 checking if standup is active in channel 0
    standup_active_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/standup/active", params=standup_active_args)
    # Asserting that result was expected
    assert json.loads(resp.text) == expected

def test_http_standup_active_invalid_token(url):
    """ Tests if error is raised when function is called from user who has logged out """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # Logging user 0 out
    logout_args = {
        "token": user_data[0]["token"]
    }
    requests.post(f"{url}/auth/logout", json=logout_args)

    # User 0, who has logged out, checking if standup is active in channel 0
    standup_active_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/standup/active", params=standup_active_args)
    # Asserting that an error was raised
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_active_invalid_channel(url):
    """ Tests if error is raised when function is called for an invalid channel """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 0 checking if standup is active in nonexistent channel 1
    standup_active_args = {
        "token": user_data[0]["token"],
        "channel_id": 1
    }
    resp = requests.get(f"{url}/standup/active", params=standup_active_args)
    # Asserting that an error was raised
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_active_not_member(url):
    """ Tests if error is raised if authorised user is not a member of channel """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 2, not in channel 0, checking if standup is active in channel 0
    standup_active_args = {
        "token": user_data[2]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/standup/active", params=standup_active_args)
    # Asserting that an error was raised
    assert json.loads(resp.text)["code"] == 400

###############################
### standup_send http tests ###
###############################
# Parameters: (token, channel_id, message)
# Return: {}
# Methods: POST

def test_http_standup_send_general(url):
    """ Tests if a message is sent to get buffered in the standup queue """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    resp = requests.post(f"{url}/standup/start", json=standup_start_args)
    
    # User 1 sending a message in standup 
    standup_send_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "message": "Some message"
    }
    requests.post(f"{url}/standup/send", json=standup_send_args)
    
    # Sleeping (waiting) for 3 seconds so that standup ends and messages are packaged and sent
    time.sleep(3)
    
    # User 0 searching for packaged message for message sent during standup
    search_args = {
        "token": user_data[0]["token"],
        "query_str": "Some message"
    }
    resp = requests.get(f"{url}/search", params=search_args)
    search_return = json.loads(resp.text)["messages"]
    
    # Asserting that one message was returned from search function
    assert len(search_return) == 1

def test_http_standup_send_invalid_token(url):
    """ Tests if error is raised when function is called from user who has logged out """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    requests.post(f"{url}/standup/start", json=standup_start_args)
    
    # Logging user 1 out
    logout_args = {
        "token": user_data[1]["token"]
    }
    requests.post(f"{url}/auth/logout", json=logout_args)

    # User 1, logged out, attempting to send a message during a standup 
    standup_send_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "message": "Some message"
    }
    resp = requests.post(f"{url}/standup/send", json=standup_send_args)
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_send_invalid_channel(url):
    """ Tests if error is raised when function is called for an invalid channel """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    requests.post(f"{url}/standup/start", json=standup_start_args)

    # User 1 attempting to send a standup message to a nonexistent channel 1
    standup_send_args = {
        "token": user_data[1]["token"],
        "channel_id": 1,
        "message": "Some message"
    }
    resp = requests.post(f"{url}/standup/send", json=standup_send_args)
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_send_exceeding_len(url):
    """ Tests if error is raised if message is more than 1000 chars long """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    requests.post(f"{url}/standup/start", json=standup_start_args)

    # User 1 attempting to send a msg over 1000 chars during standup
    standup_send_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "message": "Hello! " * 144
    }
    resp = requests.post(f"{url}/standup/send", json=standup_send_args)
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_send_inactive_standup(url):
    """ Tests if error is raised if there is no standup running in the channel """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 attempting to send a standup message without active standup
    standup_send_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "message": "Some message"
    }
    resp = requests.post(f"{url}/standup/send", json=standup_send_args)
    assert json.loads(resp.text)["code"] == 400

def test_http_standup_send_not_member(url):
    """ Tests if error is raised if authorised user is not a member of channel """
    # Initialising data
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup_start_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "length": 2
    }
    requests.post(f"{url}/standup/start", json=standup_start_args)

    # User 2 attempting to send a standup message to channel 1, which they are not part of
    standup_send_args = {
        "token": user_data[2]["token"],
        "channel_id": channel_id,
        "message": "Some message"
    }
    resp = requests.post(f"{url}/standup/send", json=standup_send_args)
    assert json.loads(resp.text)["code"] == 400

#######################
### Initialise data ###
#######################

def initialise_data(url):
    """ 
    Initialises dummy data
    Registers users 0, 1 and 2
    User 0 creates a channel
    User 1 joins the channel
    """
    # Clearing previous date
    requests.delete(f"{url}/clear")

    # Registering user 0
    reg_args = {
        'email': "validemail0@hotmail.com",
        'password': "goodpassword",
        'name_first': "Zero",
        'name_last': "Jiro"
    }
    resp = requests.post(f"{url}/auth/register", json=reg_args)
    u_0 = json.loads(resp.text)

    # Registering user 1
    reg_args = {
        'email': "validemail1@hotmail.com",
        'password': "goodpassword",
        'name_first': "One",
        'name_last': "Ichi"
    }
    resp = requests.post(f"{url}/auth/register", json=reg_args)
    u_1 = json.loads(resp.text)

    # Registering user 2
    reg_args = {
        'email': "validemail2@hotmail.com",
        'password': "goodpassword",
        'name_first': "Two",
        'name_last': "Ni"
    }
    resp = requests.post(f"{url}/auth/register", json=reg_args)
    u_2 = json.loads(resp.text)

    # User 0 creating channel 0
    ch_create_args = {
        'token': u_0["token"],
        'name': "channel_name",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=ch_create_args)
    channel_id = json.loads(resp.text)["channel_id"]

    # User 1 joining channel 0
    ch_join_args = {
        'token': u_1["token"],
        'channel_id': channel_id
    }
    requests.post(f"{url}/channel/join", json=ch_join_args)

    return {
        "users": [u_0, u_1, u_2],
        "channel_id": channel_id
    }

""" Tests (general and exceptions) for standup """
from error import InputError, AccessError
import channels
import channel
import standup
import pytest
import other
import auth
import time
from datetime import datetime
import source_data

def test_invalid_channel():
    initial_data = initialise_data()
    user_data = initial_data["users"]
    with pytest.raises(InputError):
        assert standup.standup_start(user_data[0]["token"], 5, 21)

def test_existing_standup():
    initial_data = initialise_data()
    user_data = initial_data["users"]
    standup_start = int(datetime.now().timestamp())
    standup_finish = standup_start + 10
    assert standup.standup_start(user_data[0]["token"], 0, 10) == {
        'time_finish': standup_finish
    }
    matching_channel = source_data.get_channelinfo(0)
    assert matching_channel["standup"]["is_active"] == True

    with pytest.raises(InputError):
        standup.standup_start(user_data[0]["token"], 0, 8)


#####################################
### standup_active test functions ###
#####################################
# Parameters: (token, channel_id)
# Return: {is_active, time_finish}

def test_standup_active_general():
    """ Tests if function returns whether a standup is active, and what time it finishes """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    time_fin = standup.standup_start(user_data[0]["token"], channel_id, 2)["time_finish"]
    
    # Expected is that is_active is True and time_finish is return value from standup start
    expected = {
        "is_active": True,
        "time_finish": time_fin
    }

    # Asserting that standup is active in channel 0
    assert standup.standup_active(user_data[0]["token"], channel_id) == expected

def test_standup_active_inactive_standup():
    """ Tests if function returns None if no standup is currently active """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # If no standup is active, expected that is_active is False and time_finish is None
    expected = {
        "is_active": False,
        "time_finish": None
    }

    # Asserting that no standup is active in channel 0
    assert standup.standup_active(user_data[0]["token"], channel_id) == expected

def test_standup_active_invalid_token():
    """ Tests if error is raised when function is called from user who has logged out """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # Logging user 0 out, thus setting token to None
    auth.auth_logout(user_data[0]["token"])

    # Asserting that error is raised when user 0, who has logged out calls function
    with pytest.raises(AccessError):
        assert standup.standup_active(user_data[0]["token"], channel_id)

def test_standup_active_invalid_channel():
    """ Tests if error is raised when function is called for an invalid channel """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]

    # Asserting that error is raised when user 0 calls function for nonexistent channel
    with pytest.raises(InputError):
        assert standup.standup_active(user_data[0]["token"], 1)

def test_standup_active_not_member():
    """ Tests if error is raised if authorised user is not a member of channel """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # Asserting that error is raised when user 2, not in ch, checks if standup is active in ch
    with pytest.raises(AccessError):
        standup.standup_active(user_data[2]["token"], channel_id)

###################################
### standup_send test functions ###
###################################
# Parameters: (token, channel_id, message)
# Return: {}

def test_standup_send_general():
    """ Tests if a message is sent to get buffered in the standup queue """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]
    
    # User 0 starting a standup for 2 seconds in channel 0
    standup.standup_start(user_data[0]["token"], channel_id, 2)
    
    # User 1 sending a message in standup 
    standup.standup_send(user_data[1]["token"], channel_id, "Some message")
    
    # Sleeping (waiting) for 3 seconds so that standup ends and messages are packaged and sent
    time.sleep(3)
    
    # Searching for section/all of packaged message for message sent during standup
    search_return = other.search(user_data[0]["token"], "Some message")["messages"]
    
    # Asserting that one message was returned from search function
    assert len(search_return) == 1

def test_standup_send_invalid_token():
    """ Tests if error is raised when function is called from user who has logged out """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    standup.standup_start(user_data[0]["token"], channel_id, 2)

    # Logging user 0 out
    auth.auth_logout(user_data[0]["token"])

    # Asserting that error is raised when user 0, who has logged out, sends standup message
    with pytest.raises(AccessError):
        assert standup.standup_send(user_data[0]["token"], channel_id, "Some message")

def test_standup_send_invalid_channel():
    """ Tests if error is raised when function is called for an invalid channel """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    standup.standup_start(user_data[0]["token"], channel_id, 2)

    # Asserting that error is raised when user 0 sends standup message in nonexistent channel
    with pytest.raises(InputError):
        standup.standup_send(user_data[0]["token"], 1, "Some message")

def test_standup_send_exceeding_len():
    """ Tests if error is raised if message is more than 1000 chars long """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    standup.standup_start(user_data[0]["token"], channel_id, 2)

    # A long message is one that is over 1000 characters long
    long_msg = "Hello! " * 144

    # Asserting that error is raised when user 0 sends a standup message that is too long
    with pytest.raises(InputError):
        standup.standup_send(user_data[0]["token"], 1, long_msg)

def test_standup_send_inactive_standup():
    """ Tests if error is raised if there is no standup currently active """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # Asserting that error is raised when user 0 sends standup message without active standup
    with pytest.raises(InputError):
        standup.standup_send(user_data[0]["token"], channel_id, "some message")
       
def test_standup_send_not_member():
    """ Tests if error is raised if authorised user is not a member of channel """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 starting a standup for 2 seconds in channel 0
    standup.standup_start(user_data[0]["token"], channel_id, 2)

    # Asserting that error is raised when user 2, not in ch, sends a standup msg in ch
    with pytest.raises(AccessError):
        standup.standup_send(user_data[2]["token"], channel_id, "some message")

#######################
### Initialise data ###
#######################

def initialise_data():
    """ 
    Initialises dummy data
    Registers users 0, 1 and 2
    User 0 creates a channel
    User 1 joins the channel
    """
    # Clearing previous data
    other.clear()

    # Registering user 0
    u_0 = auth.auth_register("validemail0@gmail.com", "goodpassword", "Aqib", "Shaikh")

    # Registering user 1
    u_1 = auth.auth_register("validemail1@gmail.com", "goodpassword", "Aqib", "Naeem")

    # Registering user 2
    u_2 = auth.auth_register("validemail2@gmail.com", "goodpassword", "Naeem", "Shaikh")

    # User 0 creating channel 0
    channel_id = channels.channels_create(u_0["token"], "name", True)["channel_id"]

    # User 1 joining channel 0
    channel.channel_join(u_1["token"], channel_id)

    return {
        "users": [u_0, u_1, u_2],
        "channel_id": channel_id
    }

""" Tests the functionality of search """
import pytest
import auth
import other
import message
import channels
import channel
from error import AccessError

def test_search_not_member():
    """ Tests if an access error is raised when user is not part of any channels """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]

    # Asserting that error is raised when user is not part of any channel
    with pytest.raises(AccessError):
        # User 2, who is not a part of any channel, calling search function
        assert other.search(user_data[2]["token"], "")

def test_search_invalid_token():
    """ Tests if an access error is raised when passed an invalid token """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]

    # Logging user 1 out, making their token invalid
    auth.auth_logout(user_data[1]["token"])

    # Asserting that error is raised when function is called with invalid token
    with pytest.raises(AccessError):
        # User 1, who has logged out, calling search function
        assert other.search(user_data[1]["token"], "")

def test_search_empty_string():
    """ Testing if every message within user's channels is returned when passed an empty string """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    msg_data = initial_data["message_id"]

    # User 1 calling search function, providing an empty query string
    result = other.search(user_data[1]["token"], "")["messages"]

    # There should be two messages in total within the channels user 1 is part of
    assert len(result) == 2
    # There is one message in ch 1 and one in ch 2, which should both be returned
    assert result[0]["message_id"] == msg_data[0]
    assert result[1]["message_id"] == msg_data[1]

def test_search_general():
    """ Testing if messages which include string are returned """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]
    msg_data = initial_data["message_id"]

    # User 1 calling search function, providing a string matching one message
    result = other.search(user_data[1]["token"], "TESTING")["messages"]

    # There should be one messages returned
    assert len(result) == 1
    # There is one message in ch 2 which includes the string "TESTING", which should be returned
    assert result[0]["message_id"] == msg_data[1]

def test_search_no_matches():
    """ Testing if no messages are returned if there aren't any matching strings """
    # Initialising data
    initial_data = initialise_data()
    user_data = initial_data["users"]

    # User 1 calling search function, providing a string not found in any message
    result = other.search(user_data[1]["token"], "blah")["messages"]

    # There should be 0 messages returned
    assert len(result) == 0

def initialise_data():
    """
    Registers user 0,1,2,3 and 4
    Creates a channel with user 0 as owner
    User 1,2 and 3 join the channel
    User 1 is given owner permissions
    """
    # Clearing any previous data
    other.clear()

    # Registering user 0 (flockr owner), user 1 and user 2
    u_0 = auth.auth_register("validemail0@gmail.com", "goodpassword", "Aqib", "Shaikh")
    u_1 = auth.auth_register("validemail1@gmail.com", "goodpassword", "Shaikh", "Naeem")
    u_2 = auth.auth_register("validemail2@gmail.com", "goodpassword", "Aqib", "Naeem")

    # Having user 0 create channel 1, 2 and 3
    ch_1 = channels.channels_create(u_0["token"], "channel_name", True)["channel_id"]
    ch_2 = channels.channels_create(u_0["token"], "channel_name", True)["channel_id"]
    ch_3 = channels.channels_create(u_0["token"], "channel_name", True)["channel_id"]

    # Having user 1 join channel 1 and 2
    channel.channel_join(u_1["token"], ch_1)
    channel.channel_join(u_1["token"], ch_2)

    # Having user 0 send messages in channel 1
    msg_1 = message.message_send(u_0["token"], ch_1, "Testing testing 1 2 3")["message_id"]

    # Having user 0 send messages in channel 2
    msg_2 = message.message_send(u_0["token"], ch_2, "TESTING TESTING 123")["message_id"]

    # Having user 0 send messages in channel 3
    msg_3 = message.message_send(u_0["token"], ch_3, "Testing")["message_id"]

    # A dictionary holding the returned values when registering users and the channel_id
    return {
        "users": [u_0, u_1, u_2],
        "channel_id": [ch_1, ch_2, ch_3],
        "message_id": [msg_1, msg_2, msg_3]
    }

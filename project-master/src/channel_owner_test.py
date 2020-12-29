""" Tests the functionality of channel_addowner and channel_removeowner """
import pytest
from error import InputError
from error import AccessError
import channel
import channels
import other
import auth

##################################
### Tests for channel_addowner ###
##################################

def test_channel_addowner_general():
    """ Tests if making a valid user an owner of a valid channel works """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 making user 2 an owner of the channel
    channel.channel_addowner(user_data[1]["token"], channel_id, user_data[2]["u_id"])
    owners = channel.channel_details(user_data[0]["token"], channel_id)['owner_members']

    # Checking user 2 has been made an owner of channel 0
    is_owner = False
    for owner in owners:
        if owner["u_id"] == 2:
            is_owner = True
    assert is_owner

def test_channel_addowner_already_owner():
    """ Tests if an error is raised when the user is already an owner """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(InputError):
        # User 0 attempting to make user 1, an owner, an owner of the channel again
        assert channel.channel_addowner(user_data[0]["token"], channel_id, user_data[1]["u_id"])

def test_channel_addowner_invalid_channel():
    """ Tests if an error is raised when an invalid channel is passed """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(InputError):
        # User 0 attempting to make user 1 an owner of a non-existent channel 6
        assert channel.channel_addowner(user_data[0]["token"], 6, user_data[1]["u_id"])

def test_channel_addowner_invalid_user():
    """ Tests if an error is raised when the user is not a member of the channel """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(InputError):
        # User 0 attempting to make user 3, not a member of the channel, an owner
        assert channel.channel_addowner(user_data[0]["token"], channel_id, user_data[4]["u_id"])

def test_channel_addowner_invalid_token():
    """ Tests if an error is raised when an invalid token is passed, i.e user has logged out """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 logging out
    auth.auth_logout(user_data[1]["token"])

    with pytest.raises(AccessError):
        # User 1, an owner who has logged out, adding user 2 as owner
        assert channel.channel_addowner(user_data[1]["token"], channel_id, user_data[2]["u_id"])

def test_channel_addowner_not_authorised():
    """ Tests if the user calling the function is not authorised (an owner or flockr owner) """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(AccessError):
        # User 2, a non-owner member, making user 3 an owner of the channel
        assert channel.channel_addowner(user_data[2]["token"], channel_id, user_data[3]["u_id"])

#####################################
### Tests for channel_removeowner ###
#####################################

def test_channel_removeowner_valid():
    """ Tests if revoking a valid user an owner of a valid channel works """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 making revoking user 1 as an owner of the channel
    channel.channel_removeowner(user_data[0]["token"], channel_id, user_data[1]["u_id"])
    owners = channel.channel_details(user_data[0]["token"], channel_id)["owner_members"]

    # Checking if user 1 is no longer an owner of channel 0
    is_owner = False
    for owner in owners:
        if owner["u_id"] == 1:
            is_owner = True
    assert not is_owner

def test_channel_removeowner_not_owner():
    """ Tests if an error is raised when the user is not an owner """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(InputError):
        # User 1 removing user 2, a non-owner of the channel, as owner of channel
        assert channel.channel_removeowner(user_data[1]["token"], channel_id, user_data[2]["u_id"])

def test_channel_removeowner_invalid_channel():
    """ Tests if an error is raised when an invalid channel is passed """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(InputError):
        # User 0 removing user 1 as owner to a non-existent channel 6
        assert channel.channel_removeowner(user_data[0]["token"], 6, user_data[1]["u_id"])

def test_channel_removeowner_invalid_user():
    """ Tests if an error is raised when the user is not a member of the channel """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(InputError):
        # User 0 removing user 4 as owner to channel 0
        assert channel.channel_removeowner(user_data[0]["token"], channel_id, user_data[4]["u_id"])

def test_channel_removeowner_invalid_token():
    """ Tests if an error is raised when an invalid token is passed, i.e user has logged out """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 logging out
    auth.auth_logout(user_data[0]["token"])

    with pytest.raises(AccessError):
        # User 0, an owner who has logged out, removing user 1 as owner
        assert channel.channel_removeowner(user_data[0]["token"], channel_id, user_data[1]["u_id"])

def test_channel_removeowner_not_authorised():
    """ Tests if the user calling the function is not authorised (an owner or flockr owner) """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    with pytest.raises(AccessError):
        # User 2 removing user 1 as owner
        assert channel.channel_removeowner(user_data[2]["token"], channel_id, user_data[1]["u_id"])

#################################
### Other functions for tests ###
#################################

def initialise_data():
    """
    Registers user 0,1,2,3 and 4
    Creates a channel with user 0 as owner
    User 1,2 and 3 join the channel
    User 1 is given owner permissions
    """
    # Clearing any initial data 
    other.clear()

    # Registering user 0 (flockr owner)
    u_0 = auth.auth_register("validemail0@gmail.com", "goodpassword", "Aqib", "Shaikh")

    # Registering user 1
    u_1 = auth.auth_register("validemail1@gmail.com", "goodpassword", "Shaikh", "Naeem")

    # Registering user 2
    u_2 = auth.auth_register("validemail2@gmail.com", "goodpassword", "Naeem", "Aqib")

    # Registering user 3
    u_3 = auth.auth_register("validemail3@gmail.com", "goodpassword", "Aqib", "Naeem")

    # Registering user 4
    u_4 = auth.auth_register("validemail4@gmail.com", "goodpassword", "Shaikh", "Aqib")

    # Having user 0 create a channel
    channel_id = channels.channels_create(u_0['token'], "channel_name", True)["channel_id"]

    # Having user 1 join the channel
    channel.channel_join(u_1['token'], channel_id)

    # Having user 2 join the channel
    channel.channel_join(u_2['token'], channel_id)

    # Having user 3 join the channel
    channel.channel_join(u_3['token'], channel_id)

    # Having user 0 add user 1 as owner
    channel.channel_addowner(u_0['token'], channel_id, u_1['u_id'])

    # A dictionary holding the returned values when registering users and the channel_id
    return {
        'users': [u_0, u_1, u_2, u_3, u_4],
        'channel_id': channel_id
    }

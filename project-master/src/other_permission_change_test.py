""" Tests the functionality of admin_userpermission_change, with valid and error raising tests """
import pytest
import auth
import other
import channel
import channels
from error import InputError, AccessError

ADMIN_PERM_ID = 1
MEM_PERM_ID = 2

def test_perm_change_invalid_user():
    """ Tests if an error is raised when function is passed invalid user_id """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(InputError):
        # Owner of flockr giving a non-existent user 3 admin permissions
        assert other.admin_userpermission_change(
            user_data[0]["token"],
            3,
            ADMIN_PERM_ID
        )

def test_perm_change_invalid_token():
    """ Tests if an error is raised when function is called from token that is no longer valid """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    # User 0 logging out
    auth.auth_logout(user_data[0]["token"])

    with pytest.raises(AccessError):
        # User 0, who is no longer logged in, giving user 1 admin permissions
        assert other.admin_userpermission_change(
            user_data[0]["token"],
            user_data[1]["u_id"],
            ADMIN_PERM_ID
        )

def test_perm_change_not_authorised():
    """ Tests if an error is raised when caller is not authorised to add/remove admins """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(AccessError):
        # User 1 attempting to give user 2 admin permissions
        assert other.admin_userpermission_change(
            user_data[1]["token"],
            user_data[2]["u_id"],
            ADMIN_PERM_ID
        )

def test_perm_change_invalid_permID():
    """ Tests if an error is raised when function is passed invalid permission id """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(InputError):
        # Owner of flockr giving user 1 non-existent permission ID 3
        assert other.admin_userpermission_change(
            user_data[0]["token"],
            user_data[1]["u_id"],
            3
        )

def test_perm_change_make_admin_again():
    """ Tests if an error is raised when making an admin, admin """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    
    # User 0 giving user 1 admin permissions
    other.admin_userpermission_change(
        user_data[0]["token"],
        user_data[1]["u_id"],
        ADMIN_PERM_ID
    )

    with pytest.raises(InputError):
    # User 0 giving user 1 admin permissions again
        assert other.admin_userpermission_change(
            user_data[0]["token"],
            user_data[1]["u_id"],
            ADMIN_PERM_ID
        )

def test_perm_change_make_member_again():
    """ Tests if an error is raised when making a member, member """
    initial_data = initialise_data()
    user_data = initial_data["users"]

    with pytest.raises(InputError):
    # User 0 giving user 1, a member, member permissions again
        assert other.admin_userpermission_change(
            user_data[0]["token"],
            user_data[1]["u_id"],
            MEM_PERM_ID
        )

def test_perm_change_make_admin():
    """ Tests changing a user's permissions to 1 (admin) """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]


    # User 0 giving user 1 admin permissions
    other.admin_userpermission_change(
        user_data[0]["token"],
        user_data[1]["u_id"],
        ADMIN_PERM_ID
    )

    # User 1, who is a admin of flockr but not owner of channel, making user 2 owner of channel
    channel.channel_addowner(user_data[1]["token"], channel_id, user_data[2]["u_id"])

    # asserting that user 2 has been made an owner of channel
    owners = channel.channel_details(user_data[0]["token"], channel_id)["owner_members"]

    success = False
    for owner in owners:
        if owner["u_id"] == user_data[2]["u_id"]:
            success = True

    assert success == True

def test_perm_change_make_member():
    """ Tests changing a user's permissions to 2 (member) """
    initial_data = initialise_data()
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 giving user 1 admin permissions
    other.admin_userpermission_change(
        user_data[0]["token"],
        user_data[1]["u_id"],
        ADMIN_PERM_ID
    )
    # User 0 revoking user 1's admin permissions by giving them member permissions
    other.admin_userpermission_change(
        user_data[0]["token"],
        user_data[1]["u_id"],
        MEM_PERM_ID
    )

    with pytest.raises(AccessError):
        # User 1, not admin of flockr nor owner of channel, trying to make user 2 owner of channel
        assert channel.channel_addowner(user_data[1]["token"], channel_id, user_data[2]["u_id"])

def initialise_data():
    """
    Clears data, registers users 0, 1 and 2
    User 0 creates a channel, users 0, 1 and 2 join the channel
    user 1 is made an owner of the channel
    """
    # Clearing previous data
    other.clear()

    # Registering user 0 (flockr owner)
    u_0 = auth.auth_register("validemail0@gmail.com", "goodpassword", "Aqib", "Shaikh")

    # Registering user 1
    u_1 = auth.auth_register("validemail1@gmail.com", "goodpassword", "Shaikh", "Naeem")

    # Registering user 2
    u_2 = auth.auth_register("validemail2@gmail.com", "goodpassword", "Naeem", "Aqib")

    # User 0 creating a channel
    channel_id = channels.channels_create(u_0["token"], "name", True)["channel_id"]

    # User 1 joining the channel
    channel.channel_join(u_1["token"], channel_id)

    # User 2 joining the channel
    channel.channel_join(u_2["token"], channel_id)

    # A dictionary holding the returned values when registering users
    return {
        'users': [u_0, u_1, u_2],
        'channel_id': channel_id
    }

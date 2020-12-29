""" http tests, errors and general cases, for functions in channel.py """
import requests
import pytest
import json
from serverurl import url

#################################
### channel_invite http tests ###
#################################
# methods: POST
# arguments: token, channel_id, u_id

def test_http_channel_invite_general(url):
    """ Tests if inviting a user to a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 inviting user 3 to channel
    invite_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": user_data[3]["u_id"]
    }
    requests.post(f"{url}/channel/invite", json=invite_args)

    # Getting the list of channels for user 3
    list_args = {
        "token": user_data[3]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=list_args)
    ch_list = json.loads(resp.text)["channels"]
    
    success = False
    for ch in ch_list:
        if ch["channel_id"] == channel_id:
            success = True

    assert success == True

def test_http_channel_invite_invalid_user(url):
    """ Tests if error is raised when inviting nonexistent user """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 inviting user 4 to channel
    invite_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": 4
    }
    resp = requests.post(f"{url}/channel/invite", json=invite_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_invite_invalid_channel(url):
    """ Tests if error is raised when inviting to nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 1 inviting user 3 to nonexistent channel 2
    invite_args = {
        "token": user_data[1]["token"],
        "channel_id": 2,
        "u_id": user_data[3]["u_id"]
    }
    resp = requests.post(f"{url}/channel/invite", json=invite_args)
    
    assert json.loads(resp.text)["code"] == 400

def test_http_channel_invite_already_joined(url):
    """ Tests if error is raised when user is already in channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 inviting user 2 to channel which they are already part of
    invite_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": user_data[2]["u_id"]
    }
    resp = requests.post(f"{url}/channel/invite", json=invite_args)
    
    assert json.loads(resp.text)["code"] == 400

##################################
### channel_details http tests ###
##################################
# methods: GET
# arguments: token, channel_id

def test_http_channel_details_general(url):
    """ Tests if returning the details of a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 getting details of channel
    details_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/channel/details", params=details_args)

    exp = {
        "name": "channel_name",
        "owner_members": [
            {
                'u_id': user_data[0]["u_id"],
                'name_first': 'Zero',
                'name_last': 'Jiro',
            },
            {
                'u_id': user_data[1]["u_id"],
                'name_first': 'One',
                'name_last': 'Ichi',
            }
        ],
        "all_members": [
            {
                'u_id': user_data[0]["u_id"],
                'name_first': 'Zero',
                'name_last': 'Jiro',
            },
            {
                'u_id': user_data[1]["u_id"],
                'name_first': 'One',
                'name_last': 'Ichi',
            },
            {
                'u_id': user_data[2]["u_id"],
                'name_first': 'Two',
                'name_last': 'Ni',
            }
        ]
    }

    assert json.loads(resp.text) == exp

def test_http_channel_details_invalid_channel(url):
    """ Tests if error is raised when asking for details of nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 1 getting details of nonexistent channel 2
    details_args = {
        "token": user_data[1]["token"],
        "channel_id": 2
    }
    resp = requests.get(f"{url}/channel/details", params=details_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_details_not_auth(url):
    """ Tests if error is raised when user asking for details is not in channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 3 getting details of channel they are not in
    details_args = {
        "token": user_data[3]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/channel/details", params=details_args)

    assert json.loads(resp.text)["code"] == 400

###################################
### channel_messages http tests ###
###################################
# methods: GET
# arguments: token, channel_id, start

def test_http_channel_messages_general(url):
    """ Tests if returning the messages of a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 getting messages from channel
    messages_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "start": 0
    }
    resp = requests.get(f"{url}/channel/messages", params=messages_args)

    exp = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    assert json.loads(resp.text) == exp

def test_http_channel_messages_invalid_channel(url):
    """ Tests if error is raised when asking for messages of nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 1 getting messages from nonexistent channel 2
    messages_args = {
        "token": user_data[1]["token"],
        "channel_id": 2,
        "start": 0
    }
    resp = requests.get(f"{url}/channel/messages", params=messages_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_messages_invalid_start(url):
    """ Tests if error is raised when start is greater than num msgs """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 getting messages from channel with 0 messages, from the 7th message
    messages_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "start": 7
    }
    resp = requests.get(f"{url}/channel/messages", params=messages_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_messages_not_auth(url):
    """ Tests if error is raised when user asking for messages is not in channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 3 getting messages from channel they are not in
    messages_args = {
        "token": user_data[3]["token"],
        "channel_id": channel_id,
        "start": 0
    }
    resp = requests.get(f"{url}/channel/messages", params=messages_args)

    assert json.loads(resp.text)["code"] == 400

################################
### channel_leave http tests ###
################################
# methods: POST
# arguments: token, channel_id

def test_http_channel_leave_general(url):
    """ Tests if leaving a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 2 leaving the channel
    leave_args = {
        "token": user_data[2]["token"],
        "channel_id": channel_id,
    }
    requests.post(f"{url}/channel/leave", json=leave_args)

    # Getting the list of channels for user 2
    list_args = {
        "token": user_data[2]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=list_args)

    assert json.loads(resp.text)["channels"] == []

def test_http_channel_leave_wrong_channel(url):
    """ Tests if error is raised when user attempts to leave channel they're not in """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 1 leaving nonexistent channel 2
    leave_args = {
        "token": user_data[1]["token"],
        "channel_id": 2,
    }
    resp = requests.post(f"{url}/channel/leave", json=leave_args)

    assert json.loads(resp.text)["code"] == 400

###############################
### channel_join http tests ###
###############################
# methods: POST
# arguments: token, channel_id

def test_http_channel_join_general(url):
    """ Tests if joining a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 3 joining the channel
    join_args = {
        "token": user_data[3]["token"],
        "channel_id": channel_id,
    }
    requests.post(f"{url}/channel/join", json=join_args)

    # Getting the list of channels for user 3
    list_args = {
        "token": user_data[3]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=list_args)
    ch_list = json.loads(resp.text)["channels"]

    success = False
    for ch in ch_list:
        if ch["channel_id"] == channel_id:
            success = True

    assert success == True

def test_http_channel_join_wrong_channel(url):
    """ Tests if error is raised when user joins nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 3 joining nonexistent channel 2
    join_args = {
        "token": user_data[3]["token"],
        "channel_id": 2,
    }
    resp = requests.post(f"{url}/channel/join", json=join_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_join_private_channel(url):
    """ Tests if error is raised when user attempts to join private channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 0 creating a private channel
    channel_args = {
        'token': user_data[0]["token"],
        'name': "private_name",
        'is_public': False
    }
    resp = requests.post(f"{url}/channels/create", json=channel_args)
    private_channel_id = json.loads(resp.text)["channel_id"]

    # User 1 attempts to join private channel
    join_args = {
        "token": user_data[1]["token"],
        "channel_id": private_channel_id,
    }
    resp = requests.post(f"{url}/channel/join", json=join_args)

    assert json.loads(resp.text)["code"] == 400

###################################
### channel_addowner http tests ###
###################################
# methods: POST
# arguments: token, channel_id, u_id

def test_http_channel_addowner_general(url):
    """ Tests if making a user an owner of a channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 making user 2 owner of channel
    addowner_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": user_data[2]["u_id"]
    }
    requests.post(f"{url}/channel/addowner", json=addowner_args)

    # User 0 getting the details of channel
    details_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/channel/details", params=details_args)
    owners = json.loads(resp.text)["owner_members"]

    is_owner = False
    for owner in owners:
        if owner["u_id"] == user_data[2]["u_id"]:
            is_owner = True
    assert is_owner

def test_http_channel_addowner_already_owner(url):
    """ Tests if error is raised when user is already an owner """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 making user 1 owner of channel again
    addowner_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "u_id": user_data[1]["u_id"]
    }
    resp = requests.post(f"{url}/channel/addowner", json=addowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_addowner_invalid_channel(url):
    """ Tests if error is raised when passed a nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 1 making user 2 owner of nonexistent channel
    addowner_args = {
        "token": user_data[1]["token"],
        "channel_id": 2,
        "u_id": user_data[2]["u_id"]
    }
    resp = requests.post(f"{url}/channel/addowner", json=addowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_addowner_invalid_user(url):
    """ Tests if error is raised when the user is not a member of the channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 making user 3, who is not in channel, owner of channel 
    addowner_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": user_data[3]["u_id"]
    }
    resp = requests.post(f"{url}/channel/addowner", json=addowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_addowner_invalid_token(url):
    """ Tests if error is raised when an invalid token is passed """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 1 logging out
    logout_args = {
        "token": user_data[1]["token"]
    }
    requests.post(f"{url}/auth/logout", json=logout_args)

    # User 1, who has logged out, making user 2 owner of channel
    addowner_args = {
        "token": user_data[1]["token"],
        "channel_id": channel_id,
        "u_id": user_data[2]["u_id"]
    }
    resp = requests.post(f"{url}/channel/addowner", json=addowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_addowner_not_authorised(url):
    """ Tests if error is raised when user calling the function is not authorised """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 3 joining channel
    join_args = {
        "token": user_data[3]["token"],
        "channel_id": channel_id,
    }
    requests.post(f"{url}/channel/join", json=join_args)

    # User 2, not an owner, attempting to make user 3 owner of channel
    addowner_args = {
        "token": user_data[2]["token"],
        "channel_id": channel_id,
        "u_id": user_data[3]["u_id"]
    }
    resp = requests.post(f"{url}/channel/addowner", json=addowner_args)

    assert json.loads(resp.text)["code"] == 400

######################################
### channel_removeowner http tests ###
######################################
# methods: POST
# arguments: token, channel_id, u_id

def test_http_channel_removeowner_general(url):
    """ Tests if revoking a user as owner of the channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 making revoking user 1 as owner of channel
    removeowner_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "u_id": user_data[1]["u_id"]
    }
    requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    # User 0 getting the details of channel
    details_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id
    }
    resp = requests.get(f"{url}/channel/details", params=details_args)
    owners = json.loads(resp.text)["owner_members"]

    is_owner = False
    for owner in owners:
        if owner["u_id"] == user_data[1]["u_id"]:
            is_owner = True
    assert not is_owner

def test_http_channel_removeowner_not_owner(url):
    """ Tests if error is raised when user is not an owner """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 making revoking user 2, who is not an owner, as owner
    removeowner_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "u_id": user_data[2]["u_id"]
    }
    resp = requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_removeowner_invalid_channel(url):
    """ Tests if error is raised when passed a nonexistent channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # User 0 revoking user 1 as owner of nonexistent channel
    removeowner_args = {
        "token": user_data[0]["token"],
        "channel_id": 2,
        "u_id": user_data[1]["u_id"]
    }
    resp = requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_removeowner_invalid_user(url):
    """ Tests if error is raised when the user is not a member of the channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 revoking user 3, who is not in channel, as owner of channel 
    removeowner_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "u_id": user_data[3]["u_id"]
    }
    resp = requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_removeowner_invalid_token(url):
    """ Tests if error is raised when an invalid token is passed """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 0 logging out
    logout_args = {
        "token": user_data[0]["token"]
    }
    requests.post(f"{url}/auth/logout", json=logout_args)

    # User 0, who has logged out, revoking user 1 as owner of channel
    removeowner_args = {
        "token": user_data[0]["token"],
        "channel_id": channel_id,
        "u_id": user_data[1]["u_id"]
    }
    resp = requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    assert json.loads(resp.text)["code"] == 400

def test_http_channel_removeowner_not_authorised(url):
    """ Tests if error is raised when user calling the function is not authorised """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channel_id"]

    # User 2, not an owner, attempting to revoke user 1 as owner of channel
    removeowner_args = {
        "token": user_data[2]["token"],
        "channel_id": channel_id,
        "u_id": user_data[1]["u_id"]
    }
    resp = requests.post(f"{url}/channel/removeowner", json=removeowner_args)

    assert json.loads(resp.text)["code"] == 400

###############################
### Initialising dummy data ###
###############################

def initialise_data(url):
    """
    Registers user 0, 1, 2 and 3
    User 0 creates a channel
    User 1 and 2 join the channel
    User 1 is made an owner of channel 1
    """

    # Clearing previous data
    requests.delete(f"{url}/clear")

    # Registering user 0 (flockr owner)
    user0 = {
        'email': "validemail0@hotmail.com",
        'password': "goodpassword",
        'name_first': "Zero",
        'name_last': "Jiro"
    }
    resp = requests.post(f"{url}/auth/register", json=user0)
    u_0 = json.loads(resp.text)

    # Registering user 1
    user1 = {
        'email': "validemail1@hotmail.com",
        'password': "goodpassword",
        'name_first': "One",
        'name_last': "Ichi"
    }
    resp = requests.post(f"{url}/auth/register", json=user1)
    u_1 = json.loads(resp.text)

    # Registering user 2
    user2 = {
        'email': "validemail2@hotmail.com",
        'password': "goodpassword",
        'name_first': "Two",
        'name_last': "Ni"
    }
    resp = requests.post(f"{url}/auth/register", json=user2)
    u_2 = json.loads(resp.text)

    # Registering user 3
    user3 = {
        'email': "validemail3@hotmail.com",
        'password': "goodpassword",
        'name_first': "Three",
        'name_last': "San"
    }
    resp = requests.post(f"{url}/auth/register", json=user3)
    u_3 = json.loads(resp.text)

    # Having user 0 create a channel
    channel = {
        'token': u_0["token"],
        'name': "channel_name",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=channel)
    channel_id = json.loads(resp.text)["channel_id"]

    # Having user 1 join the channel
    join_args = {
        'token': u_1["token"],
        'channel_id': channel_id
    }
    requests.post(f"{url}/channel/join", json=join_args)

    # Having user 2 join the channel
    join_args = {
        'token': u_2["token"],
        'channel_id': channel_id
    }
    requests.post(f"{url}/channel/join", json=join_args)

    # Having user 0 add user 1 as owner
    addowner_args = {
        'token': u_0["token"],
        'channel_id': channel_id,
        'u_id': u_1["u_id"]
    }
    requests.post(f"{url}/channel/addowner", json=addowner_args)

    # A dictionary holding the returned values when registering users and the channel_id
    return {
        'users': [u_0, u_1, u_2, u_3],
        'channel_id': channel_id
    }

""" http tests, errors and general cases, for functions in channels.py """
import requests
import json
from serverurl import url

################################
### channels_list http tests ###
################################
# methods: GET
# arguments: token

def test_http_channels_list_empty(url):
    """ Tests if empty list is returned if user is not in any channel """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # Getting list of channels user 3 is in
    channel_list_args = {
        "token": user_data[3]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=channel_list_args)

    assert json.loads(resp.text)["channels"] == []

def test_http_channels_list_general(url):
    """ Tests if list of channels user is in is returned """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channels"]

    # Getting list of channels user 1 is in
    channel_list_args = {
        "token": user_data[1]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=channel_list_args)
    ch_list = json.loads(resp.text)["channels"]

    # Messy way of finding out if both channels u_1 is in are listed
    ch_exists = 0
    for channel in ch_list:
        if channel["channel_id"] == channel_id[0]:
            ch_exists += 1
        if channel["channel_id"] == channel_id[1]:
            ch_exists += 1

    assert ch_exists == 2

###################################
### channels_listall http tests ###
###################################
# methods: GET
# arguments: token

def test_http_channels_listall_empty(url):
    """ Tests if empty list is returned if no channels exist """
     # Registering user 0 
    register_args = {
        'email': "validemail0@hotmail.com",
        'password': "goodpassword",
        'name_first': "Zero",
        'name_last': "Jiro"
    }
    resp = requests.post(f"{url}/auth/register", json=register_args)
    u_0 = json.loads(resp.text)

    # Getting list of channels, called by user 0
    listall_args = {
        "token": u_0["token"]
    }
    resp = requests.get(f"{url}/channels/listall", params=listall_args)

    assert json.loads(resp.text)["channels"] == []

def test_http_channels_listall_general(url):
    """ Tests if list of channels that exist is returned """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]
    channel_id = initial_data["channels"]

    # Getting list of channels called by user 3
    listall_args = {
        "token": user_data[3]["token"]
    }
    resp = requests.get(f"{url}/channels/listall", params=listall_args)
    ch_list = json.loads(resp.text)["channels"]

    # Messy way of finding out if all (2) channels created are listed
    ch_exists = 0
    for channel in ch_list:
        if channel["channel_id"] == channel_id[0]:
            ch_exists += 1
        if channel["channel_id"] == channel_id[1]:
            ch_exists += 1

    assert ch_exists == 2

##################################
### channels_create http tests ###
##################################
# methods: POST
# arguments: token, name, is_public

def test_http_channels_create_name_long(url):
    """ Tests if error is raised when name for channel creation is too long """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # Having user 2 create a channel with a name too long
    channel_create_args = {
        'token': user_data[2]["token"],
        'name': "ThisIsMoreThanTwentyCharactersLongProbably",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=channel_create_args)
    assert json.loads(resp.text)["code"] == 400

def test_http_channels_create_name_exists(url):
    """ Tests if channel with same name as another can be created """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # Having user 2 create a channel with a name same as another channel
    channel_create_args = {
        'token': user_data[2]["token"],
        'name': "channel_name",
        'is_public': True
    }
    assert requests.post(f"{url}/channels/create", json=channel_create_args)

def test_http_channels_create_general_public(url):
    """ Tests if creation of public channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # Having user 2 create a new public channel
    channel_create_args = {
        'token': user_data[2]["token"],
        'name': "channel_name3",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=channel_create_args)
    ch_id = json.loads(resp.text)["channel_id"]

    # Getting list of channels user 2 is in
    channel_list_args = {
        "token": user_data[2]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=channel_list_args)
    ch_list = json.loads(resp.text)["channels"]

    # Messy way of finding out if new channel exists
    ch_exists = False
    for channel in ch_list:
        if channel["channel_id"] == ch_id:
            ch_exists = True

    assert ch_exists == True

def test_http_channels_create_general_private(url):
    """ Tests if creation of private channel works """
    initial_data = initialise_data(url)
    user_data = initial_data["users"]

    # Having user 2 create a new private channel
    channel_create_args = {
        'token': user_data[2]["token"],
        'name': "channel_name3",
        'is_public': False
    }
    resp = requests.post(f"{url}/channels/create", json=channel_create_args)
    ch_id = json.loads(resp.text)["channel_id"]

    # Getting list of channels user 2 is in
    channel_list_args = {
        "token": user_data[2]["token"]
    }
    resp = requests.get(f"{url}/channels/list", params=channel_list_args)
    ch_list = json.loads(resp.text)["channels"]

    # Messy way of finding out if both all (2) channels created are listed
    ch_exists = False
    for channel in ch_list:
        if channel["channel_id"] == ch_id:
            ch_exists = True

    assert ch_exists == True

###############################
### Initialising dummy data ###
###############################

def initialise_data(url):
    """
    Registers user 0,1,2, and 3
    User 0 creates a channel
    User 1 and 2 join the channel
    """
    # Clearing previous data
    requests.delete(f"{url}/clear")

    # Registering user 0 (flockr owner)
    user_register_args = {
        'email': "validemail0@hotmail.com",
        'password': "goodpassword",
        'name_first': "Zero",
        'name_last': "Jiro"
    }
    resp = requests.post(f"{url}/auth/register", json=user_register_args)
    u_0 = json.loads(resp.text)

    # Registering user 1
    user_register_args = {
        'email': "validemail1@hotmail.com",
        'password': "goodpassword",
        'name_first': "One",
        'name_last': "Ichi"
    }
    resp = requests.post(f"{url}/auth/register", json=user_register_args)
    u_1 = json.loads(resp.text)

    # Registering user 2
    user_register_args = {
        'email': "validemail2@hotmail.com",
        'password': "goodpassword",
        'name_first': "Two",
        'name_last': "Ni"
    }
    resp = requests.post(f"{url}/auth/register", json=user_register_args)
    u_2 = json.loads(resp.text)

    # Registering user 3
    user_register_args = {
        'email': "validemail3@hotmail.com",
        'password': "goodpassword",
        'name_first': "Three",
        'name_last': "San"
    }
    resp = requests.post(f"{url}/auth/register", json=user_register_args)
    u_3 = json.loads(resp.text)

    # Having user 0 create a channel
    channel_create_args = {
        'token': u_0["token"],
        'name': "channel_name",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=channel_create_args)
    ch_0_id = json.loads(resp.text)["channel_id"]

    # Having user 1 join the channel
    channel_join_args = {
        'token': u_1["token"],
        'channel_id': ch_0_id
    }
    requests.post(f"{url}/channel/join", json=channel_join_args)

    # Having user 2 join the channel
    channel_join_args = {
        'token': u_2["token"],
        'channel_id': ch_0_id
    }
    requests.post(f"{url}/channel/join", json=channel_join_args)

    # Having user 1 create a channel
    channel_create_args = {
        'token': u_1["token"],
        'name': "channel_name2",
        'is_public': True
    }
    resp = requests.post(f"{url}/channels/create", json=channel_create_args)
    ch_1_id = json.loads(resp.text)["channel_id"]

    # A dictionary holding the returned values when registering users and the channel_id
    return {
        'users': [u_0, u_1, u_2, u_3],
        'channels': [ch_0_id, ch_1_id]
    }

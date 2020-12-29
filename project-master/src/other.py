""" This file includes other functions not attributed to other files within the project """
import source_data as src
import error
all_users = src.data["users"]
all_channels = src.data["channels"]
admins = src.data["admins"]

def clear():
    """ Clears the data within source_data to its initial state (empty) """
    for key in src.data:
        src.data[key].clear()

def users_all(token):
    users_all_list = []
    for user in all_users:
        users_all_list.append({
        "u_id": user["id"],
        "email": user["email"],
        "name_first": user["fname"],
        "name_last": user["lname"],
        "handle_str": user["handle_str"]
        })
    return {
        "users": users_all_list
    }

###################################
### admin_userpermission_change ###
###################################

def admin_userpermission_change(token, u_id, permission_id):
    """ Changes a user's permissions to either admin or member 

    Parameters:
        token (str): The authorisation hash of the user executing the function
        u_id (int): The id of the user whose permisions are being changed
        permission_id (int): The id of the permission (1 = Admin, 2 = Member)

    Returns: 
        nothing

    """

    # Error checks
    change_perm_check_user_valid(u_id)
    change_perm_check_token_valid(token)
    change_perm_check_authorised(token)
    change_perm_check_permID_valid(permission_id) 
    change_perm_check_already_admin(permission_id, u_id)
    change_perm_check_already_member(permission_id, u_id)

    # If making user admin from member
    if permission_id == 1: 
        admins.append(u_id)
    # If making user member from admin (removing admin)
    if permission_id == 2:
        admins.remove(u_id)

def change_perm_check_user_valid(u_id):
    """ Checks if the u_id refers to a valid user """
    does_user_exist = False
    for user in all_users:
        if user["id"] == u_id:
            does_user_exist = True
    
    if not does_user_exist:
        raise error.InputError(f"Invalid user id - user {u_id} does not exist")

def change_perm_check_token_valid(token):
    """ Checks if the token is valid (user is logged in) """
    is_token_valid = False
    for user in all_users:
        if user["token"] == token:
            is_token_valid = True

    if not is_token_valid:
        raise error.AccessError("Invalid token - user not logged in")

def change_perm_check_authorised(token):
    """ Checks if the token is authorised for changing another user's permissions """
    is_authorised = False

    for user in all_users:
        if user["token"] == token and user["id"] in admins:
            is_authorised = True

    if not is_authorised:
        raise error.AccessError("Not authorised to change permissions of other users")

def change_perm_check_permID_valid(permission_id):
    """ Checks if the given permission ID is valid (exists), i.e 1 or 2 """
    if permission_id != 1 and permission_id != 2:
        raise error.InputError(f"Invalid permission id - perm id {permission_id} does not exist")

def change_perm_check_already_admin(permission_id, u_id):
    """ Checks if the given user is already an admin, being made an admin """
    if permission_id == 1 and u_id in admins:
        raise error.InputError(f"User {u_id} is already an admin")

def change_perm_check_already_member(permission_id, u_id):
    """ Checks if the given user is already a member, being made a member """
    if permission_id == 2 and u_id not in admins:
        raise error.InputError(f"User {u_id} is already a member")

##############
### Search ###
##############

def search(token, query_str):
    """ Searches through every channel message user has joined for query string

    Parameters:
        token (str): The authorisation hash of the user executing the function
        query_str (str): The string to be searched for within each message in each channel

    Returns:
        List of dictionaries containing data of messages (message_id, u_id, message, time_created)

    """
    # Error checks
    search_check_token_valid(token)
    search_check_user_member(token)

    # Searching for all matching messages
    channels_joined = search_find_user_channels(token)
    matching_messages = []
    for channel in all_channels:
        if channel["channel_id"] in channels_joined:
            for message_info in channel["messages"]:
                if query_str in message_info["message"]:
                    matching_messages.append(message_info)

    return {"messages": matching_messages}

def search_find_token_user(token):
    """ Finds the information of the calling user given their token """
    caller = None
    for user in all_users:
        if user["token"] == token:
            caller = user

    return caller

def search_find_user_channels(token):
    """ Returns list of channels the user is a member of """
    channels_joined = []

    caller = search_find_token_user(token)

    for channel in all_channels:
        for member in channel["members"]:
            if member["u_id"] == caller["id"]:
                channels_joined.append(channel["channel_id"])

    return channels_joined

def search_check_token_valid(token):
    """ Checks if a given token is valid (user is logged in) """
    if search_find_token_user(token) is None:
        raise error.AccessError("Invalid token - User is not logged in")

def search_check_user_member(token):
    """ Checks if the user is a member of at least one channel """
    if len(search_find_user_channels(token)) == 0:
        raise error.AccessError("User must be a part of at least one channel")

import source_data
import error
import channels
from source_data import token2id, get_channelinfo, get_messageinfo

all_users = source_data.data["users"]
all_channels = source_data.data["channels"]


def channel_invite(token, channel_id, u_id):
    source_data.valid_channel(channel_id)

    if not any(u_id == i.get("id") for i in all_users):
        raise error.InputError("Invalid u_id")
    for i in all_channels:
        if channel_id == i.get("channel_id"):
            user_info = i["members"]
            if any(u_id == j.get("u_id") for j in user_info):
                raise error.AccessError("User already in channel")
            else:
                user_details = {}
                for k in all_users:
                    if u_id == k.get("id"):
                        user_details["u_id"] = k.get("id")
                        user_details["name_first"] = k.get("fname")
                        user_details["name_last"] = k.get("lname")
                i["members"].append(user_details)
    return {
    }


def channel_details(token, channel_id):
    source_data.valid_channel(channel_id)

    uid = source_data.token2id(token)

    for i in all_channels:
        if channel_id == i.get("channel_id"):
            user_info = i["members"]
    if not any(uid == k.get("u_id") for k in user_info):
        raise error.AccessError("User not part of channel")

    for channel_look in source_data.data["channels"]:
        if channel_look["channel_id"] == channel_id:
            channel_use = channel_look
    details = {
        'name': channel_use["name"],
        'owner_members': channel_use.get("owners"),
        'all_members': channel_use.get("members"),
    }
    return details


def channel_messages(token, channel_id, start):
    # If channel_id is invalid, raises input error.
    source_data.valid_channel(channel_id)

    # If the user is not a member/owner of the channel, raises access error.
    channel_info = (channels.channels_list(token))["channels"]
    if not any(channel_id == i.get("channel_id") for i in channel_info):
        raise error.AccessError("User is not in the channel")

    # Check if the start is greater than total number of messages in the channel.
    channel_info = get_channelinfo(channel_id)
    if start > len(channel_info['messages']):
        raise error.InputError("Start is greater that number of messages")

    new_msg = []
    message_list = channel_info['messages']
    loop = len(message_list) - start - 1
    if loop < 49:
        end = -1
    else:
        end = start + 50
    while loop >= 0:
        new_msg.append(message_list[loop])
        loop -= 1
    for msg in new_msg:
        for reacts in msg["reacts"]:
            if any (token2id(token) == i for i in reacts['u_ids']):
                reacts["is_this_user_reacted"] = True
            else:
                reacts["is_this_user_reacted"] = False

    return {
        'messages': new_msg,
        'start': start,
        'end': end,
    }


def channel_leave(token, channel_id):
    """If channel_id is invalid, raises input error"""
    source_data.valid_channel(channel_id)
    """If the user is not a member/owner of the channel, raises access error"""
    channel_info = (channels.channels_list(token))["channels"]
    if not any(channel_id == i.get("channel_id") for i in channel_info):
        raise error.AccessError("User is not in the channel")
    """Create a dictionary of the details of the user"""
    user_details = {}
    for i in all_users:
        if token == i.get("token"):
            user_details["u_id"] = i.get("id")
            user_details["name_first"] = i.get("fname")
            user_details["name_last"] = i.get("lname")
    for i in all_channels:
        if channel_id == i.get("channel_id"):
            user_info = i["members"]
            if not any(user_details == j for j in user_info):
                raise error.AccessError("User is not in the channel")
    """Remove the user from the channel"""
    for i in all_channels:
        if channel_id == i.get("channel_id"):
            i["members"].remove(user_details)
            for owner_details in i["owners"]:
                if user_details == owner_details:
                    i["owners"].remove(user_details)
    return {
    }


def channel_join(token, channel_id):
    source_data.valid_channel(channel_id)

    for i in all_channels:
        if channel_id == i.get("channel_id") and i.get("public") == False:
            raise error.AccessError("Channel is private, can't join")
        if channel_id == i.get("channel_id") and i.get("public") == True:
            """Create a dictionary of the details of the user"""
            user_details = {}
            for j in all_users:
                if token == j.get("token"):
                    user_details["u_id"] = j.get("id")
                    user_details["name_first"] = j.get("fname")
                    user_details["name_last"] = j.get("lname")
            i["members"].append(user_details)
    return {
    }


################################################
### channel_owner functions and error checks ###
################################################

def channel_addowner(token, channel_id, u_id):
    """ Adds a user as owner/gives a user owner permissions 

    Parameters:
        token (str): The authorisation hash of the user executing the function
        channel_id (int): The channel to which the user will be added as owner
        u_id (int): The id of the user being added as owner

    Returns: 
        nothing

    """
    # Error checks
    channel_owner_check_channel_exists(channel_id)
    channel_owner_check_token_valid(token)
    channel_owner_check_token_auth(token, channel_id)
    channel_owner_check_user_inChannel(channel_id, u_id)
    channel_owner_check_not_owner(channel_id, u_id)

    # Add user as owner of channel
    matching_user = source_data.find_matching_user_dict_id(u_id)
    owner_info = {
        "u_id": u_id,
        "name_first": matching_user["fname"],
        "name_last": matching_user["lname"],
    }

    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            channel["owners"].append(owner_info)

    return {}


def channel_removeowner(token, channel_id, u_id):
    """ Removes a user as owner/removes a user's owner permissions 

    Parameters:
        token (str): The authorisation hash of the user executing the function
        channel_id (int): The channel from which the user will be removed as owner
        u_id (int): The id of the user being removed as owner

    Returns: 
        nothing

    """
    # Error checks
    channel_owner_check_channel_exists(channel_id)
    channel_owner_check_token_valid(token)
    channel_owner_check_token_auth(token, channel_id)
    channel_owner_check_user_inChannel(channel_id, u_id)
    channel_owner_check_is_owner(channel_id, u_id)

    # Remove user as owner of channel
    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            for owner in channel["owners"]:
                if owner["u_id"] == u_id:
                    channel["owners"].remove(owner)

    return {}


def channel_owner_check_channel_exists(channel_id):
    """ Checks if the given channel exists """
    if not source_data.get_channelinfo(channel_id):
        raise error.InputError(f"Invalid channel_id - channel {channel_id} does not exist ")


def channel_owner_check_token_valid(token):
    """ Checks that given token is valid (user exists, and is logged in) """
    token_valid = False

    for user in all_users:
        if user["token"] == token:
            token_valid = True

    if token_valid == False:
        raise error.AccessError("Invalid token - User does not exist or is not logged in")


def channel_owner_check_token_auth(token, channel_id):
    """ Checks that the caller is authorised to add/remove owners """
    is_owner = False

    auth_id = source_data.find_matching_user_dict_token(token)["id"]
    channel_data = source_data.get_channelinfo(channel_id)

    for owner in channel_data["owners"]:
        if owner["u_id"] == auth_id:
            is_owner = True

    if not is_owner and auth_id not in source_data.data["admins"]:
        raise error.AccessError(f"User {auth_id} is not auth to add/del owners in ch {channel_id}")


def channel_owner_check_user_inChannel(channel_id, u_id):
    """ Check that the user is in the given channel """
    in_channel = False

    channel_data = source_data.get_channelinfo(channel_id)

    for member in channel_data["members"]:
        if member["u_id"] == u_id:
            in_channel = True

    if not in_channel:
        raise error.InputError(f"User {u_id} is not a member of channel {channel_id}")


def channel_owner_check_not_owner(channel_id, u_id):
    """ Check user is not already an owner of the channel, to add owner """
    channel_data = source_data.get_channelinfo(channel_id)

    for owner in channel_data["owners"]:
        if owner["u_id"] == u_id:
            raise error.InputError(f"User {u_id} is already an owner of channel {channel_id}")


def channel_owner_check_is_owner(channel_id, u_id):
    """ Check user is an owner of the channel, to remove owner """
    already_owner = False
    channel_data = source_data.get_channelinfo(channel_id)

    for owner in channel_data["owners"]:
        if owner["u_id"] == u_id:
            already_owner = True

    if not already_owner:
        raise error.InputError(f"User {u_id} is not an owner of channel {channel_id}")

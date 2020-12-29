""" Function implementations for standup feature """
from datetime import datetime
import message as msg
import source_data
import threading
import error
import time
all_channels = source_data.data["channels"]
all_users = source_data.data["users"]
all_messages = source_data.data["messages"]
    
def standup_start(token, channel_id, length):
    source_data.valid_channel(channel_id)

    matching_channel = source_data.get_channelinfo(channel_id)

    if (matching_channel["standup"]["is_active"] == True):
        raise error.InputError("Standup already active")

    standup_start = int(datetime.now().timestamp())
    standup_finish = standup_start + length

    matching_channel["standup"]["is_active"] = True
    matching_channel["standup"]["time_finish"] = standup_finish

    timer = threading.Timer(length, finish_standup, args=[token, channel_id])
    timer.start()
    
    return {
        'time_finish': standup_finish
    }

def finish_standup(token, channel_id):
    channel_info = source_data.get_channelinfo(channel_id)
    standup_messages = channel_info["standup"]["standup_messages"]

    packaged_msg = ""
    for i in range(0, len(standup_messages)):
        handle = standup_messages[i]["handle_str"]
        message = standup_messages[i]["message"]
        packaged_msg += f"{handle}: {message}" + ("\n" if i != (len(standup_messages) - 1) else "")

    msg.message_send(token, channel_id, packaged_msg)

    """ Edge case: If user who starts standup logs out before it ends
    message_id = len(all_messages)
    react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    new_msg = {}
    new_msg['channel_id'] = channel_id
    new_msg['message_id'] = message_id
    new_msg['u_id'] = source_data.token2id(token)
    new_msg['message'] = packaged_msg
    new_msg['time_created'] = int(datetime.now().timestamp())
    new_msg['reacts'] = [react]
    all_messages.append(new_msg)
    channel_info = source_data.get_channelinfo(channel_id)
    channel_info['messages'].append(new_msg)
    """

    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            channel["standup"]["is_active"] = False
            channel["standup"]["time_finish"] = None
            channel["standup"]["standup_messages"].clear()

def standup_active(token, channel_id):
    """ 
    Returns whether a standup in a given channel is active or not,
    If it is active, returns end time. if not active, returns None for end time
    
    Parameters:
    - token: An authorisation hash for the user calling the functions
    - channel_id (int): The id for the channel in which the function is being called
    
    Return:
    - is_active (bool): A true/false value for whether a standup is active or not
    - time_finish (Unix timestamp): The time at which the standup will finish
    
    Possible errors:
    - Invalid channel_id (InputError) - Channel doesn't exist
    - Invalid token (AccessError) - Caller has logged out
    """
    
    # Error checking
    check_invalid_token(token)
    source_data.valid_channel(channel_id)
    check_caller_not_member(token, channel_id)

    # Returning if standup is active, and time_finish if any
    standup_info = source_data.get_channelinfo(channel_id)["standup"]
    if standup_info["is_active"]:
        return {
            "is_active": True,
            "time_finish": standup_info["time_finish"]
        }
    else:
        return {
            "is_active": False,
            "time_finish": None,
        }
    
def standup_send(token, channel_id, message):
    """ 
    Sends a message during a standup meeting in a channel that will be buffered 
    and put into a queue...
    
    Parameters:
    - token: An authorisation hash for the user calling the functions
    - channel_id (int): The id for the channel in which the function is being called
    - message (string): The message that will be sent during the standup
    
    Return: No returns
    
    Possible errors:
    - Invalid channel_id (InputError) - Channel doesn't exist
    - Message too long (InputError) - Message is over 1000 chars long
    - No active standup (InputError) - No standup is currently active
    - Not member (AccessError) - Caller is not a member of channel
    - Invalid token (AccessError) - Caller has logged out
    """
    
    # Error checking
    check_invalid_token(token)
    source_data.valid_channel(channel_id)
    check_inactive_standup(channel_id)
    check_caller_not_member(token, channel_id)
    check_msg_exceeding_len(message)

    # Appending message to standup dictionary in channel
    msg_info = {
        "handle_str": source_data.find_matching_user_dict_token(token)["handle_str"],
        "message": message
    }

    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            channel["standup"]["standup_messages"].append(msg_info)

#################################################################
### Error checking and helper functions for standup functions ###
#################################################################

def get_token_user_info(token):
    """ Given a token, returns the corresponding user dictionary, if it exists """
    caller = None
    for user in all_users:
        if user["token"] == token:
            caller = user

    return caller

def check_invalid_token(token):
    """ Checks if a given token is invalid """
    if get_token_user_info(token) is None:
        raise error.AccessError("Invalid token")

def check_caller_not_member(token, channel_id):
    """ Checks if the user corresponding with the given token is in the given channel """
    token_u_id = get_token_user_info(token)["id"]
    channel_members = source_data.get_channelinfo(channel_id)["members"]
    is_member = False

    for member in channel_members:
        if member["u_id"] == token_u_id:
            is_member = True

    if not is_member:
        raise error.AccessError(f"Not a member of channel {channel_id}")

def check_msg_exceeding_len(message):
    """ Checks if the given message is over 1000 chars long """
    if len(message) > 1000:
        raise error.InputError("Message is over 1000 chars long")

def check_inactive_standup(channel_id):
    """ Checks if there is no active standup within a channel """
    channel_info = source_data.get_channelinfo(channel_id)
    if not channel_info["standup"]["is_active"]:
        raise error.InputError(f"There is no active standup in channel {channel_id}")

import source_data
from source_data import token2id, get_channelinfo, get_messageinfo
import error
import channels
from datetime import datetime
all_users = source_data.data["users"]
all_channels = source_data.data["channels"]
all_messages = source_data.data["messages"]

def message_send(token, channel_id, msg):
    source_data.validate_token(token)

    # InputError
    if len(msg) > 1000:
        raise error.InputError('Exceed 1000 characters.')

    # AccessError
    channel_info = channels.channels_list(token)
    if not any(channel_id == i.get("channel_id") for i in channel_info["channels"]):
        raise error.AccessError("User is not in the channel.")

    # Insert the message into the channel and messages list
    message_id = len(all_messages)
    react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    new_msg = {}
    new_msg['channel_id'] = channel_id
    new_msg['message_id'] = message_id
    new_msg['u_id'] = token2id(token)
    new_msg['message'] = msg
    new_msg['time_created'] = int(datetime.now().timestamp())
    new_msg['reacts'] = [react]
    new_msg['is_pinned'] = False
    all_messages.append(new_msg)
    channel_info = get_channelinfo(channel_id)
    channel_info['messages'].append(new_msg)
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    source_data.validate_token(token)

    # InputError
    if message_id >= len(all_messages):
        raise error.InputError('Message no longer exists.')

    # AccessError
    message_info = get_messageinfo(message_id)
    channel_info = get_channelinfo(message_info.get('channel_id'))
    owner_list = channel_info.get('owners')
    if token2id(token) != message_info.get('u_id') and token2id(token) != owner_list[0].get('u_id'):
        raise error.AccessError('Authorised user did not send this message and not the owner of the channel')
    
    removed_msg = all_messages.pop(message_id)
    messages_list = channel_info.get('messages')
    messages_list.remove(removed_msg)
    # Decrease all messages's id which are greater that message_id by 1.
    for i in all_messages:
        if i.get('message_id') > message_id:
            i['message_id'] -= 1
    for i in all_channels:
        for j in i.get('messages'):
            if j.get('message_id') > message_id:
                j['message_id'] -= 1
    
    return {
    }

def message_edit(token, message_id, msg):
    # AccessError
    message_info = get_messageinfo(message_id)
    channel_info = get_channelinfo(message_info.get('channel_id'))
    owner_list = channel_info.get('owners')
    if token2id(token) != message_info.get('u_id') and token2id(token) != owner_list[0].get('u_id'):
        raise error.AccessError('Authorised user did not send this message and not the owner of the channel')
    
    if msg == '':
        message_remove(token, message_id)
    else:
        message_info['message'] = msg
        for i in channel_info.get('messages'):
            if i.get('message_id') == message_id:
                i['message'] = msg
    return {
    }

def message_sendlater(token, channel_id, msg, time_sent):
    source_data.validate_token(token)
    
    # InputError: Invalid channel_id.
    if channel_id >= len(all_channels):
        raise error.InputError('Invalid channel_id.')
    
    # InputError: More than 1000 characters.
    if len(msg) > 1000:
        raise error.InputError('Exceed 1000 characters.')

    # InputError: Time in the past.
    if time_sent < int(datetime.now().timestamp()):
        raise error.InputError('Invalid time.')
    
    # AccessError
    channel_info = channels.channels_list(token)
    if not any(channel_id == i.get("channel_id") for i in channel_info["channels"]):
        raise error.AccessError("User is not in the channel")
    
    message_id = len(all_messages)
    react = {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
    new_msg = {}
    new_msg['channel_id'] = channel_id
    new_msg['message_id'] = message_id
    new_msg['u_id'] = token2id(token)
    new_msg['message'] = msg
    new_msg['time_created'] = time_sent
    new_msg['reacts'] = [react]
    all_messages.append(new_msg)
    channel_info = get_channelinfo(channel_id)
    channel_info['messages'].append(new_msg)
    return {
        'message_id': message_id,
    }
    
def message_react(token, message_id, react_id):
    u_id = token2id(token)
    channel_info = channels.channels_list(token)
    
    # Message_id is not valid in authorised channel.
    is_message_valid = False
    for i in channel_info['channels']:
        channel_details = get_channelinfo(i.get('channel_id'))
        if any(message_id == j.get('message_id') for j in channel_details['messages']):
            is_message_valid = True
    
    if is_message_valid == False:
        raise error.InputError('Message is not in authorised channel.')
    
    # Invalid react_id.
    if react_id != 1:
        raise error.InputError('Invalid react_id.')
    
    # Already reacted.
    message_info1 = get_messageinfo(message_id)
    channel_info = get_channelinfo(message_info1.get('channel_id'))
    reacts_list1 = message_info1['reacts']
    for i in reacts_list1:
        if i.get('react_id') == react_id:
            if any (u_id == j for j in i['u_ids']):
                raise error.InputError('Already reacted.')
            else:
                i['u_ids'].append(u_id)
    return {
    }

def message_pin(token, message_id):
        source_data.validate_token(token)
        is_there = 0
        for i in source_data.data["messages"]:
            if message_id == i.get('message_id'):
                curr_msg = i
                is_there = 1
        if is_there == 0:
            raise error.InputError('Invalid message id')
        if curr_msg.get('is_pinned'):
            raise error.InputError('message is already pinned')
        channel_id = curr_msg.get('channel_id')
        for k in source_data.data["channels"]:
            if channel_id == k.get('channel_id'):
                curr_channel = k
        within = 0
        for z in curr_channel.get('members'):
            if source_data.token2id(token) == z.get('u_id'):
                within = 1
        if within == 0:
            raise error.AccessError('Message not a part of a channel you are in')
        an_owner = 0
        owner_list = curr_channel["owners"]
        for owners in owner_list:
            if source_data.token2id(token) == owners['u_id']:
                an_owner = 1
        if an_owner == 0:
            raise error.AccessError('Only owners can pin messages')
        curr_msg['is_pinned'] = True

        return {
        }

def message_unpin(token, message_id):
    source_data.validate_token(token)
    for i in source_data.data["messages"]:
        if message_id == i.get('message_id'):
            curr_msg = i
        else:
            raise error.InputError('Invalid message id')
    if curr_msg.get('is_pinned') is False:
        raise error.InputError('message is already unpinned')
    channel_id = curr_msg.get('channel_id')
    for k in source_data.data["channels"]:
        if channel_id == k.get('channel_id'):
            curr_channel = k
    within = 0
    for z in curr_channel.get('members'):
        if source_data.token2id(token) == z.get('u_id'):
            within = 1
    if within == 0:
        raise error.AccessError('Message not a part of a channel you are in')
    an_owner = 0
    for z in curr_channel.get('owners'):
        if source_data.token2id(token) == z.get('u_id'):
            an_owner = 1
    if an_owner == 0:
        raise error.AccessError('Only owners can pin messages')
    curr_msg['is_pinned'] = False

    return {
    }

def message_unreact(token, message_id, react_id):
    u_id = token2id(token)
    channel_info = channels.channels_list(token)

    # Message_id is not valid in authorised channel.
    is_message_valid = False
    for i in channel_info['channels']:
        channel_details = get_channelinfo(i.get('channel_id'))
        if any(message_id == j.get('message_id') for j in channel_details['messages']):
            is_message_valid = True

    if is_message_valid == False:
        raise error.InputError('Message is not in authorised channel.')

    # Invalid react_id.
    if react_id != 1:
        raise error.InputError('Invalid react_id.')

    # Already unreacted.
    message_info1 = get_messageinfo(message_id)
    channel_info = get_channelinfo(message_info1.get('channel_id'))
    reacts_list1 = message_info1['reacts']
    for i in reacts_list1:
        if i.get('react_id') == react_id:
            if not any(u_id == j for j in i['u_ids']):
                raise error.InputError('Already unreacted.')
            else:
                i['u_ids'].remove(u_id)
    return {
    }

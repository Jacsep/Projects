import source_data
import error

def channels_list(token):
    source_data.validate_token(token)

    list_channels = []
    matching_u_id = source_data.find_matching_user_dict_token(token)["id"]
    """Loop through all the channels and find the ones user is apart of"""
    for chan in source_data.data["channels"]:
        for each_chan in chan['members']:
            if matching_u_id == each_chan['u_id']:
                list_channels.append(generate_channel_dict(chan))

    return {
        'channels': list_channels,
    }

def channels_listall(token):
    source_data.validate_token(token)

    list_channels = []
    """Loop through all the channels and add their id and name to a list"""
    for chan in source_data.data["channels"]:
        list_channels.append(generate_channel_dict(chan))

    return {
        'channels': list_channels,
    }

def channels_create(token, name, is_public):
    source_data.validate_token(token)
    
    for user in source_data.data["users"]:
        if user["token"] == token:
            channel_owner = user

    for user in source_data.data["users"]:
        if user["token"] == token:
            channel_owner = user

    if len(name) > 20:
        raise error.InputError("Invalid name")

    id_num = len(source_data.data["channels"])
    """Create new dictionary entry for the creation of a channel"""
    new_channel = {
        'channel_id': id_num,
        'name': name,
        'public': is_public,
        'members': [],
        'owners': [],
        'messages': [
            # Add a list of dictionaries for when messages are added
        ],
        'standup': {
            'is_active': False,
            'time_finish': None,
            'standup_messages': [],
        }
    }
    """Create new dictionary entry containing the member's id, first and last name"""
    member = {
        'u_id': channel_owner["id"],
        'name_first': channel_owner["fname"],
        'name_last': channel_owner["lname"],
    }
    new_channel["members"].append(member)
    new_channel["owners"].append(member)
    source_data.data["channels"].append(new_channel)

    return {
        'channel_id': id_num,
    }

def generate_channel_dict(matching_channel):
    return {
        'channel_id': matching_channel.get('channel_id'),
        'name': matching_channel.get('name'),
    }

from json import dumps

from flask import Flask, request
from flask_cors import CORS

import auth
import channel
import channels
import message as msg
import other
import user
import standup
from error import InputError


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


# auth_register
@APP.route("/auth/register", methods=["POST"])
def auth_register_http():
    payload = request.get_json()
    email = payload["email"]
    password = payload["password"]
    name_first = payload["name_first"]
    name_last = payload["name_last"]
    u_id, token = auth.auth_register(email, password, name_first, name_last).values()
    return dumps({
        'u_id': u_id,
        'token': token
    })


# auth_login
@APP.route("/auth/login", methods=["POST"])
def auth_login_http():
    payload = request.get_json()
    email = payload["email"]
    password = payload["password"]
    u_id, token = auth.auth_login(email, password).values()
    return dumps({
        "u_id": u_id,
        "token": token

    })


# auth_logout
@APP.route("/auth/logout", methods=["POST"])
def auth_logout_http():
    payload = request.get_json()
    token = payload["token"]
    data = auth.auth_logout(token)
    success = str(data["is_success"])
    return dumps({
        "is_success": success
    })


# auth_passwordreset_request
@APP.route("/auth/passwordreset/request", methods=["POST"])
def auth_passwordreset_request_http():
    payload = request.get_json()
    email = payload["email"]
    auth.auth_passwordreset_request(email)
    return ""


# auth_passwordreset_reset
@APP.route("/auth/passwordreset/reset", methods=["POST"])
def auth_passwordreset_reset_http():
    payload = request.get_json()
    reset_code = payload["reset_code"]
    print(type(reset_code))
    new_password = payload["new_password"]
    auth.auth_passwordreset(reset_code, new_password)
    return ""


# channel_invite
@APP.route("/channel/invite", methods=["POST"])
def channel_invite_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    u_id = payload["u_id"]
    channel.channel_invite(token, int(channel_id), int(u_id))
    return ""


@APP.route("/channel/details", methods=["GET"])
def channel_details_http():
    token, channel_id = request.args.values()
    name, owner_members, all_members = channel.channel_details(str(token), int(channel_id)).values()
    return dumps({
        "name": name,
        "owner_members": owner_members,
        "all_members": all_members
    })


@APP.route("/channel/messages", methods=["GET"])
def channel_messages_http():
    token, channel_id, start = request.args.values()
    print(token, channel_id, start)
    messages, start, end = channel.channel_messages(str(token), int(channel_id), int(start)).values()
    return dumps({
        "messages": messages,
        "start": start,
        "end": end
    })


@APP.route("/channel/leave", methods=["POST"])
def channel_leave_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    channel.channel_leave(token, int(channel_id))
    return ""


@APP.route("/channel/join", methods=["POST"])
def channel_join_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    channel.channel_join(str(token), int(channel_id))
    return ""


@APP.route("/channel/addowner", methods=["POST"])
def channel_addowner_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    u_id = payload["u_id"]
    channel.channel_addowner(token, int(channel_id), int(u_id))
    return ""


@APP.route("/channel/removeowner", methods=["POST"])
def channel_removeowner_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    u_id = payload["u_id"]
    channel.channel_removeowner(token, int(channel_id), int(u_id))
    return ""


@APP.route("/channels/list", methods=["GET"])
def channels_list_http():
    token = request.args.get("token")
    channels_dict = channels.channels_list(token)
    return dumps({
        "channels": channels_dict["channels"]
    })


@APP.route("/channels/listall", methods=["GET"])
def channels_listall_http():
    token = request.args.get("token")
    channels_all_dict = channels.channels_listall(token)
    return dumps({
        "channels": channels_all_dict["channels"]
    })


@APP.route("/channels/create", methods=["POST"])
def channels_create_http():
    payload = request.get_json()
    token = payload["token"]
    name = payload["name"]
    is_public = payload["is_public"]
    channel_id_dict = channels.channels_create(token, name, bool(is_public))
    return dumps({
        "channel_id": channel_id_dict["channel_id"]
    })


@APP.route("/message/send", methods=["POST"])
def message_send_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    print(token, channel_id, message)
    dictionary = msg.message_send(token, int(channel_id), message)
    return dumps({
        'message_id': dictionary['message_id']
    })


@APP.route("/message/remove", methods=["DELETE"])
def message_remove_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    msg.message_remove(token, int(message_id))
    return ''


@APP.route("/message/edit", methods=["PUT"])
def message_edit_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message = payload['message']
    msg.message_edit(token, int(message_id), message)
    return ''


@APP.route("/message/sendlater", methods=["POST"])
def message_sendlater_http():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    time_sent = payload['time_sent']
    dictionary = msg.message_sendlater(token, int(channel_id), message, int(time_sent))
    return dumps({
        'message_id': dictionary['message_id']
    })


@APP.route("/message/react", methods=["POST"])
def message_react_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    msg.message_react(token, int(message_id), int(react_id))
    return ''


@APP.route("/message/unreact", methods=["POST"])
def message_unreact_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    msg.message_unreact(token, int(message_id), int(react_id))
    return ''


@APP.route("/message/pin", methods=["POST"])
def message_pin_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    msg.message_pin(token, int(message_id))
    return ''


@APP.route("/message/unpin", methods=["POST"])
def message_unpin_http():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    msg.message_unpin(token, int(message_id))
    return ''


@APP.route("/user/profile", methods=["GET"])
def user_profile_http():
    token, u_id = request.args.values()
    profile = user.user_profile(token, int(u_id))
    return dumps({
        'user': profile['user']
    })


@APP.route("/user/profile/setname", methods=["PUT"])
def user_profile_setname_http():
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    user.user_profile_setname(token, name_first, name_last)
    return ''


@APP.route("/user/profile/setemail", methods=["PUT"])
def user_profile_setemail_http():
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    user.user_profile_setemail(token, email)
    return ''


@APP.route("/user/profile/sethandle", methods=["PUT"])
def user_profile_sethandle_http():
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']
    user.user_profile_sethandle(token, handle_str)
    return ''


@APP.route("/users/all", methods=["GET"])
def users_all_http():
    token = request.args.get('token')
    user_list = other.users_all(token)
    return dumps({
        'users': user_list["users"]
    })


@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_userpermission_change_http():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    other.admin_userpermission_change(token, int(u_id), int(permission_id))
    return ''


@APP.route("/search", methods=["GET"])
def search_http():
    token, query_str = request.args.values()
    messages_list = other.search(token, query_str)
    return ({
        'messages': messages_list['messages']
    })


@APP.route("/clear", methods=["DELETE"])
def clear_http():
    other.clear()
    return ''


@APP.route("/standup/start", methods=["POST"])
def standup_start_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    length = payload["length"]
    returned_dict = standup.standup_start(str(token), int(channel_id), int(length))
    return dumps({
        'time_finish': returned_dict["time_finish"]
    })


@APP.route("/standup/active", methods=["GET"])
def standup_active_http():
    token, channel_id = request.args.values()
    is_active, time_finish = standup.standup_active(str(token), int(channel_id)).values()
    return dumps({
        "is_active": is_active,
        "time_finish": time_finish
    })


@APP.route("/standup/send", methods=["POST"])
def standup_send_http():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    message = payload["message"]
    standup.standup_send(str(token), int(channel_id), str(message))
    return ''


if __name__ == "__main__":
    APP.run(port=0)  # Do not edit this port

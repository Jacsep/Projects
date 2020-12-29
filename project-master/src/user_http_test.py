import requests
import json
from serverurl import url
import pytest
from requests.exceptions import HTTPError

user1 = {
        'email': "validemail@hotmail.com",
        'password': "goodpassword",
        'name_first': "John",
        'name_last': "Smith"
    }

user2 = {
        'email': "validemail1@hotmail.com",
        'password': "goodpassword",
        'name_first': "Mary",
        'name_last': "Smith"
    }

def test_user_profile_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.get(f"{url}/user/profile", params={
            'token': None,
            'u_id': u_id1
        }).raise_for_status()

    with pytest.raises(HTTPError):
        requests.get(f"{url}/user/profile", params={
            'token': token,
            'u_id': 321312
        }).raise_for_status()

def test_valid_normal_user_profile(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]


    profile = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id1
    })
    profile_details = profile.json()
    handle = (profile_details["user"])["handle_str"]
    assert profile_details == {
        'user': {
            'u_id': u_id1,
            'email': "validemail@hotmail.com",
            'name_first': "John",
            'name_last': "Smith",
            'handle_str': handle,
        },
    }

def test_profile_setname_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setname", json={
            'token': 21321,
            'name_first': "Harry",
            'name_last': "John"
        }).raise_for_status()
    
    invalid_name = "m" * 52

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': invalid_name,
            'name_last': "Cheese"
        }).raise_for_status()

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': "Koala",
            'name_last': invalid_name
        }).raise_for_status()

def test_valid_normal_profile_setname(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]

    requests.put(f"{url}/user/profile/setname", json={
        'token': token,
        'name_first': "Kanye",
        'name_last': "West"
    })

    profile = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id1
    })
    profile_details = profile.json()
    handle = (profile_details["user"])["handle_str"]
    assert profile_details == {
        'user': {
            'u_id': u_id1,
            'email': "validemail@hotmail.com",
            'name_first': "Kanye",
            'name_last': "West",
            'handle_str': handle,
        }
    }

def test_profile_setemail_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setemail", json={
            'token': 21321,
            'email': "validemail123@gmail.com"
        }).raise_for_status()

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setemail", json={
            'token': token,
            'email': "ankitrai326.com"
        }).raise_for_status()

    register_user = requests.post(f"{url}/auth/register", json=user2)
    token2 = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/setemail", json={
            'token': token2,
            'email': "validemail@hotmail.com"
        }).raise_for_status()

def test_valid_normal_profile_setemail(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]

    requests.put(f"{url}/user/profile/setemail", json={
        'token': token,
        'email': "kanyewest@gmail.com"
    })

    profile = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id1
    })
    profile_details = profile.json()
    handle = (profile_details["user"])["handle_str"]
    assert profile_details == {
        'user': {
            'u_id': u_id1,
            'email': "kanyewest@gmail.com",
            'name_first': "John",
            'name_last': "Smith",
            'handle_str': handle,
        }
    }

def test_profile_sethandle_errors(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    token = register_user.json()["token"]

    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/sethandle", json={
            'token': 21321,
            'handle_str': 3212
        }).raise_for_status()

    invalid_str = "l" * 23
    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/sethandle", json={
            'token': token,
            'handle_str': invalid_str
        }).raise_for_status()
    
    with pytest.raises(HTTPError):
        requests.put(f"{url}/user/profile/sethandle", json={
            'token': token,
            'handle_str': "a"
        }).raise_for_status()

def test_valid_normal_profile_sethandle(url):
    requests.delete(f"{url}/clear")
    register_user = requests.post(f"{url}/auth/register", json=user1)
    u_id1 = register_user.json()["u_id"]
    token = register_user.json()["token"]

    requests.put(f"{url}/user/profile/sethandle", json={
        'token': token,
        'handle_str': "kanyewest"
    })

    profile = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id1
    })
    profile_details = profile.json()
    assert profile_details == {
        'user': {
            'u_id': u_id1,
            'email': "validemail@hotmail.com",
            'name_first': "John",
            'name_last': "Smith",
            'handle_str': "kanyewest"
        }
    }

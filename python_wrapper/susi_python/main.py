import json
import geocoder
import requests
import time
import os

from .response_parser import *
from uuid import getnode as get_mac

api_endpoint = 'https://api.susi.ai'

access_token = None
location = {'latitude': None, 'longitude': None, 'country_name': None, 'country_code': None}


def check_local_server():
    test_params = {
        'q': 'Hello',
        'timezoneOffset': int(time.timezone / 60)
    }
    try:
        chat_url = 'http://localhost:4000/susi/chat.json'
        if (requests.get(chat_url, test_params)):
            print('connected to local server')
            global api_endpoint
            api_endpoint = 'http://localhost:4000'
    except requests.exceptions.ConnectionError:
        print('local server is down')


check_local_server()


def use_api_endpoint(url):
    global api_endpoint
    api_endpoint = url


def update_location(latitude, longitude, country_name, country_code):
    global location
    location['latitude'] = latitude
    location['longitude'] = longitude
    location['country_name'] = country_name
    location['country_code'] = country_code


def query(query_string):
    params = {
        'q': query_string,
        'timezoneOffset': int(time.timezone/60),
        'device_type': 'Smart Speaker'
    }
    if access_token is not None:
        params['access_token'] = access_token

    if location['latitude'] is not None and location['longitude'] is not None:
        params['latitude'] = location['latitude']
        params['longitude'] = location['longitude']

    if location['country_name'] is not None and location['country_code'] is not None:
        params['country_name'] = location['country_name']
        params['country_code'] = location['country_code']

    global api_endpoint
    chat_url = api_endpoint + "/susi/chat.json"
    try:
        api_response = requests.get(chat_url, params)
    except requests.exceptions.ConnectionError:
        if api_endpoint == 'http://localhost:4000' | api_endpoint == 'https://localhost:4000':
            api_endpoint = 'https://api.susi.ai'
            api_response = requests.get(chat_url, params)
        elif api_endpoint == 'http://api.susi.ai' | api_endpoint == 'https://api.susi.ai':
            api_endpoint = 'http://localhost:4000'
            api_response = requests.get(chat_url, params)

    response_json = api_response.json()
    parsed_res = get_query_response(response_json)
    return parsed_res


def generate_result(response):
    result = dict()
    actions = response.answer.actions
    data = response.answer.data
    
    print(actions)

    for action in actions:
        if isinstance(action, AnswerAction):
            print(action)
            result['answer'] = action.expression
        elif isinstance(action, AudioAction):
            result['identifier'] = action.identifier
        elif isinstance(action, TableAction):
            result['table'] = Table(action.columns, data)
        elif isinstance(action, MapAction):
            result['map'] = Map(action.longitude, action.latitude, action.zoom)
        elif isinstance(action, AnchorAction):
            result['anchor'] = action
        elif isinstance(action, VideoAction):
            result['identifier'] = 'ytd-' + action.identifier
        elif isinstance(action, VolumeAction):
            result['volume'] = action.volume
        elif isinstance(action, RssAction):
            entities = get_rss_entities(data)
            count = action.count
            result['rss'] = {'entities': entities, 'count': count}
        elif isinstance(action, StopAction):
            result['stop'] = action
            break
        elif isinstance(action, MediaAction):
            result['media_action'] = action.type

    return result


def ask(query_string):
    response = query(query_string)
    return generate_result(response)


def answer_from_json(json_response):
    response_dict = json.loads(json_response)
    query_response = get_query_response(response_dict)
    return generate_result(query_response)


def get_rss_entities(data):
    entities = []
    for datum in data:
        values = datum.values
        entity = RssEntity(
            title=values['title'],
            description=values['description'],
            link=values['link']
        )
        entities.append(entity)
    return entities

def add_device(access_token, room_name):

    get_device_info = api_endpoint + '/aaa/listUserSettings.json?'
    add_device_url = api_endpoint + '/aaa/addNewDevice.json?'
    mac = get_mac()
    macid = ':'.join(("%012X"%mac)[i:i+2] for i in range(0,12,2))

    param1 = {
        'access_token':access_token
    }

    # print(access_token)

    if access_token is not None:
        device_info_response = requests.get(get_device_info,param1)
        device_info = device_info_response.json()

    # print(device_info)

    if device_info is not None:
        device = device_info['devices'] # list of existing mac ids
        print(device)
        session = device_info['session'] # session info
        identity = session['identity']
        name = identity['name']
        curr_location = geocoder.ip('me')
        params2 = {
        'macid': macid,
        'name': name,
        'room': str(room_name),
        'latitude': curr_location.lat,
        'longitude': curr_location.lng,
        'access_token': access_token
        }

        for dev in device:
            if dev == macid:
                print('Device already configured')
                return
            else :
                adding_device = requests.post(add_device_url, params2)
                print(adding_device.url)

def sign_in(email, password, room_name=None):
    global access_token
    params = {
        'login': email,
        'password': password
    }
    sign_in_url = api_endpoint + '/aaa/login.json?type=access-token'
    api_response = requests.get(sign_in_url, params)

    if api_response.status_code == 200:
        response_dict = api_response.json()
        parsed_response = get_sign_in_response(response_dict)
        access_token = parsed_response.access_token
        # print(access_token)
        if access_token is not None:
            add_device(access_token, room_name)
    else:
        access_token = None

def sign_up(email, password):
    params = {
        'signup': email,
        'password': password
    }
    sign_up_url = api_endpoint + '/aaa/signup.json'
    api_response = requests.get(sign_up_url, params)
    parsed_dict = api_response.json()
    return get_sign_up_response(parsed_dict)


def forgot_password(email):
    params = {
        'forgotemail': email
    }
    forgot_password_url = api_endpoint + '/aaa/recoverpassword.json'
    api_response = requests.get(forgot_password_url, params)
    parsed_dict = api_response.json()
    return get_forgot_password_response(parsed_dict)


def get_previous_responses():
    memory_url = api_endpoint + '/susi/memory.json'
    api_response = requests.get(memory_url)
    parsed_dict = api_response.json()
    return get_memory_responses(parsed_dict)

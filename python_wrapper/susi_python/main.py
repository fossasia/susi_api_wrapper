import json
import requests

from susi_python.models import Answer, Datum, Metadata, Session, Identity, QueryResponse, LoginResponse, \
    ForgotPasswordResponse, SignUpResponse, AnswerAction, TableAction, UnknownAction, Table, MapAction, AnchorAction, \
    Map

api_endpoint = 'http://api.susi.ai'


def use_api_endpoint(url):
    global api_endpoint
    api_endpoint = url


def query(query_string):
    params = {
        'q': query_string
    }
    chat_url = api_endpoint + "/susi/chat.json"
    api_response = requests.get(chat_url, params)
    return api_response.json(cls=SusiResponseDecoder)


def ask(query_string):
    response = query(query_string)

    result = dict()
    actions = response.answer.actions
    data = response.answer.data

    for action in actions:
        if isinstance(action, AnswerAction):
            result['answer'] = action.expression
        elif isinstance(action, TableAction):
            result['table'] = Table(action.columns, data)
        elif isinstance(action, MapAction):
            result['map'] = Map(action.longitude, action.latitude, action.zoom)
        elif isinstance(action, AnchorAction):
            result['anchor'] = action

    return result


def sign_in(email, password):
    params = {
        'login': email,
        'password': password
    }
    sign_in_url = api_endpoint + '/aaa/login.json?type=access-token'
    api_response = requests.get(sign_in_url, params)
    return api_response.json(cls=LoginResponseDecoder)


def sign_up(email, password):
    params = {
        'signup': email,
        'password': password
    }
    sign_up_url = api_endpoint + '/aaa/signup.json'
    api_response = requests.get(sign_up_url, params)
    return api_response.json(cls=SignUpResponseDecoder)


def forgot_password(email):
    params = {
        'forgotemail': email
    }
    forgot_password_url = api_endpoint + '/aaa/recoverpassword.json'
    api_response = requests.get(forgot_password_url, params)
    return api_response.json(cls=ForgotPasswordDecoder)


def get_previous_responses():
    memory_url = api_endpoint + '/susi/memory.json'
    api_response = requests.get(memory_url)
    return api_response.json(cls=MemoryResponseDecorder)


def get_action(jsn):
    if jsn['type'] == 'answer':
        return AnswerAction(jsn['expression'])
    elif jsn['type'] == 'table':
        return TableAction(jsn['columns'])
    elif jsn['type'] == 'map':
        return MapAction(jsn['latitude'], jsn['longitude'], jsn['zoom'])
    elif jsn['type'] == 'anchor':
        return AnchorAction(jsn['link'], jsn['text'])
    else:
        return UnknownAction()



def generate_query_response(json_object):
    ans = json_object['answers'][0]

    data = [Datum(jsn)
            for jsn in ans['data']]

    metadata = Metadata(ans['metadata'])

    actions = [get_action(jsn)
               for jsn in ans['actions']]

    answer = Answer(data, metadata, actions)

    try:
        identity_json = json_object['session']['identity']
        identity = Identity(identity_json)
        session = Session(identity)
    except KeyError:
        session = None

    return QueryResponse(json_object, answer, session)


class MemoryResponseDecorder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        cognitions = json_object['cognitions']

        susi_responses = []
        for cognition in cognitions:
            susi_responses.append(generate_query_response(cognition))

        return susi_responses

class SusiResponseDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        return generate_query_response(json_object)


class LoginResponseDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        identity_json = json_object['session']['identity']
        identity = Identity(identity_json)
        session = Session(identity)
        return LoginResponse(json_object, session)


class ForgotPasswordDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        return ForgotPasswordResponse(json_object)


class SignUpResponseDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        identity_json = json_object['session']['identity']
        identity = Identity(identity_json)
        session = Session(identity)
        return SignUpResponse(json_object, session)

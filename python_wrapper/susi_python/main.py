import json
import requests

from susi_python.models import Answer, Datum, Metadata, Session, Identity, QueryResponse, LoginResponse, \
    ForgotPasswordResponse, SignUpResponse, AnswerAction, TableAction, UnknownAction, Table

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
        if isinstance(action, TableAction):
            result['table'] = Table(action.columns, data)

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


def get_action(jsn):
    if jsn['type'] == 'answer':
        return AnswerAction(jsn['expression'])
    elif jsn['type'] == 'table':
        return TableAction(jsn['columns'])
    else:
        return UnknownAction()


class SusiResponseDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        ans = json_object['answers'][0]

        data = [Datum(jsn)
                for jsn in ans['data']]

        metadata = Metadata(ans['metadata'])

        actions = [get_action(jsn)
                   for jsn in ans['actions']]

        answer = Answer(data, metadata, actions)

        identity_json = json_object['session']['identity']
        identity = Identity(identity_json)
        session = Session(identity)

        return QueryResponse(json_object, answer, session)


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

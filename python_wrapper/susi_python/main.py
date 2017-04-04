import json
import requests

from susi_python.models import Answer, Datum, Metadata, Action, Session, Identity, QueryResponse, LoginResponse, \
    ForgotPasswordResponse


def query(query_string):
    params = {
        'q': query_string
    }
    api_response = requests.get('https://api.asksusi.com/susi/chat.json', params)
    return api_response.json(cls=SusiResponseDecoder)


def ask(query_string):
    response = query(query_string)
    return response.answer.actions[0].expression


def sign_up(email, password):
    params = {
        'login': email,
        'password': password
    }
    api_response = requests.get('https://api.asksusi.com/aaa/login.json?type=access-token', params)
    return api_response.json(cls=LoginResponseDecoder)


def forgot_password(email):
    params = {
        'forgotemail': email
    }
    api_response = requests.get('https://api.asksusi.com/aaa/recoverpassword.json', params)
    return api_response.json(cls=ForgotPasswordDecoder)


class SusiResponseDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        ans = json_object['answers'][0]

        data = [Datum(jsn)
                for jsn in ans['data']]

        metadata = Metadata(ans['metadata'])

        actions = [Action(jsn)
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
        session = Session(identity_json)
        return LoginResponse(json_object, session)


class ForgotPasswordDecoder(json.JSONDecoder):
    def decode(self, raw_json):
        json_object = super().decode(raw_json)
        return ForgotPasswordResponse(json_object)

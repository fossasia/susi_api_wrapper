import json

from susi_python.models import AnswerAction, TableAction, MapAction, AnchorAction, UnknownAction, Datum, Metadata, \
    Answer, Identity, Session, QueryResponse, LoginResponse, ForgotPasswordResponse, SignUpResponse, RssAction


def get_action(jsn):
    if jsn['type'] == 'answer':
        return AnswerAction(jsn['expression'])
    elif jsn['type'] == 'table':
        return TableAction(jsn['columns'])
    elif jsn['type'] == 'map':
        return MapAction(jsn['latitude'], jsn['longitude'], jsn['zoom'])
    elif jsn['type'] == 'anchor':
        return AnchorAction(jsn['link'], jsn['text'])
    elif jsn['type'] == 'rss':
        return RssAction(jsn['count'],jsn['title'], jsn['description'], jsn['link'])
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

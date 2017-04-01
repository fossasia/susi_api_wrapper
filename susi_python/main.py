import requests
import json

from susi_python.models import Answer, Datum, Metadata, Action, Session, Identity, Response


def query(query_string):
    params = {
        'q': query_string
    }
    api_response = requests.get('https://api.asksusi.com/susi/chat.json', params)
    return api_response.json(cls=SusiResponseDecoder)


def ask(query_string):
    response = query(query_string)
    return response.answer.actions[0].expression


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

        sess = json_object['session']['identity']
        identity = Identity(sess)
        session = Session(identity)

        return Response(json_object, answer, session)

import requests

from susi_python.models import AnswerAction, TableAction, Table, MapAction, AnchorAction, Map, RssAction, RssEntity
from susi_python.response_decoders import MemoryResponseDecorder, ForgotPasswordDecoder, SignUpResponseDecoder, \
    LoginResponseDecoder, SusiResponseDecoder

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
        elif isinstance(action, RssAction):
            result['rss'] = get_rss_entities(data)

    return result


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

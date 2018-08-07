from .models import *


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
        return RssAction(jsn['count'], jsn['title'], jsn['description'], jsn['link'])
    elif jsn['type'] == 'video_play':
        return VideoAction(jsn['identifier'], jsn['identifier_type'])
    elif jsn['type'] == 'stop':
        return StopAction()
    elif jsn['type'] == 'audio_play':
        return AudioAction(jsn['identifier'], jsn['identifier_type'])
    elif jsn['type'] == 'audio_volume':
        return VolumeAction(jsn['volume'])
    else:
        return UnknownAction()


def get_query_response(parsed_dict):
    try:
        identity_json = parsed_dict['session']['identity']
        identity = Identity(identity_json)
        session = Session(identity)
    except KeyError:
        session = None
    if parsed_dict['answers']:
        ans = parsed_dict['answers'][0]
        data = [Datum(jsn) for jsn in ans['data']]
        metadata = Metadata(ans['metadata'])
        actions = [get_action(jsn) for jsn in ans['actions']]
        print(actions[::-1])
        answer = Answer(data, metadata, actions[::-1])
        return QueryResponse(answer,parsed_dict, session)
    else:
        data=[Datum({})]
        metadata=Metadata({'count':0})
        #Generate a temporary action dict in order to reply
        temp_jsn={'language':'en','type':'answer','expression':"Hmm... I'm not sure if I understand you correctly."}
        actions=[get_action(temp_jsn)]
        answer = Answer(data, metadata, actions[::])
        return QueryResponse(answer,parsed_dict, session)


def get_sign_in_response(parsed_dict):
    identity_json = parsed_dict['session']['identity']
    identity = Identity(identity_json)
    session = Session(identity)
    return LoginResponse(parsed_dict, session)


def get_memory_responses(parsed_dict):
    cognitions = parsed_dict['cognitions']

    susi_responses = []
    for cognition in cognitions:
        susi_responses.append(get_query_response(cognition))

    return susi_responses


def get_forgot_password_response(parsed_dict):
    return ForgotPasswordResponse(parsed_dict)


def get_sign_up_response(parsed_dict):
    identity_json = parsed_dict['session']['identity']
    identity = Identity(identity_json)
    session = Session(identity)
    return SignUpResponse(parsed_dict, session)

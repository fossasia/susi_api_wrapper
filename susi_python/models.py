class Response:
    def __init__(self, json, answer, session):
        self.query = json['query']
        self.count = json['count']
        self.client_id = json['client_id']
        self.query_date = json['query_date']
        self.answer_time = json['answer_time']
        self.session = session
        self.answer = answer


class Answer:
    def __init__(self, data, metadata, actions):
        self.data = data
        self.metadata = metadata
        self.actions = actions


class Datum:
    def __init__(self, json):
        #
        # self.zero = json['0']
        # self.one = json['1']
        # self.intent_original = json['intent_original']
        # self.intent_canonical = json['intent_canonical']
        # self.timezoneOffset = json['timezoneOffset']
        #
        self.answer = json['answer']
        self.query = json['query']


class Metadata:
    def __init__(self, json):
        self.count = json['count']


class Action:
    def __init__(self, json):
        if 'type' in json:
            self.type = json['type']
        if 'expression' in json:
            self.expression = json['expression']


class Session:
    def __init__(self, identity):
        self.identity = identity


class Identity:
    def __init__(self, json):
        self.name = json['name']
        self.type = json['type']
        self.anonymous = json['anonymous']

class QueryResponse:
    def __init__(self,answer, json, session):
        self.query = json['query']
        self.count = json['count']
        self.client_id = json['client_id']
        self.query_date = json['query_date']
        self.answer_time = json['answer_time']
        self.session = session
        self.answer = answer

    def __repr__(self):
        return 'QueryResponse (query = %s , count = %s, client_id = %s, ' \
               'query_date = %s, answer_time = %s, session = %s, answer = %s )' % \
               (self.query, self.count, self.client_id, self.query_date, self.answer_time, self.session, self.answer)


class LoginResponse:
    def __init__(self, json, session):
        self.message = json['message']
        self.session = session
        self.valid_seconds = json['valid_seconds']
        self.access_token = json['access_token']

    def __repr__(self):
        return 'LoginResponse: (message = %s, session = %s, valid_seconds = %s, access_token = %s )' % \
               (self.message, self.session, self.valid_seconds, self.access_token)


class SignUpResponse:
    def __init__(self, json, session):
        self.session = session
        self.message = json['message']

    def __repr__(self):
        return 'SignUpResponse: (message = %s, session = %s' % \
               (self.message, self.session)


class ForgotPasswordResponse:
    def __init__(self, json):
        self.message = json['message']

    def __repr__(self):
        return 'ForgotPasswordResponse: (message = %s)' % self.message


class Answer:
    def __init__(self, data, metadata, actions):
        self.data = data
        self.metadata = metadata
        self.actions = actions

    def __repr__(self):
        return 'Answer: (data = %s, metadata = %s, actions = %s)' % \
               (self.data, self.metadata, self.actions)


class Datum:
    def __init__(self, json):
        # all properties of Datum are exposed as a dictionary rather than by field names
        self.values = json

    def __repr__(self):
        return 'Datum: (values = %s)' % self.values


class Metadata:
    def __init__(self, json):
        self.count = json['count']

    def __repr__(self):
        return 'Metadata: (count = %s)' % self.count


class BaseAction:
    def __init__(self):
        pass


class UnknownAction(BaseAction):
    def __init__(self):
        super().__init__()


class AnswerAction(BaseAction):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class TableAction(BaseAction):
    def __init__(self, columns):
        super().__init__()
        # columns is a dictionary containing list of names of column to be displayed on client.
        self.columns = columns


class MapAction(BaseAction):
    def __init__(self, latitude, longitude, zoom=None):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        if zoom is None:
            self.zoom = 13
        else:
            self.zoom = zoom


class AnchorAction(BaseAction):
    def __init__(self, link, text):
        super().__init__()
        self.link = link
        self.text = text

class VideoAction(BaseAction):
    def __init__(self, identifier , identifier_type):
        super().__init__()
        self.identifier = identifier
        self.identifier_type = identifier_type

class RssAction(BaseAction):
    def __init__(self, count, title, description, link):
        super().__init__()
        self.count = count
        self.title = title
        self.description = description
        self.link = link

class StopAction(BaseAction):
    def __init__(self):
        super().__init__()

class AudioAction(BaseAction):
    def __init__(self, identifier , identifier_type):
        super().__init__()
        self.identifier = identifier
        self.identifier_type = identifier_type

class MediaAction(BaseAction):
    def __init__(self, mediaAction):
        super().__init__()


class VolumeAction(BaseAction):
    def __init__(self, volume):
        super().__init__()
        self.volume = volume

class Session:
    def __init__(self, identity):
        self.identity = identity

    def __repr__(self):
        return 'Session: (identity = %s)' % self.identity


class Identity:
    def __init__(self, json):
        self.name = json['name']
        self.type = json['type']
        self.anonymous = json['anonymous']

    def __repr__(self):
        return 'Identity: (name = %s, type = %s, anonymous = %s)' % \
               (self.name, self.type, self.anonymous)


class Table:
    def __init__(self, columns, data):
        self.head = list(columns.values())

        table_data = []
        for datum in data:
            table_datum = []
            for key in columns.keys():
                table_datum.append(datum.values[key])
            table_data.append(table_datum)

        self.data = table_data


class Map:
    def __init__(self, longitude, latitude, zoom=None):
        self.longitude = longitude
        self.latitude = latitude
        if zoom is None:
            self.zoom = 13
        else:
            self.zoom = zoom
        self.openStreetMapLink = 'https://www.openstreetmap.org/#map=%s/%s/%s' % \
                                 (zoom, latitude, longitude)


class RssEntity:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link


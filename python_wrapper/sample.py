import susi_python as susi

'''
A sample application demonstrating use of Wrapper
Currently, Wrapper supports basic chat and auth functionality
'''

'''
Auth Examples
'''


def print_session_info(session):
    identity = session.identity
    print('name:' + identity.name)
    print('anonymous:' + str(identity.anonymous))
    print('type:' + identity.type)


def sign_in(email, password):
    response = susi.sign_in(email, password)

    # message from server
    message = response.message
    print('Server''s Message:' + message)

    # session info
    session = response.session
    print_session_info(session)

    # access-token. Access token can be passed as parameter to queries to identify user
    print('access token:' + response.access_token)

    # valid_seconds. Specifies time in seconds for which token is valid
    print('valid time:' + response.valid_seconds)


def sign_up(email, password):
    response = susi.sign_up(email, password)

    # message from server
    message = response.message
    print('Server''s Message:' + message)

    # session info
    print_session_info(response.session)


def get_old_conversations():
    response = susi.get_previous_responses()
    print(response)
    # handle response


# To sign up a user by email and password
# sign_up('EMAIL_HERE', 'PASSWORD_HERE')

# To sign in a user by email and password
# sign_in('EMAIL_HERE', 'PASSWORD_HERE')


'''
Use a custom api endpoint
'''

# susi.use_api_endpoint('<ADDRESS>')

'''
handle previous conversations
'''

# get_old_conversations()

'''
Chat Example
'''


while True:
    print("You: ", end='')
    input_query = str(input())
    reply = susi.ask(input_query)
    if 'answer' in reply.keys():
        print('Susi:' + reply['answer'])
    if 'table' in reply.keys():
        table = reply['table']
        for h in table.head:
            print('%s\t' % h, end='')
        print()
        for datum in table.data:
            for value in datum:
                print('%s\t' % value, end='')
            print()


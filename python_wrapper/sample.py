import susi_python as susi

'''
A sample application demonstrating use of Wrapper
Currently, Wrapper supports basic chat and auth functionality
'''

'''
Auth Examples
'''


def sign_up(email, password):
    response = susi.sign_up(email, password)

    # message from server
    message = response.message
    print('Server''s Message:' + message)


def get_old_conversations():
    response = susi.get_previous_responses()
    print(response)
    # handle response


# To sign up a user by email and password
# sign_up('EMAIL_HERE', 'PASSWORD_HERE')

# To sign in a user by email and password
# susi.sign_in('clever@gmail.com', 'Clever123')

"""
Use a custom api endpoint
"""
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
    if 'map' in reply.keys():
        mapObject = reply['map']
        print("Map can be viewed at %s", mapObject.openStreetMapLink)
    if 'rss' in reply.keys():
        rss = reply['rss']
        for entity in rss['entities']:
            print('title: {0}\ndescription: {1}\nlink:{2}'.
                  format(entity.title, entity.description, entity.link))

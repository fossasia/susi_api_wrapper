import susi_python as susi

'''
A sample application demonstrating use of Wrapper
Currently, Wrapper supports only chat functionality
'''

while True:
    print("You: ", end='')
    input_query = str(input())
    reply = susi.ask(input_query)
    print('Susi:' + reply)

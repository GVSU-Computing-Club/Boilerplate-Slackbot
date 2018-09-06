from slackclient import SlackClient
from sys import exit
from os import environ
from time import sleep
from pprint import pprint

class Bot(object):
    def __init__(self):
        self.token = None
        self.slackclient = None

    def getTokenFromFile(self, filename):
        '''
        Returns token as a string without newline char from specified file.
        '''
        print('Retrieving Auth Token from file...')
        try:
            tokenFile = open(filename, 'r')
            token = tokenFile.read().rstrip()
            tokenFile.close()
        except IOError:
            print('File does not exist')
            exit(1)
        return token

    def getTokenFromEnv(self):
        '''
        Returns token as string from env variable
        '''
        print('Retriving Auth Token from env...')
        if(environ.get('SLACK_BOT_TOKEN') is not None):
            return environ.get('SLACK_BOT_TOKEN')
        else:
            print('Failed to get token from env')
            exit(2)

    def setToken(self):
        '''
        You can use whichever method you prefer to get the token.
        Comment and uncomment if you prefer the other.
        '''
        self.token = self.getTokenFromFile('token.txt')
#        self.token = self.getTokenFromEnv()

    def connect(self):
        self.setToken()
        self.slackclient = SlackClient(self.token)
        print('Attempting to connect...')
        if(self.slackclient.rtm_connect()):
            print('Connection successful!')
            return True
        else:
            print('Failed to connect')
            return False

    def message(self, text, channel):
        self.slackclient.api_call(
            'chat.postMessage',
            channel=channel,
            text=text
        )

    def run(self):
        if(self.connect()):
            print('Bot running...')

            while True:
                slackevent = self.slackclient.rtm_read()
                #ignore if there is nothing to read
                if(len(slackevent) != 0):
                    event = slackevent[0]
                    pprint(event)

                #Gives the CPU a small break so it's not constantly checking
                sleep(1)


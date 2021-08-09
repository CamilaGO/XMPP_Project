""" Fuentes de consulta
https://slixmpp.readthedocs.io/en/latest/getting_started/sendlogout.html
"""
import sys
import aiodns
import asyncio
import logging
import xmpp
import threading
import base64, time

from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import ClientXMPP


if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Register a new user
def sign_up(user, passw):
    usuario = user
    password = passw
    jid = xmpp.JID(usuario)
    client = xmpp.Client(jid.getDomain(), debug=[])
    client.connect()

    if xmpp.features.register(client, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False

        
class XMPP_CHAT(ClientXMPP):
    def __init__(self, jid, password, *more_arguments):
        #super(XMPP_CHAT, self).__init__(jid, password)
        ClientXMPP.__init__(self, jid, password)
        self.action_info = more_arguments
        # Setup the command line arguments.
        """parser = ArgumentParser(description=XMPP_CHAT.__doc__)

        # Output verbosity options.
        parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                            action="store_const", dest="loglevel",
                            const=logging.ERROR, default=logging.INFO)
        parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                            action="store_const", dest="loglevel",
                            const=logging.DEBUG, default=logging.INFO)

        # JID and password options.
        parser.add_argument("-j", "--jid", dest="jid",
                            help="JID to use")
        parser.add_argument("-p", "--password", dest="password",
                            help="password to use")

        args = parser.parse_args()

        if args.jid is None:
            args.jid = input("Component JID: ")
        if args.password is None:
            args.password = getpass("Password: ")

        # Setup logging.
        logging.basicConfig(level=args.loglevel,
                            format='%(levelname)-8s %(message_start)s')"""

        """self.auto_authorize = True
        self.auto_subscribe = True
        self.contact_dict = {}
        self.user_dict = {}
        self.username = jid"""

        if self.action_info[0] == 1:    
            self.add_event_handler("session_start", self.start)
       
        elif self.action_info[0] == 2:

            self.recipient = self.action_info[1]
            self.msg = self.action_info[2]

            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search

            self.add_event_handler("msg_start", self.msg_start)
            self.add_event_handler("message", self.message)
            
            

            '''self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping'''
            

        elif self.action_info[0] == 3:
            self.add_event_handler("file_start", self.file_start)
            self.add_event_handler("file", self.file)
            
        elif self.action_info[0] == 4:
            self.add_event_handler("showall_start", self.showall_start)
            #self.add_event_handler("showallcontacts", self.showallcontacts)
            
            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search

            self.presences = threading.Event()
            self.contacts = []
            self.user = None
            self.show = True
            self.message = ""

        elif self.action_info[0] == 5:
            self.add_event_handler("addc_start", self.addc_start)
            self.add_event_handler("addcontact", self.addcontact)

            

        elif self.action_info[0] == 6:
            self.add_event_handler("deleteacc_start", self.deleteacc_start)
            self.add_event_handler("deleteuser", self.deleteuser)

            
        elif self.action_info[0] == 7:
            self.add_event_handler("showone_start", self.showone_start)
            self.add_event_handler("showone", self.showone)
        elif self.action_info[0] == 8:
            self.add_event_handler("joinr_start", self.joinr_start)
            self.add_event_handler("joinroom", self.joinroom)
        elif self.action_info[0] == 9:
            self.add_event_handler("creater_start", self.creater_start)
            self.add_event_handler("createroom", self.createroom)
        elif self.action_info[0] == 10:
            self.add_event_handler("msgr_start", self.msgr_start)
            self.add_event_handler("msgroom", self.msgroom)

        """self.received = set()
        self.contacts = []
        self.presences_received = threading.Event()

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0077')  # In-band Registration
        self.register_plugin('xep_0045')  # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096')  # Jabber Search
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0050')
        self.register_plugin('xep_0047')
        self.register_plugin('xep_0231')

        #TR to connect
        if self.connect():
            print("You have succesfully Loged In")
            self.process(block=False)
        else:
            print("We could not connect to @alumchat.xyz")
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping

        # Connect to the XMPP server and start processing XMPP stanzas.
        self.connect()
        self.process(forever=False)"""
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub

    #Log in with a previous created user
    def start(self, event):
        self.send_presence('chat', 'hello world!')
        self.get_roster()
        

    async def msg_start(self, event):
        self.send_presence('chat', 'hello world!')
        await self.get_roster()
        print("async function")
        self.send_message(mto=self.recipient, 
                        mbody=self.msg, 
                        mtype='chat')
    
    def message(self, msg):
        print(msg)
        #Print message
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            
            #print the message and the recipient
            print(str(recipient) +  ": " + str(body))

            #Ask new message
            message = input("Write the message: ")

            #Send message
            self.send_message(mto=self.recipient,
                              mbody=self.msg)

    async def showall_start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        my_contacts = []
        try:
            #Check the roster
            self.get_roster()
        except IqError as e:
            #If there is an error
            print("Something went wrong", e)
        except IqTimeout:
            #Server error
            print("THE SERVER IS NOT WITH YOU")
        
        #Wait for presences
        self.presences.wait(3)

        #For each client on roster
        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                status = show = answer = priority = ''
                self.contacts.append(user)
                subs = self.client_roster[user]['subscription']                         #Get subscription
                conexions = self.client_roster.presence(user)                           
                username = self.client_roster[user]['name']                             #Get username
                for answer, pres in conexions.items():
                    if pres['show']:
                        show = pres['show']                                             #Get show
                    if pres['status']:
                        status = pres['status']                                         #Get status
                    if pres['priority']:
                        priority = pres['priority']                                     #Get priority

                my_contacts.append([
                    user,
                    subs,
                    status,
                    username,
                    priority
                ])
                self.contacts = my_contacts

        #If want to show the details of user or users
        if(self.show):

            #If want to show message of eveyone
            if(not self.user):

                #Check if it is empty
                if len(my_contacts)==0:
                    print('NO CONTACTS CONNECTED')
                else:
                    print('\n USERS: \n\n')

                #Print all
                for contact in my_contacts:
                    print('\tJID:' + contact[0] + '\t\tSUBSCRIPTION:' + contact[1] + '\t\tSTATUS:' + contact[2])
            
            #If want to show message of specific user
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self .user):
                        print('\tJID:' + contact[0] + '\n\tSUBSCRIPTION:' + contact[1] + '\n\tSTATUS:' + contact[2] + '\n\tUSERNAME:' + contact[3] + '\n\tPRIORITY:' + contact[4])
        
        #If want to send presence message
        else:
            for JID in self.contacts:
                self.notification_(JID, self.message, 'active')

        self.disconnect()
        print('\n\n')
    
    def notification_(self, to, body, my_type):

        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body

        if (my_type == 'active'):
            fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'composing'):
            fragmentStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'inactive'):
            fragmentStanza = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Somethiing went wrong\n", e)
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")


    def sign_out(self):
        self.disconnect(wait=True)
        print("Disconnected")




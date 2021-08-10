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
        ClientXMPP.__init__(self, jid, password)
        self.action_info = more_arguments

        if self.action_info[0] == 1:    
            #SIGN UP 
            self.add_event_handler("session_start", self.start)


        elif self.action_info[0] == 2:
            #SEND MESSAGE
            self.recipient = self.action_info[1]
            self.msg = self.action_info[2]

            self.add_event_handler("session_start", self.msg_start)
            self.add_event_handler("message", self.message)
            
            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
            
        elif self.action_info[0] == 3:
            #SHOW ALL CONTACTS INFO
            self.add_event_handler("session_start", self.showall_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = None
            self.show = True
            self.message = ""

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
            

        elif self.action_info[0] == 4:
            #ADD CONTACT TO ROSTER
            self.add_event_handler("session_start", self.addc_start)
            self.new_contact = self.action_info[1]

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
        
        elif self.action_info[0] == 5:
            #SHOW ONE CONTACT DETAILS
            self.add_event_handler("session_start", self.showall_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = self.action_info[1]
            self.show = True
            self.message = ""

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search

        elif self.action_info[0] == 6:
            self.add_event_handler("deleteacc_start", self.deleteacc_start)
            self.add_event_handler("deleteuser", self.deleteuser)

            
        elif self.action_info[0] == 7:
            #SHOW ONE CONTACT DETAILS
            self.add_event_handler("showone_start", self.showone_start)
            self.focus_contact = self.action_info[1]
        elif self.action_info[0] == 8:
            self.add_event_handler("joinr_start", self.joinr_start)
            self.add_event_handler("joinroom", self.joinroom)
        elif self.action_info[0] == 9:
            self.add_event_handler("creater_start", self.creater_start)
            self.add_event_handler("createroom", self.createroom)
        elif self.action_info[0] == 10:
            self.add_event_handler("msgr_start", self.msgr_start)
            self.add_event_handler("msgroom", self.msgroom)


    #Log in with a previous created user
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        
    #Log in with a previous created user and send a message
    async def msg_start(self, event):
        self.send_presence()
        await self.get_roster()
        print("She/He is typing ...")
        self.send_message(mto=self.recipient, 
                        mbody=self.msg, 
                        mtype='chat')
        
    #Receive and print message from the sender
    def message(self, msg):
        #Print message
        if msg['type'] in ('chat'):
            
            sender = str(msg['from']).split("/")
            recipient = str(msg['to']).split("/")
            body = msg['body']
            print("\n>> DM from: " + str(sender[0]) + "\n>> DM to: " + str(recipient[0]) +  "\n>> DM body: " + str(body))
            message = input("\nInput 'E' if you want to close DM\nMessage: ")
            if message == "E" or message == "e":
                self.disconnect()
            else:
                self.send_message(mto=self.recipient,
                                mbody=message, mtype='chat')

    #Show all contacts
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
            print("The server doesn't worl")
        
        #Wait for presences
        self.presences.wait(3)

        #For each user on the roster
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

        #Print the details
        if(self.show):

            #Show all contacts
            if(not self.user):

                #Check if it is empty
                if len(my_contacts)==0:
                    print('Zero contacts #ForeverAlone')
                else:
                    print('\n USERS: \n\n')

                #Print all
                for contact in my_contacts:
                    print('\tJID:' + contact[0] + '\t\tSUBSCRIPTION:' + contact[1] + '\t\tSTATUS:' + contact[2])
            
            #Show specific contatc
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self.user):
                        print('>> JID: ' + contact[0] + '\n>> SUBSCRIPTION: ' + contact[1] + '\n>> STATUS: ' + contact[2])
        
        #send presence message
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

    #Add contact to roster
    async def addc_start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto = self.new_contact) 
        except IqTimeout:
            print("ERROR 500: server doesn't work") 
        self.disconnect()


    def sign_out(self):
        self.disconnect(wait=True)
        print("Disconnected")




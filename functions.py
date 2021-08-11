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

def sign_out():
        print("\nSuccesfully disconnected...")

        
class XMPP_CHAT(ClientXMPP):
    def __init__(self, jid, password, *more_arguments):
        ClientXMPP.__init__(self, jid, password)
        self.action_info = more_arguments
        self.my_user = jid
        self.new_status = ""

        if self.action_info[0] == 1:    
            #SIGN UP 
            self.add_event_handler("session_start", self.start)


        elif self.action_info[0] == 2:
            #SEND MESSAGE
            self.recipient = self.action_info[1]
            self.msg = self.action_info[2]
            self.new_status = self.action_info[3]

            self.add_event_handler("session_start", self.msg_start)
            self.add_event_handler("message", self.message)
            
            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
            
        elif self.action_info[0] == 3:
            #SHOW ALL CONTACTS INFO
            self.add_event_handler("session_start", self.showc_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = None
            self.show = True
            self.message = ""
            self.new_status = self.action_info[1]

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
            

        elif self.action_info[0] == 4:
            #ADD CONTACT TO ROSTER
            self.add_event_handler("session_start", self.addc_start)
            self.new_contact = self.action_info[1]
            self.new_status = self.action_info[2]

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
        
        elif self.action_info[0] == 5:
            #SHOW ONE CONTACT DETAILS
            self.add_event_handler("session_start", self.showc_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = self.action_info[1]
            self.show = True
            self.message = ""
            self.new_status = self.action_info[2]

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search

        elif self.action_info[0] == 6:
            #JOIN CHAT ROOM
            self.room = self.action_info[1]
            self.room_name = self.action_info[2]
            self.new_status = self.action_info[3]

            self.add_event_handler("session_start", self.joinroom_start)
            self.add_event_handler("groupchat_message", self.room_message)
            self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)

            self.register_plugin('xep_0030')
            self.register_plugin('xep_0045')
            self.register_plugin('xep_0199')
        
        elif self.action_info[0] == 7:
            #SEND NOTIFICATION
            print("aun no")
            
        elif self.action_info[0] == 8:
            #SEND A FILE
            self.add_event_handler("session_start", self.file_start)

            self.receiver = self.action_info[1]
            self.file = self.action_info[2]
            self.new_status = self.action_info[3]
            
            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0065') # SOCKS5 Bytestreams

        elif self.action_info[0] == 9:
            #PRESENCE MESSAGE
            self.add_event_handler("session_start", self.showc_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = None
            self.show = False
            self.message = self.action_info[1]
            self.new_status = self.action_info[2]

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
            
        
        elif self.action_info[0] == 10:
            #DEFINE STATUS
            self.new_status = self.action_info[1]
            self.add_event_handler("session_start", self.status_start)

            self.presences = threading.Event()
            self.contacts = []
            self.user = None
            self.show = True
            self.message = ""

            self.register_plugin('xep_0030') # Service Discovery
            self.register_plugin('xep_0199') # XMPP Ping
            self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            self.register_plugin('xep_0096') # Jabber Search
        
        elif self.action_info[0] == 11:
            #DELETE USER
            self.add_event_handler("session_start", self.delete_start)
            

            

    #Log in with a previous created user
    async def start(self, event):
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')
        
        await self.get_roster()
        
    #Send a message to a contact
    async def msg_start(self, event):
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')
        
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
    async def showc_start(self, event):
        #Send presence
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')

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
            print("The server doesn't work")
        
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
                username = self.client_roster[user]['name']   
                print(username)                          #Get username
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
                    print('Zero contacts #LonelyLife')

                #Print all
                for contact in my_contacts:
                    if len(contact[0]) > 3:
                        print('>> JID: ' + contact[0] + '\n>> SUBSCRIPTION: ' + contact[1] + '\n>> STATUS: ' + contact[2]+ "\n")
                    
            #Show specific contatc
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self.user):
                        print('>> JID: ' + contact[0] + '\n>> SUBSCRIPTION: ' + contact[1] + '\n>> STATUS: ' + contact[2])
        
        #send presence message
        else:
            for JID in self.contacts:
                self.presence_msg(JID, self.message, 'active')
            print("Task done!")

        self.disconnect()
    
    #Send presence message
    def presence_msg(self, to, body, my_type):

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
            print("ERROR 500: server doesn't work")        

    #Add contact to roster
    async def addc_start(self, event):
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')

        await self.get_roster()
        try:
            self.send_presence_subscription(pto = self.new_contact) 
        except IqTimeout as e:
            print("ERROR 500: server doesn't work", e) 
        self.disconnect()

    #Room communication
    async def joinroom_start(self, event):
        #Send events to muc
        await self.get_roster()
        
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')

        self.plugin['xep_0045'].join_muc(self.room, self.room_name)

        #Message to send
        message = input("Message: ")
        self.send_message(mto=self.room,
                          mbody=message,
                          mtype='groupchat')

    #Handle muc message for room
    def room_message(self, msg):
        if(str(msg['from']).split('/')[1]!=self.room_name):
            print(str(msg['from']).split('/')[1] + ": " + msg['body'])
            message = input("Message: ")
            self.send_message(mto=msg['from'].bare,
                              mbody=message,
                              mtype='groupchat')

    #Send message to group
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.room_name:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')


    #Send a file
    async def file_start(self, event):
        try:
            #Set the receiver
            proxy = await self['xep_0065'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            proxy.transport.write_eof()
        except (IqError, IqTimeout) as e:
            #Something went wrong
            print('We can not transfer file', e)
        else:
            #File transfer
            print('File succesfully transfered')
        finally:
            self.file.close()
            self.disconnect()
    

    #Delete the account
    async def delete_start(self, event):
        self.send_presence()
        await self.get_roster()
        
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.my_user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("User succesfully deleted\n")
            self.disconnect()
        except IqError as e:
            print("Something went wrong", e)
        except IqTimeout:
            print("ERROR 500: server doesn't work")
        except Exception as e:
           print(e) 


    #Change status and show profile info updated
    async def status_start(self, event):
        self.send_presence('chat', self.new_status)
        await self.get_roster() 

        #Send presence
        if (self.new_status != ""):
            self.send_presence('chat', self.new_status)
        else:
            self.send_presence('chat', 'The future is vegan!')

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
            print("The server doesn't work")
        
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
                username = self.client_roster[user]['name']   
                print(username)                          #Get username
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
                    print('Zero contacts #LonelyLife')

                #Print all
                #for contact in my_contacts:
                 #   if len(contact[0]) > 3:
                print('>> JID: ' + my_contacts[0][0] + '\n>> SUBSCRIPTION: ' + my_contacts[0][1] + '\n>> STATUS: ' + my_contacts[0][2]+ "\n")
                    
            #Show specific contatc
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self.user):
                        print('>> JID: ' + contact[0] + '\n>> SUBSCRIPTION: ' + contact[1] + '\n>> STATUS: ' + contact[2])
        
        #send presence message
        else:
            for JID in self.contacts:
                self.presence_msg(JID, self.message, 'active')
            print("Task done!")

        self.disconnect()
    
    




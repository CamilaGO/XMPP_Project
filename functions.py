import sys
import logging
import getpass
import xmpp
import time
import threading
import binascii
import sleekxmpp
from optparse import OptionParser
from sleekxmpp.util.misc_ops import setdefaultencoding
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from xml.etree.ElementTree import fromstring, ElementTree

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

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
        
class XMPP_CHAT(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super(XMPP_CHAT, self).__init__(jid, password)
        self.auto_authorize = True
        self.auto_subscribe = True
        self.contact_dict = {}
        self.user_dict = {}
        self.username = jid

        self.add_event_handler("session_start", self.sign_in)

        self.received = set()
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

    #Log in with a previous created user
    def sign_in(self, event):
        self.send_presence()
        roster = self.get_roster()




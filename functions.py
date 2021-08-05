import sys
import aiodns
import asyncio
import logging
import xmpp

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
    def __init__(self, jid, password):
        #super(XMPP_CHAT, self).__init__(jid, password)
        ClientXMPP.__init__(self, jid, password)

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
                            format='%(levelname)-8s %(message)s')"""

        """self.auto_authorize = True
        self.auto_subscribe = True
        self.contact_dict = {}
        self.user_dict = {}
        self.username = jid"""

        self.add_event_handler("start_connection", self.start_connection)
        self.add_event_handler("message", self.message)

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

    #Log in with a previous created user
    def start_connection(self, event):
        self.send_presence('chat', 'hello world!')
        self.get_roster()
        

    def message(self, msg):
        print(msg)
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def sign_out(self):
        self.disconnect(wait=True)
        print("Disconnected")




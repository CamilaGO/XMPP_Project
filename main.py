import functions
import fun2
import sys
import logging

user_xmpp = None

def print_menu():
    print("\n-_-_-_-_-_-_-_-_-_ MENU @alumchat.xyz _-_-_-_-_-_-_-_-_-")
    print("1: Send a DM\n2: Show all users info\n3: Add a user to roster\n4: Show contact details\n5: Join Chat room\n6: Create a Room\n7: Send DM to room\n8: Send a File\n9: Delete a user\n10: Sign out\n11: Exit\n")
    menu_option = int(input("Select an option: "))
    return menu_option


def first_menu():
    print("\n-_-_-_-_-_-_-_-_-_ WELCOME TO @alumchat.xyz _-_-_-_-_-_-_-_-_-")
    print("1: Sign up\n2: Sign In\n")
    menu_option = int(input("Select an option: "))
    return menu_option

#empieza el main 


print("******************** CHAT XMPP ********************")
initiation = first_menu()  
user, passw = "", ""
logging.basicConfig()

if (initiation==1):
    print("\n========= Sign Up =========\n")
    user = input("Type your username:   ")
    passw = input("Type your password:    ")
    print("Loading ......")

    signup = functions.sign_up(user, passw)
    if (signup):
        print("User succesfully created!")
        print("Loading ...")

        my_xmpp = functions.XMPP_CHAT(user, passw, 1)
        my_xmpp.connect()
        print("Welcome!")
        my_xmpp.disconnect()

        option = print_menu() 
    else:
        print("F! Try again")

elif (initiation==2):
    print("\n========= Sign In =========\n")
    user = input("Username: ") #gon18398@alumchat.xyz / camila@alumchat.xyz 
    passw = input("Password: ") #123
    my_xmpp = functions.XMPP_CHAT(user, passw, 1)
    my_xmpp.connect()
    print("Welcome Back!")
    my_xmpp.disconnect()

    option = print_menu() 

else:
    print("Invalid option")



while(option >= 1 or option <= 1 ):  
         
    if (option == 1):
        print("\n========= Send Message =========\n")
        recipient = input("Recipient username: ") #echobot@alumchat.xyz
        msg = input("Message: ") 
        print("Sending ......")
        my_xmpp = functions.XMPP_CHAT(user, passw, 2, recipient, msg)
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        option = print_menu()

    elif (option == 2):
        print("\n========= Show All Contacts =========\n")
        my_xmpp = functions.XMPP_CHAT(user, passw, 3)
        print("Loading ...")
        my_xmpp.connect()
        my_xmpp.process(forever=False) 
        option = print_menu() 

    elif (option == 3):
        print("\n========= Add user to roster =========\n")
        new_contact = input("New contact username: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 4, new_contact)
        my_xmpp.connect()
        my_xmpp.process(forever=False)  
        option = print_menu()
    
    elif (option == 4):
        print("\n========= Show contact details =========\n")
        contact = input("Contact username: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 5, contact)
        print("Loading ...")
        my_xmpp.connect()
        my_xmpp.process(forever=False)  
        option = print_menu()

    if (option == 5):
        print("\n========= Sign Out =========\n")
        print("Disconnecting... ")
        my_xmpp.sign_out()
        option = print_menu()  

    elif (option == 6):
        print("\nC U Later - _ -")
        break


    else:
        print("Invalid option!")
        option = print_menu() 

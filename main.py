import functions
import sys
import logging

user_xmpp = None

def print_menu():
    print("\n-_-_-_-_-_-_-_-_-_ MENU @alumchat.xyz _-_-_-_-_-_-_-_-_-")
    print("1: Send a DM\n2: Show all users info\n3: Add a user to roster\n4: Show details of a contact\n5: Join Chat room\n6: Send Notification\n7: Send a File\n8: Define Presence Message\n9: Change Status\n10: Delete account  [ DANGER ] \n11: Sign out / Exit\n")
    menu_option = int(input("Select an option: "))
    return menu_option


def first_menu():
    print("\n-_-_-_-_-_-_-_-_-_ WELCOME TO @alumchat.xyz _-_-_-_-_-_-_-_-_-")
    print("1: Sign up\n2: Sign In\n3: Exit\n")
    menu_option = int(input("Select an option: "))
    return menu_option

#empieza el main 


print("************************* CHAT XMPP *************************")
initiation = first_menu()  
user, passw, new_status = "", "", ""
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
    passw = input("Password: ") #123  /  123*
    my_xmpp = functions.XMPP_CHAT(user, passw, 1)
    my_xmpp.connect()
    print("Welcome Back!")
    my_xmpp.disconnect()

    option = print_menu() 

elif (initiation==3):
    print(" Bye -.- ") 

else:
    print("Invalid option")



while(option >= 1):  
         
    if (option == 1):
        print("\n========= Send Message =========\n")
        recipient = input("Recipient username: ") #echobot@alumchat.xyz
        msg = input("Message: ") 
        print("Sending ......")
        my_xmpp = functions.XMPP_CHAT(user, passw, 2, recipient, msg, new_status)
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        option = print_menu()

    elif (option == 2):
        print("\n========= Show All Contacts =========\n")
        my_xmpp = functions.XMPP_CHAT(user, passw, 3, new_status)
        print("Loading ...")
        my_xmpp.connect()
        my_xmpp.process(forever=False) 
        option = print_menu() 

    elif (option == 3):
        print("\n========= Add User to Roster =========\n")
        new_contact = input("New contact username: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 4, new_contact, new_status)
        my_xmpp.connect()
        my_xmpp.process(forever=False)  
        option = print_menu()
    
    elif (option == 4):
        print("\n========= Show Contact Details =========\n")
        contact = input("Contact username: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 5, contact, new_status)
        print("Loading ...\n")
        my_xmpp.connect()
        my_xmpp.process(forever=False)  
        option = print_menu()
    
    elif (option == 5):
        print("\n========= Join Chat Room =========\n")
        room = input("Room JID: ")  #@conference.alumchat.xyz
        nick_name = input("Your nickname: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 6, room, nick_name, new_status)
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        option = print_menu()
    
    elif (option == 6):
        print("\n========= Send Notification =========\n")
        #7
    
    elif (option == 7):
        print("\n========= Send a File =========\n")
        recipient = input("Recipient username: ") 
        file = input("File path: ") 
        my_xmpp = functions.XMPP_CHAT(user, passw, 8, recipient, file, new_status)
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        option = print_menu()

    elif (option == 8):
        print("\n========= Presence Message =========\n")
        pmsg = input("Presence Message: ")
        my_xmpp = functions.XMPP_CHAT(user, passw, 9, pmsg, new_status)
        print("Loading ...")
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        option = print_menu()
    
    elif (option == 9):
        print("\n========= Define Status =========\n")
        new_status = input('New Status: ') 
        my_xmpp = functions.XMPP_CHAT(user, passw, 10, new_status)
        my_xmpp.connect()
        print("Updating ...")
        my_xmpp.process(forever=False)
        option = print_menu()
    
        
    elif (option == 10):
        print("\n========= Delete User =========\n")
        my_xmpp = functions.XMPP_CHAT(user, passw, 11)
        print("Removing ...\n")
        my_xmpp.connect()
        my_xmpp.process(forever=False)
        initiation = first_menu()
        
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
            passw = input("Password: ") #123  /  123*
            my_xmpp = functions.XMPP_CHAT(user, passw, 1)
            my_xmpp.connect()
            print("Welcome Back!")
            my_xmpp.disconnect()

            option = print_menu() 

        elif (initiation==3):
            print("\nBye (: ")
            break 

        else:
            print("Invalid option")

    elif (option == 11):
        print("\n========= Sign Out =========\n")
        functions.sign_out()
        break

    else:
        print("Invalid option!")
        option = print_menu()
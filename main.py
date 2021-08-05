import functions
import sys
import logging

user_xmpp = None

def print_menu():
    print("\n-_-_-_-_-_-_-_-_-_ MENU @alumchat.xyz _-_-_-_-_-_-_-_-_-")
    print("1: Sign up\n2: Sign In\n3: Sign Out\n4: Delete Account\n5: Show all users info\n6: Add a user to roster\n7: Show contact details\n8: Send a DM\n9: Join Chat room\n10: Create a Room\n11: Send a room message\n12: Send a File\n13: Exit\n")
    menu_option = int(input("Select an option: "))
    return menu_option


#empieza el main 


print("******************** CHAT XMPP ********************")
option = print_menu()   

while(option >= 1 or option <= 1 ):
    
    if (option == 1):
        print("\n========= Sign Up =========\n")
        nickname = input("Type your username:   ")
        code = input("Type your password:    ")
        print("Loading ......")

        signup = functions.sign_up(nickname, code)
        if (signup):
            print("User succesfully created!")
        else:
            print("F! Try again")

        option = print_menu()  

    elif (option == 2):
        print("\n========= Sign In =========\n")
        logging.basicConfig()

        user = input("Username: ") #gon18398@alumchat.xyz / camila@alumchat.xyz 
        passw = input("Password: ") #123
        print("Loading ......")
        #my_xmpp = functions.XMPP_CHAT(user, passw)
        my_xmpp = functions.XMPP_CHAT(user, passw)
        my_xmpp.connect()
        print("You have successfully logged in")
        #my_xmpp.process(block=True)

        option = print_menu()  
    
    elif (option == 3):
        print("\n========= Sign Out =========\n")
        print("Disconnecting... ")
        my_xmpp.sign_out()
        option = print_menu()  

    elif (option == 13):
        print("\nC U Later - _ -")
        break

    else:
        print("Invalid option!")
        option = print_menu() 

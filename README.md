# XMPP Project

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

This project is a XMPP client with slixmpp implemented for *redes* course at UVG. 

## Demo
[![Watch the video](https://img.youtube.com/vi/YAdJggSAgUc/maxresdefault.jpg)](https://youtu.be/YAdJggSAgUc)


## Requirements
You need `Python 3.7.3` installed and the python libraries listed:
```
pip install slixmpp
pip install xmpppy
```

## Usage
Run `main.py` and select *sign up* or *sign in*
\
\
\
Please make sure to include `@alumchat.xyz` in your username and your friend's username. **Example:**
``` 
myusername@alumchat.xyz
```
You can chat with `echobot@alumchat.xyz` to immediately receive the same message that you sent
\
\
\
Take note that a room name must contains `@conference.alumchat.xyz`. **You can join the following room:**
``` 
test@conference.alumchat.xyz
```

## Features
- [x] 💬 Register a new account on the server
- [x] 💻 Log in with an account
- [x] 💻 Log out with an account
- [x] 🗑️ Delete account from server
- [x] 👁️‍🗨️ Show all contacts and their status
- [x] 👩‍💻 Add a user to contacts
- [x] 👁️ Show a user's contact details
- [x] 👤 1 to 1 communication with any user
- [x] 👥 Participate in group conversations
- [x] 📢 Define presence message
- [x] 🔔 Send / receive notifications
- [x] 📂 Send / receive files
- [x] 💭 Define status

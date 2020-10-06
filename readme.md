This project contains only one app, namely 'chat'.

The main premise of this project is real-time chat between users.

This project makes use of 'polling', where the client makes request to the server to find what has changed, if nothing has changed then nothing happens, but if something did change then that data is taken from the server and further processed on the client side.

Users can login, register and send messages to each other.

it contains two Django Models(User and Message), RestAPI routes and Javascript on the client-side to perform client-side operations.

There are Two API routes and Four basic routes which are all explained below:

## Basic Routes:
#### login:
    Allows users to login if they already have an account.

#### register:
    Allows users to create new accounts.

#### logout:
    Allows users to logout if logged-in.

#### index:
    The main chat page where users can send and read messages from other users, 
    user if logged out can still read and receive new messages but cannot send messages unless logged-in.

## API Routes:
#### send:
    Allows users to send new messages and save them in the database.

#### messages/<id>:
    
    The 'polling' route on which requests are made for new data changes.
    Takes the id of the last message that user already has and then checks if data has been updated or not.

______________________________________________

## Self Created Files:
#### serializers.py:
    Contains serializers for rest api data transmission.
#### main.js:
    Contains the main javascript that handles all the client side processing.
#### styles.css:
    Contains all the self-written css for page styling.

## Templates:
#### layout.html:
    Contains the navbar and static file links.
#### index.html:
    Contains the chatroom for messaging and receiving messages.
#### login.html/register.html:
    Contains html for login/register form(s).

## Models:
models.py contains Two Models.

#### User:
    Contains the main user data.

#### Message:
    Contains data of the messages sent by the user.

#### How to Run?
* Download python 3.x
* type "pip install Django" in the command line
* type "pip install djangorestframework" in the command line
* Clone or download this Repository.
* Go into the Repository directory.
* type "python manage.py runserver" in command line.


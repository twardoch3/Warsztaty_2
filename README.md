# Warsztaty_2 -Database module - Message server
This project is a simple communication app that allows a user to create account (also edit or delete account) and send messages to other users.
### Requirements
Program requires PostgreSQL database and python3.
### Installing
Connection info (src/db_run/__init__.py): 
```
class DB:
    username = "postgres"
    passwd = "coderslab"
    hostname = "localhost"
    db = "warsztaty_db"
```

Run create_db.py file to create database with tables for users and messages.
```
python3 create_db.py
```
### Running the program
Manage users:
```
python3 manage_users.py
```
Send messages:
```
python3 send_messages.py
```
### Usage Examples:
create user:
```
python3 manage_users.py -u USERNAME -p PASSWORD
```
send message:
```
python3 send_messages.py -u USERNAME -p PASSWORD -t TO -s SEND

```
users/messages list:
```
python3 manage_users.py -l
python3 send_messages.py -u USERNAME -p PASSWORD -l

```
### Help:
Use help to see all commands:
```
python3 manage_users.py -h
python3 send_messages.py -h

```

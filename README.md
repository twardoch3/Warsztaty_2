# Warsztaty_2 -Database module - Message server
Application allows to send messages between users and manage them (add, edit or delete users).
### Requirements
Program requires PostgreSQL database and python3.
### Installing
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

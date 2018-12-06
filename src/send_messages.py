#!/usr/bin/python3
from models import User, Message
from db_run import DB
from prettytable import PrettyTable
import argparse
from manage_users import password_atleast_8
from clcrypto import check_password
from getpass import getpass



def user_messages_list(message_list, username):  # userX.username
    pt = PrettyTable(['Id', 'sender(from)', 'text', 'creation_date'])
    for ob in message_list:
        row = [ob.id, ob.sender, ob.text, ob.creation_date]
        pt.add_row(row)
    print('***User {} *** Messages List***'.format(username))
    print(pt)


def messages(all_messages):
    pt = PrettyTable(['Id', 'from_user', 'to_user', 'text', 'creation_date'])
    for ob in all_messages:
        row = [ob.id, 'xxx', 'xxx', ob.text, ob.creation_date]
        pt.add_row(row)
    print('***All messages in database. Only text and date***')
    print(pt)


def delete_messages(message_list, username):  # userX.username
    for ob in message_list:
        ob.delete(curs)
    print('All messages removed for user {}'.format(username))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Warsztaty database - sending messages',
                                     description='Allowed options: (-u -p -d), (-u -p -l), (-u -p -t -s), (-u -p -m)')
    parser.add_argument('-u', '--username', help='type in username, use with -p')
    parser.add_argument('-p', '--password', help='type in password, use with -u')
    parser.add_argument('-t', '--to', help='receiver username, use with -u, -p and -s')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true', help='list of user messages, use with -u and -p')
    group.add_argument('-m', '--messages', action='store_true', help="list of all users' messages, use with -u and -p")
    group.add_argument('-d', '--delete', action='store_true', help="delete user messages, use with -u and -p")
    group.add_argument('-s', '--send',
                       help='type in message, contain message in quotes: \'\' or "", use with -u, -p and -t')

    args = parser.parse_args()
    cnx = None
    ob = DB()
    try:
        cnx = ob.connect_db()
    except Exception:
        raise Exception('Incorrect connection parameters or database not created!')

    with ob.db_cursor(cnx) as curs:

        if args.username and args.password:
            userX = User.load_user_by_username(curs, args.username)  # ?
            if not userX:
                print("User {} doesn't exist in database.".format(args.username))
            else:
                if password_atleast_8(args.password):
                    p_check = check_password(args.password, userX.hashed_password)
                    if p_check:
                        if args.to:  # !
                            if args.send:
                                receiver = User.load_user_by_username(curs, args.to)
                                # create new message
                                if receiver:
                                    new_message = Message()
                                    new_message.from_id = userX.id
                                    new_message.to_id = receiver.id
                                    new_message.text = args.send
                                    new_message.save_to_db(curs)
                                    print("Message with text '{}' was sent to user {}".format(args.send,
                                                                                              receiver.username))
                                else:
                                    print("User {} doesn't exist in database.".format(args.to))
                            elif not args.send:
                                if args.send == '':
                                    print("Error. Message is a empty field!")
                                else:
                                    parser.print_help()

                        elif args.list:
                            # user message box
                            message_list = Message.load_all_messages_for_user(curs, userX.username)
                            user_messages_list(message_list, userX.username)

                        elif args.messages:
                            # all messages
                            all_messages = Message.load_all_messages(curs)
                            messages(all_messages)

                        elif args.delete:
                            # delete message box
                            message_list = Message.load_all_messages_for_user(curs, userX.username)
                            delete_messages(message_list, userX.username)

                        else:
                            parser.print_help()

                    else:
                        print(argparse.ArgumentTypeError('Error. Wrong Password!'))


                else:
                    print(argparse.ArgumentTypeError('Password too short. Eight marks required'))
        else:
            parser.print_help()

    cnx.commit()
    cnx.close()

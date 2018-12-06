#!/usr/bin/python3
import argparse
from models import User
from db_run import DB
from clcrypto import generate_salt, check_password
from prettytable import PrettyTable


def users_list(all_users_list):
    print('***** Users List *****')
    pt = PrettyTable(['Id', 'username', 'email'])
    for ob in all_users_list:
        row = [ob.id, ob.username, ob.email]
        pt.add_row(row)
    print(pt)


def create_user(username, password):  # options['username'] options['password']
    print("User {} doesn't exist in database.".format(username))
    print('Create new User:')
    email = input('Enter new user email: ')
    u1 = User()
    dict_pass_salt = {'password': password, 'salt': generate_salt()}
    u1.username = username
    u1.hashed_password = dict_pass_salt
    if email_check(email):
        u1.email = email
        u1.save_to_db(curs)
        # print(u1.id)
        print(' User added to database.')
    else:
        print(argparse.ArgumentTypeError('Wrong email!'))


def delete_user(user):
    user.delete(curs)
    print('User {} deleted from database'.format(user.username))


def change_password(new_pass):  # options['new_pass']
    if password_atleast_8(new_pass):
        dict_pass_salt = {'password': new_pass, 'salt': generate_salt()}
        userX.hashed_password = dict_pass_salt
        userX.save_to_db(curs)
        print('password changed')
    else:
        print(
            argparse.ArgumentTypeError('New Password too short. Eight marks required'))  # !


def password_atleast_8(password):
    if len(password) < 8:
        return False
    else:
        return True


def email_check(email):
    if '@' and '.' not in email:
        return False
    else:
        return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Warsztaty database - users management',
                                     description='Allowed options: (-u -p), (-u -p -d), (-l), (-u -p -e -n)')
    parser.add_argument('-u', '--username', help='type username, use with -p')
    parser.add_argument('-p', '--password', help='type password, use with -u')
    parser.add_argument('-e', '--edit', action='store_true', help='edit, use with -u -p -n')
    parser.add_argument('-n', '--new_pass', help='change password, use with -u -p -e')
    parser.add_argument('-d', '--delete', action='store_true', help='delete user, use wit -u -p')
    parser.add_argument('-l', '--list', action='store_true', help='list of users')

    options = vars(parser.parse_args())
    options = {k: v for k, v in options.items() if v not in (False, None)}

    # db connection
    cnx = None
    ob = DB()
    try:
        cnx = ob.connect_db()
    except Exception:
        raise Exception('Incorrect connection parameters or database not created!')

    with ob.db_cursor(cnx) as curs:
        if 'username' in options:
            if len(options) > 0 and 'password' not in options:
                parser.print_help()
            userX = User.load_user_by_username(curs, options['username'])
            # no user
            if not userX:
                if 'password' in options:
                    if len(options) == 2:
                        if password_atleast_8(options['password']):
                            # create user
                            create_user(options['username'], options['password'])
                        else:
                            print(argparse.ArgumentTypeError('Password too short. Eight marks required'))
                    else:
                        parser.print_help()
                        print("User {} doesn't exist in database.".format(options['username']))

            # user exists
            else:
                if 'password' in options:
                    if password_atleast_8(options['password']):
                        p_check = check_password(options['password'], userX.hashed_password)
                        if p_check:
                            if len(options) == 2:
                                print(argparse.ArgumentTypeError('Error. User already exists!'))
                            elif 'delete' in options and len(options) == 3:
                                # delete user
                                delete_user(userX)

                            elif 'edit' in options and 'new_pass' in options and len(options) == 4:
                                # change password
                                change_password(options['new_pass'])

                            else:
                                parser.print_help()

                        else:
                            print(argparse.ArgumentTypeError('Error. Wrong Password!'))

                    else:
                        print(argparse.ArgumentTypeError('Password too short. Eight marks required'))


        else:
            if 'list' in options and len(options) == 1:
                all_users_list = User.load_all_users(curs)
                # print users list
                users_list(all_users_list)
            else:
                parser.print_help()

    cnx.commit()
    cnx.close()

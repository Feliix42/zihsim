#!/usr/bin/env python3
import re
import os
import sys
import pickle
import random
import string
import signal
from getpass import getpass
from time import sleep
from termcolor import colored
import sudoers

# the global users list - is being dumped to the backup file
users = []
# semester counter
semester = 1
# location of the backup file
backupfile = './backup.pkl'
# controlls the language
en = False
# are we in sudo mode?
sudomode = False

class User():
    '''
    The User Class instantiates an object for each user that is created.
    '''

    def __init__(self, first, last, dob, address):
        self.first = first
        self.last = last
        self.dob = dob
        self.address = address
        self.uid = uid_gen()
        self.fpass = passwordgen()
        self.password = ''
        if en:
            print('\nWelcome, {firstname}! Your USER ID is {uid}.'.format(
                  firstname=self.first, uid=colored(self.uid, 'yellow',
                                                    'on_white',
                                                    attrs=['blink', 'bold'])),
                  '\nYour one-time password is {passw}.'.format(passw=colored(
                                                                self.fpass,
                                                                'green',
                                                                'on_white',
                                                                attrs=['blink',
                                                                       'bold'])
                                                                ),
                  "\nDon't forget to change it.")
        else:
            print('\nWillkommen, {firstname}! Deine USER ID ist {uid}.'.format(
                  firstname=self.first, uid=colored(self.uid, 'yellow',
                                                    'on_white',
                                                    attrs=['blink', 'bold'])),
                  '\nDein Startpasswort lautet {passw}.'.format(passw=colored(
                                                                self.fpass,
                                                                'green',
                                                                'on_white',
                                                                attrs=['blink',
                                                                       'bold'])
                                                                ),
                  '\nVergiss nicht es zu ändern.')

def save():
    '''
    Dumps the list of users to the backup file
    '''
    with open(backupfile, 'wb') as fp:
        pickle.dump(users, fp)


def chill(clear=True):
    '''
    Freezes the script execution, listens for any input ("any key") and clears
    the screen afterwards.
    '''
    try:
        os.system('read _')
    except whatever_it_is:
        os.system('pause')
    if clear:
        os.system('clear')


def loader(time):
    '''
    A loading animation that is being called with the amount of time,
    the system should display the animation.
    '''
    if sudomode:
        return
    time = time - 5
    if en:
        print('Loading...')
    else:
        print('Laden...')
    t_fwd = int(0.1 * time) / 70
    t_slow_fwd = int(0.3 * time) / 5
    t_rwd = int(0.2 * time) / 55
    t_finish = int(0.4 * time) / 60
    count = 0

    # up to 70 segments
    for i in range(70):
        count += 1
        print('\r{hashtag}'.format(hashtag='#' * count), end=' ')
        sleep(t_fwd)

    # up to 75 segments
    for i in range(5):
        count += 1
        print('\r{hashtag}'.format(hashtag='#' * count), end=' ')
        sleep(t_slow_fwd)

    if en:
        print('\rAn error occured.                                                          \
 \nChanges beeing reverted.\n', end=' ')
    else:
        print('\rEs ist ein Fehler aufgetreten.                                             \
\nÄnderungen werden rückgängig gemacht.\n', end=' ')

    # back to 20 segments
    for i in range(55):
        count -= 1
        print('\r{hashtag} '.format(hashtag='#' * count), end=' ')
        sleep(t_rwd)

    sleep(5)
    if en:
        print('\rLoading...          \n', end=' ')
    else:
        print('\rLaden...            \n', end=' ')

    # up to 80
    for i in range(60):
        count += 1
        print('\r{hashtag}'.format(hashtag='#' * count), end=' ')
        sleep(t_finish)
    print('\n')


def startup():
    '''
    This function recovers any users that have been stored in previous sessions
    '''
    # this is necessary since we are reassigning the var 'users' here
    global users
    print('Booting up servers...')
    if os.path.isfile(backupfile):
        print('Recovering backup file... ', end='')
        with open(backupfile, 'rb') as fp:
            users = pickle.load(fp)
        print('[{nr} users recovered]\n'.format(nr=len(users)))
    chill()


def welcome():
    '''
    Presents the user with a welcome message and a list of commands he can use.
    '''
    if en:
        print('-' * 80,
              '\n{sp}* ZIH Identity managent *\n'.format(sp=' ' * 26),
              '{sp}[Semester {n}]\n'.format(sp=' ' * 67, n=semester),
              '{sp}[{n}\n'.format(sp=' ' * 68, n="Protected]" if not sudomode else "S-OFF    ]"),
              '      1 - Matriculate a new student\n',
              '      2 - List all students\n',
              '      3 - Change password of an student\n',
              '      4 - Matriculate a student with temporary login\n',
              '      5 - Change the name in the base data\n',
              '      6 - Change the address in your base data\n\n'
              '      Um zu Deutsch zu wechseln tippe "de"\n')
    else:
        print('-' * 80,
              '\n{sp}* ZIH Identitätsmanagement *\n'.format(sp=' ' * 26),
              '{sp}[Semester {n}]\n'.format(sp=' ' * 67, n=semester),
              '{sp}[{n}\n'.format(sp=' ' * 68, n="Protected]" if not sudomode else "S-OFF    ]"),
              '      1 - Neuen Studenten immatrikulieren\n',
              '      2 - Liste der Studenten\n',
              '      3 - Passwort eines Studenten ändern\n',
              '      4 - Studenten mit temporären Login immatrikulieren\n',
              '      5 - Ändere den Namen in den Stammdaten\n',
              '      6 - Ändere die Adresse in den Stammdaten\n\n'
              '      To change to english type "en"\n')


def commands():
    '''
    To be called after welcome(). Gets an input from the user and executes
    the associated function.
    '''
    global semester
    global en
    global sudomode
    cmd = input('Deine Auswahl: ')
    if cmd == 'exit':
        if sudomode:
            quit()
        else:
            print(colored('NOPE!', 'red'))
            chill()
    random.seed()
    rand = random.randint(1, sys.maxsize) % 10
    if rand < 4 and cmd not in ['semester++', 'semester--', '42', '1337',
    							'credits', 'en', 'de', 'wartung','sudo',
                                'logout', 'exit']:
        time = random.randint(1, sys.maxsize) % 91 + 30
        loader(time)
    if cmd == '1':
        adduser()
    elif cmd == '2':
        listusers()
    elif cmd == '3':
        changepass()
    elif cmd == '4':
        adduser(True)
    elif cmd == '5':
        changename()
    elif cmd == '6':
        changeaddress()
    elif cmd == '42':
        if en:
            print('You found a secret!')
        else:
            print('Du hast ein Geheimnis gefunden!')
        changepass()
    elif cmd == '1337':
        if en:
            print('You found a secret!')
        else:
            print('Du hast ein Geheimnis gefunden!')
        credits()
    elif cmd == 'credits':
        credits()
    elif cmd == 'sudo':
        sudo()
    elif cmd == 'logout':
        logout()
    elif cmd == 'semester++':
        if semester >= 2:
            print("Auch Admins müssen bisschen mitdenken. Mehr geht nicht!")
            chill()
        else:
            if sudomode:
                semester += 1
            else:
                if en:
                    print(colored("You don't have enough permissions. This incident will be reported!", 'red'))
                else:
                    print(colored("Sie besitzen nicht die nötigen Berechtigungen. Dieser Vorfall wird gemeldet!", 'red'))
                loader(60)
            os.system('clear')
    elif cmd == 'semester--':
        if semester <= 1:
            print("Auch Admins müssen bisschen mitdenken. Weniger ist nicht!")
            chill()
        else:
            if sudomode:
                semester -= 1
            else:
                if en:
                    print(colored("You don't have enough permissions. This incident will be reported!", 'red'))
                else:
                    print(colored("Sie besitzen nicht die nötigen Berechtigungen. Dieser Vorfall wird gemeldet!", 'red'))
                loader(60)
            os.system('clear')
    elif cmd == 'en':
        print(colored('Changing language...', 'red'))
        en = True
        loader(60)
        os.system('clear')
    elif cmd == 'de':
        print(colored('Wechsele Sprache...', 'red'))
        en = False
        loader(60)
        os.system('clear')
    elif cmd == 'wartung':
        wartung()
    else:
        if en:
            print('You typed something wrong. Please try again.\n')
        else:
            print('Du hast irgendwas falsches eingetippt. Versuche es erneut.\
\n')
        commands()

def sudo():
    '''
    Switches system to sudo mode if presented with correct credentials from sudoers
    '''
    global sudomode
    if not sudomode:
        userpromt = 'Richard Matthew Stallman is watching you: ' if en else 'Richard Matthew Stallman beobachtet dich: '
        pwprompt = 'You think this is a good idea: ' if en else 'Denken Sie, dass das eine gute Idee ist: '
        username = input(userpromt)
        pw = getpass(pwprompt)
        if username in sudoers.sudoers:
            if sudoers.sudoers[username] == pw:
                sudomode = True
                os.system('clear')
            else:
                if en:
                    print(colored("You don't have enough permissions. This incident will be reported!", 'red'))
                else:
                    print(colored("Sie besitzen nicht die nötigen Berechtigungen. Dieser Vorfall wird gemeldet!", 'red'))
                loader(60)
        else:
            if en:
                print(colored("You are not in the sudoers file. This incident will be reported!", 'red'))
            else:
                print(colored("Sie sind nicht in der Sudoers Datei. Dieser Vorfall wird gemeldet!", 'red'))
            loader(60)
    else:
        if en:
            print(colored("You are already root. What do you want more?", "red"))
            chill()
        else:
            print(colored("Du bist schon root. Was willst du mehr?", "red"))
            chill()

def logout():
    '''
    Switches the system to protected non sudo mode or to wartung
    '''
    global sudomode
    if sudomode:
        sudomode = False
        chill()
    else:
        wartung()

def uid_gen():
    '''
    Generates a user id that exists only ONCE.
    '''
    double = False
    temp_id = generator()
    # check every existing user (used because the number of users is small)
    for user in users:
        if temp_id == user.uid:
            double = True
    # if the UID exists, generate a new one.
    if double:
        return uid_gen()
    else:
        return temp_id


def passwordgen():
    '''
    Returns a randomly generated password.
    '''
    return generator(16, string.ascii_uppercase + string.ascii_lowercase +
                     string.digits + string.digits)


def changepass():
    '''
    Changes the password of a user.
    '''
    changed = False
    user = ''
    if en:
        user = input('Type in your User ID: ')
    else:
        user = input('Trage deine User ID ein: ')
    for u in users:
        if user == u.uid:
            if input('Gib dein altes Passwort ein: ') != u.fpass:
                print(colored('Falsches Passwort!', 'red', attrs=['blink']))
                chill()
                return
            inp = input('Gib dein neues Passwort ein: ')
            u.password = inp
            u.fpass = len(inp) * '*'
            print('Passwort erfolgreich geändert!')
            changed = True
            save()
    if not changed:
        print('Das ist eine falsche User ID. Das war ein bisschen dumm.')
        chill()


def changename():
    '''
    Changes the name of a user when presented with the correct password
    '''
    user=''
    if en:
        user = input('Type in your User ID: ')
    else:
        user = input('Trage deine User ID ein: ')
    for u in users:
        if user == u.uid:
            if u.password == '':
                print('Bitte ändere dein Initial Passwort')
                chill()
                return
            if input('Gib dein Passwort ein: ') != u.password:
                print(colored('Falsches Passwort!', 'red', attrs=['blink']))
                chill()
            newfname = input('Gib bitte deinen neuen Vornamen ein: ')
            newlname = input('Gib bitte deinen neuen Vornamen ein: ')
            u.first = newfname
            u.last = newlname
            print('Herzlichen Glückwunsch zur Namensänderung!')
            save()
            chill()


def changeaddress():
    '''
    Changes the address of a user when presented with the correct password
    '''
    user=''
    if en:
        user = input('Type in your User ID: ')
    else:
        user = input('Trage deine User ID ein: ')
    for u in users:
        if user == u.uid:
            if u.password == '':
                print('Bitte ändere dein Initial Passwort')
                chill()
                return
            if input('Gib dein Passwort ein: ') != u.password:
                print(colored('Falsches Passwort!', 'red', attrs=['blink']))
                chill()
            newaddress = input('Gib bitte deine neue Adresse ein: ')
            u.address = newaddress
            print('Herzlichen Glückwunsch zur Adressänderung!')
            save()
            chill()


def generator(size=20, chars=string.ascii_uppercase + string.digits):
    '''
    Generates a string of certain size - a mix of letters & digits by default.
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def adduser(temorary = False):
    '''
    For adding a user to the database. Gets his credentials and creates a new
    instance of the class User.
    '''
    prompt = 'Füge einen neuen Studenten zur Datenbank hinzu.\n' if not temorary else 'Füge einen neuen Studenten mit temporären Login zur Datenbank hinzu.\n'
    print(prompt)
    fname = input('Vorname: ')
    lname = input('Nachname: ')
    address = input('Adresse: ')
    dob = input('Geburtsdatum (dd.mm.yyyy): ')
    while not re.match(r'[0-3][0-9]\.[0-1][0-9]\.[0-9]{4}', dob):
        print(colored('\nFALSCHE DATUMSANGABE!', 'red'), '\n\nLade Eingabe \
neu...')
        sleep(30)
        dob = input('Geburtsdatum (dd.mm.yyyy): ')
    users.append(User(fname, lname, dob, address))
    save()
    chill()

def listusers():
    '''
    Lists all users stored in the users list.
    '''
    global sudomode
    if not sudomode:
        if en:
            print(colored("You don't have enough permissions. This incident will be reported!", 'red'))
        else:
            print(colored("Sie besitzen nicht die nötigen Berechtigungen. Dieser Vorfall wird gemeldet!", 'red'))
        loader(60)
        return

    if len(users) == 0:
        print('Keine Studenten in der Datenbank.')
        chill()
        return
    os.system('clear')
    #                       |            |          |
    print('Vorname           Nachname     Geb.-datum User ID              ' +
          'Startpasswort \n' +
          '-' * 79)
    for user in users:
        print('{first}{space} '.format(first=user.first,
                                       space=' ' * (16 - len(user.first))) +
              '{last}{space} '.format(last=user.last,
                                      space=' ' * (12 - len(user.last))) +
              '{dob} '.format(dob=user.dob) +
              '{uid}{space} '.format(uid=user.uid,
                                     space=' ' * (20 - len(user.uid))) +
              '{fpass}{space} '.format(fpass=user.fpass,
                                       space=' ' * (16 - len(user.fpass))))
    chill()


def wartung():
    '''
    Puts the script in maintenance mode. Users can't do anything now.
    '''
    os.system('clear')
    print('\n\n\n\n\n', '-' * 80, '\n                        {wa}'.format(
        wa=colored(
            'Das System wird gerade gewartet.', 'magenta', attrs=['bold'])) +
          '\n' + ' ' * 29 + 'Bitte gehen Sie weg.\n')
    print('-' * 80)
    if(input("") != 'done'):
        wartung()
    else:
        os.system('clear')
        return


def main():
    startup()
    while True:
        welcome()
        commands()

def credits():
    if en:
        print('@Feliix42, @h4llow3En and @MarauderXtreme purveyors of aids to ESE mischief-makers are proud to present the\n')
    else:
        print('Die hochwohlgeborenen Herren @Feliix42, @h4llow3En und @MarauderXtreme präsentieren stolz den\n')
    print(colored('''
▒███████▒ ██▓ ██░ ██      ██████  ██▓ ███▄ ▄███▓ █    ██  ██▓    ▄▄▄     ▄▄▄█████▓ ▒█████   ██▀███  
▒ ▒ ▒ ▄▀░▓██▒▓██░ ██▒   ▒██    ▒ ▓██▒▓██▒▀█▀ ██▒ ██  ▓██▒▓██▒   ▒████▄   ▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
░ ▒ ▄▀▒░ ▒██▒▒██▀▀██░   ░ ▓██▄   ▒██▒▓██    ▓██░▓██  ▒██░▒██░   ▒██  ▀█▄ ▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
  ▄▀▒   ░░██░░▓█ ░██      ▒   ██▒░██░▒██    ▒██ ▓▓█  ░██░▒██░   ░██▄▄▄▄██░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
▒███████▒░██░░▓█▒░██▓   ▒██████▒▒░██░▒██▒   ░██▒▒▒█████▓ ░██████▒▓█   ▓██▒ ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
░▒▒ ▓░▒░▒░▓   ▒ ░░▒░▒   ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒▒   ▓▒█░ ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
░░▒ ▒ ░ ▒ ▒ ░ ▒ ░▒░ ░   ░ ░▒  ░ ░ ▒ ░░  ░      ░░░▒░ ░ ░ ░ ░ ▒  ░ ▒   ▒▒ ░   ░      ░ ▒ ▒░   ░▒ ░ ▒░
░ ░ ░ ░ ░ ▒ ░ ░  ░░ ░   ░  ░  ░   ▒ ░░      ░    ░░░ ░ ░   ░ ░    ░   ▒    ░      ░ ░ ░ ▒    ░░   ░ 
  ░ ░     ░   ░  ░  ░         ░   ░         ░      ░         ░  ░     ░  ░            ░ ░     ░     
░                                                                                                   
''', 'white'))

def print_doge():
    '''
    Such wow. Very Meme.
    '''
    print(colored('''
         ▄              ▄
        ▌▒█           ▄▀▒▌
        ▌▒▒▀▄       ▄▀▒▒▒▐
       ▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
     ▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
   ▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌
  ▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌
  ▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
 ▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌
 ▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
 ▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐
▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌
▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐
 ▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
 ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
  ▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌
    ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
   ▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
  ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀

Such exmatriculation. Much sorry''', 'white'))


def sigint_handler(signal, frame):
    pass

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    main()

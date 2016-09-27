#!/usr/bin/env python3
import re
import os
import sys
import pickle
import random
import string
import signal
from time import sleep
from termcolor import colored

# the global users list - is being dumped to the backup file
users = []
# semester counter
semester = 1
# location of the backup file
backupfile = './backup.pkl'
# controlls the language
en = False


class User():
    '''
    The User Class instantiates an object for each user that is created.
    '''

    def __init__(self, first, last, dob):
        self.first = first
        self.last = last
        self.dob = dob
        self.uid = uid_gen()
        self.fpass = passwordgen()
        if en:
            print('\nWelcome, {firstname}! Your USER ID is {uid}.'.format(
                  firstname=self.first, uid=colored(self.uid, 'yellow',
                                                    'on_white',
                                                    attrs=['blink', 'bold'])),
                  '\nYour one-time passwors is {passw}.'.format(passw=colored(
                                                                self.fpass,
                                                                'green',
                                                                'on_white',
                                                                attrs=['blink',
                                                                       'bold'])
                                                                ),
                  "\nDon't forget to chance it in the second semester.")
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
                  '\nVergiss nicht, es im zweiten Semester zu ändern.')
        random_abo()


def random_abo():
    '''
    When called, there's a 30% chance that the user opts in for an abbonement
    of a randomly chosen magazine.
    '''
    random.seed()
    rand = random.randint(1, sys.maxsize) % 10
    magazine, price = get_abo()
    if rand < 3:
        if en:
            print('Congratulations! You got an abbonoment of the magazine \
"{magazine}" ({now} for just {price} points per Year!). \
Please pay now.'.format(magazine=magazine,
                        now=colored('NOW', 'red',
                                    attrs=['blink']),
                        price=price))
        else:
            print('Herzlichen Glückwunsch! Du hast dich für ein Abonnement der \
Zeitschrift "{magazine}" ({now} für nur {price} Punkte pro Jahr!) entschieden. \
Bitte zahle dein Abo sofort.'.format(magazine=magazine,
                                     now=colored('JETZT', 'red',
                                                 attrs=['blink']),
                                     price=price))


def get_abo():
    '''
    Choses a random magazine from the dict below and returns the name and the
    corresponding price
    '''
    abodict = {'Bravo Girl': 2, 'Playboy': 4, 'HÖRZU': 1, 'happinez': 5,
               'Brigitte Woman': 3, 'Emotion Slow': 1, 'Tätowier Magazin': 4,
               'Federwelt': 2, 'Der LEUCHTTURM': 6, 'Bummi': 3,
               'Feuerwehrmann Sam': 4, 'Teen Wolf': 2, 'Bravo Sport': 2,
               'Gala': 4, 'Popcorn': 1}
    random.seed()
    abolist = []
    for key in abodict:
        abolist.append(key)
    i = abolist[random.randint(0, len(abolist) - 1)]
    return i, abodict[i]


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
        os.system('read')
    except whatever_it_is:
        os.system('pause')
    if clear:
        os.system('clear')


def loader(time):
    '''
    A loading animation that is being called with the amount of time,
    the system should display the animation.
    '''
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
    os.system('clear')


def welcome():
    '''
    Presents the user with a welcome message and a list of commands he can use.
    '''
    if en:
        print('-' * 80,
              '\n{sp}* ZIH Identity managent *\n'.format(sp=' ' * 26),
              '{sp}[Semester {n}]\n'.format(sp=' ' * 67, n=semester),
              '      1 - Matriculate a new student\n',
              '      2 - List all students\n',
              '      3 - Change password of an student\n\n',
              '      Um zu Deutsch zu wechseln tippe "de"\n')
    else:
        print('-' * 80,
              '\n{sp}* ZIH Identitätsmanagement *\n'.format(sp=' ' * 26),
              '{sp}[Semester {n}]\n'.format(sp=' ' * 67, n=semester),
              '      1 - Neuen Studenten immatrikulieren\n',
              '      2 - Liste der Studenten\n',
              '      3 - Passwort eines Studenten ändern\n\n',
              '      To change to english type "en"\n')


def commands():
    '''
    To be called after welcome(). Gets an input from the user and executes
    the associated function.
    '''
    global semester
    global en
    cmd = input('Deine Auswahl: ')
    if cmd == 'exit':
        quit()
    random.seed()
    rand = random.randint(1, sys.maxsize) % 10
    if rand < 4 and cmd not in ['semester++', 'semester--', '42', 'en', 'de',
                                'wartung']:
        time = random.randint(1, sys.maxsize) % 91 + 30
        loader(time)
    if cmd == '1':
        adduser()
    elif cmd == '2':
        listusers()
    elif cmd == '3':
        if semester == 2:
            changepass()
        else:
            if en:
                print('You can change passwords only in the second semester!')
            else:
                print('Das Ändern des Passworts ist nur im zweiten Semester \
möglich!')
            chill()
    elif cmd == '42':
        if en:
            print('You found a secret!')
        else:
            print('Du hast ein Geheimnis gefunden!')
        changepass()
    elif cmd == 'semester++':
        if semester >= 4:
            print("Auch Admins müssen bisschen mitdenken. Mehr geht nicht!")
            chill()
        else:
            semester += 1
            os.system('clear')
    elif cmd == 'semester--':
        if semester <= 1:
            print("Auch Admins müssen bisschen mitdenken. Weniger ist nicht!")
            chill()
        else:
            semester -= 1
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
    Changes the password of a user. Exmatriculates him if he types in
    a wrong old password.
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
                print(colored('Falsches Passwort!', 'red', attrs=['blink']),
                      '\nAus Sicherheitsgründen müssen wir dich leider \
exmatrikulieren.\nDas tut uns sehr Leid!')
                users.remove(u)
                print_doge()
                save()
                chill()
                return
            inp = input('Gib dein neues Passwort ein: ')
            u.fpass = len(inp) * '*'
            print('Passwort erfolgreich geändert!')
            changed = True
            save()
    if not changed:
        print('Das ist eine falsche User ID. Das war ein bisschen dumm.')
    random_abo()
    chill()


def generator(size=20, chars=string.ascii_uppercase + string.digits):
    '''
    Generates a string of certain size - a mix of letters & digits by default.
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def adduser():
    '''
    For adding a user to the database. Gets his credentials and creates a new
    instance of the class User.
    '''
    print('Füge einen neuen Studenten zur Datenbank hinzu.\n')
    fname = input('Vorname: ')
    lname = input('Nachname: ')
    dob = input('Geburtsdatum (dd.mm.yyyy): ')
    while not re.match(r'[0-3][0-9]\.[0-1][0-9]\.[0-9]{4}', dob):
        print(colored('\nFALSCHE DATUMSANGABE!', 'red'), '\n\nLade Eingabe \
neu...')
        sleep(30)
        dob = input('Geburtsdatum (dd.mm.yyyy): ')
    users.append(User(fname, lname, dob))
    save()
    chill()


def listusers():
    '''
    Lists all users stored in the users list.
    '''
    if len(users) == 0:
        print('Keine Studenten in der Datenbank.')
        chill()
        return
    os.system('clear')
    #                       |            |          |
    print('Vorame           Nachname     Geb.-datum User ID              ' +
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

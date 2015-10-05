'''
TODO:
varying length of user ID
translate 2 german
'''

import re
import os
import pickle
import string
import random
from time import sleep
from termcolor import colored

users = []
semester = 1
backupfile = "./backup.pkl"


class User():
    def __init__(self, first, last, dob):
        self.first = first
        self.last = last
        self.dob = dob
        self.uid = uid_gen()
        self.fpass = passwordgen()
        print("\nWelcome, {firstname}! Your USER ID is {uid}.\n".format(
            firstname=self.first, uid=colored(self.uid, "yellow", "on_white",
                                              attrs=["blink", "bold"])) + "Your one-way\
 password is {passw}. \n".format(passw=colored(self.fpass, "green", "on_white",
                                               attrs=["blink", "bold"])) + "Remember \
 to change it in your second semester.")
        random_abo()


def random_abo():
    random.seed()
    rand = random.randint(1, 15000000) % 10
    magazine, price = get_abo()
    if rand < 3:
        print("Congratulations! You just opted in for an abonnement " +
              "of the '{magazine}' for {now} just {price} Points per year! \
Please pay this now.".format(magazine=magazine, now=colored("NOW", "red",
                                                            attrs=["blink"]),
                             price=price))


def get_abo():
    abodict = {"Bravo Girl": 2, "Playboy": 4, "HÖRZU": 1, "happinez": 5,
               "Brigitte Woman": 3, "Emotion Slow": 1, "Tätowier Magazin": 4,
               "Federwelt": 2, "Der LEUCHTTURM": 6, "Bummi": 3,
               "Feuerwehrmann Sam": 4, "Teen Wolf": 2, "Bravo Sport": 2,
               "Gala": 4}
    random.seed()
    abolist = []
    for key in abodict:
        abolist.append(key)
    i = abolist[random.randint(0, len(abolist) - 1)]
    return i, abodict[i]


def save():
    with open(backupfile, 'wb') as fp:
        pickle.dump(users, fp)


def chill(clear=True):
    '''
    Makes the system 'chill' for a while and clears the screen afterwards
    '''
    try:
        os.system('read')
    except whatever_it_is:
        os.system('pause')
    if clear:
        os.system('clear')


def loader(time):
    print("Progress:")


def startup():
    '''
    This function recovers any users that have been stored in previous sessions
    '''
    # this is necessary since we are reassigning the var 'users' here
    global users
    os.system('clear')
    print("Booting up servers...")
    if os.path.isfile(backupfile):
        print("Recovering backup file... ", end="")
        with open(backupfile, 'rb') as fp:
            users = pickle.load(fp)
        print("[{nr} users recovered]\n".format(nr=len(users)))


def welcome():
    print("-"*80 +
          "\n{sp}* ZIH identity management *\n".format(sp=' '*26) +
          "{sp}[Semester {n}]\n".format(sp=' '*67, n=semester) +
          "      1 - Add a new user\n" +
          "      2 - List all users\n" +
          "      3 - Change a users password\n")


def commands():
    global semester
    cmd = input("Your choice? ")
    if cmd == "exit":
        quit()
    random.seed()
    rand = random.randint(1, 15000000) % 10
    if rand < 4:
        print("The system is currently experiencing some problems.\n" +
              "Please stand by...")
        # sleep(120) TODO
    if cmd == "1":
        adduser()
    elif cmd == "2":
        listusers()
    elif cmd == "3":
        if semester == 2:
            changepass()
        else:
            print("You can only change your password in the second semester!")
            chill()
    elif cmd == "42":
        print("You found a secret!")
        changepass()
    elif cmd == "semester++":
        semester += 1
        os.system('clear')
    else:
        print("Seems like you mistyped something. Try again.\n")
        commands()


def uid_gen():
    '''
    generates a user id that exists only ONCE
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
    return generator(16, string.ascii_uppercase + string.ascii_lowercase +
                     string.digits + string.digits)


def changepass():
    changed = False
    user = input("Please enter your User ID: ")
    for u in users:
        if user == u.uid:
            inp = input("Please enter your new password: ")
            u.fpass = len(inp) * '*'
            print("Password successfully changed!")
            changed = True
            save()
    if not changed:
        print("You entered a wrong User ID. That's a little bit dumb.")
    random_abo()
    chill()


def generator(size=20, chars=string.ascii_uppercase + string.digits):
    '''
    Generates a string of certain size - a mix of letters & digits by default
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def adduser():
    print("Adding a new user to the database.\n")
    fname = input("Please enter your first name: ")
    lname = input("Please enter your last name: ")
    dob = input("Please enter your date of birth (dd.mm.yyyy): ")
    while not re.match(r'[0-3][0-9]\.[0-1][0-9]\.[0-9]{4}', dob):
        print(colored("\nWRONG DATE!", "red"), "\n\nreloading input...")
        sleep(30)
        dob = input("Please enter your date of birth (dd.mm.yyyy): ")
    users.append(User(fname, lname, dob))
    save()
    chill()


def listusers():
    if len(users) == 0:
        print("No users stored in the database.")
        return
    os.system('clear')
    print('First Name       Last Name    D.o.B.     User ID              ' +
          'One-Way Password \n' +
          '-'*79)
    for user in users:
        print('{first}{space} '.format(first=user.first,
                                       space=' '*(16-len(user.first))) +
              '{last}{space} '.format(last=user.last,
                                      space=' '*(12-len(user.last))) +
              '{dob} '.format(dob=user.dob) +
              '{uid}{space} '.format(uid=user.uid,
                                     space=' '*(20-len(user.uid))) +
              '{fpass}{space} '.format(fpass=user.fpass,
                                       space=' '*(16-len(user.fpass))))
    chill()


def main():
    startup()
    while True:
        welcome()
        commands()

if __name__ == '__main__':
    main()

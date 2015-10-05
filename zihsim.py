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
        print("\nWillkommen, {firstname}! Deine USER ID ist {uid}.\n".format(
            firstname=self.first, uid=colored(self.uid, "yellow", "on_white",
                                              attrs=["blink", "bold"])),
              "Dein Startpasswort lautet {passw}. \n".format(passw=colored(
                                                             self.fpass,
                                                             "green",
                                                             "on_white",
                                                             attrs=["blink",
                                                                    "bold"])),
              "Vergiss nicht, es im zweiten Semester zu ändern.")
        random_abo()


def random_abo():
    random.seed()
    rand = random.randint(1, 15000000) % 10
    magazine, price = get_abo()
    if rand < 3:
        print("Herzlichen Glückwunsch! Du hast dich für ein Abonnement der \
Zeitschrift '{magazine}' {now} für nur {price} PPunkte pro Jahr! \
Please pay this now.".format(magazine=magazine, now=colored("JETZT", "red",
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
    print("-" * 80,
          "\n{sp}* ZIH Identitätsmanagement *\n".format(sp=' ' * 26),
          "{sp}[Semester {n}]\n".format(sp=' ' * 67, n=semester),
          "      1 - Neuen Studenten immatrikulieren\n",
          "      2 - Liste der Studenten\n",
          "      3 - Passwort eines Studenten ändern\n")


def commands():
    global semester
    cmd = input("Deine Auswahl: ")
    if cmd == "exit":
        quit()
    random.seed()
    rand = random.randint(1, 15000000) % 10
    if rand < 4:
        print("Der Server antwortet nicht.\n" +
              "Bitte warten...")
        # sleep(120) TODO
    if cmd == "1":
        adduser()
    elif cmd == "2":
        listusers()
    elif cmd == "3":
        if semester == 2:
            changepass()
        else:
            print("Das Ändern des Passworts ist nur im zweiten Semester möglich!")
            chill()
    elif cmd == "42":
        print("Du hast ein Geheimnis gefunden!")
        changepass()
    elif cmd == "semester++":
        semester += 1
        os.system('clear')
    else:
        print("Du hast irgendwas falschen getippt. Versuche es erneut.\n")
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
    user = input("Trage deine User ID ein: ")
    for u in users:
        if user == u.uid:
            inp = input("Gib dein neues Passwort ein: ")
            u.fpass = len(inp) * '*'
            print("Passwort erfolgreich geändert!")
            changed = True
            save()
    if not changed:
        print("Das ist eine falsche User ID. Das war ein bisschen dumm.")
    random_abo()
    chill()


def generator(size=20, chars=string.ascii_uppercase + string.digits):
    '''
    Generates a string of certain size - a mix of letters & digits by default
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def adduser():
    print("Füge einen neuen Studenten zur Datenbank hinzu.\n")
    fname = input("Vorname: ")
    lname = input("Nachname: ")
    dob = input("Gebutsdatum (dd.mm.yyyy): ")
    while not re.match(r'[0-3][0-9]\.[0-1][0-9]\.[0-9]{4}', dob):
        print(colored("\nFALSCHE DATUMSANGABE!", "red"), "\n\nLade Eingabe \
neu...")
        sleep(30)
        dob = input("Gebutsdatum (dd.mm.yyyy): ")
    users.append(User(fname, lname, dob))
    save()
    chill()


def listusers():
    if len(users) == 0:
        print("Keine Sudenten in der Datenbank.")
        return
    os.system('clear')
    #                       |            |          |
    print('Vorame           Nachname     Geb.-datum User ID              ' +
          'Startpassword \n' +
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


def main():
    startup()
    while True:
        welcome()
        commands()

if __name__ == '__main__':
    main()

import datetime
import random
import select
import sys
import time
from collections import Counter
from classes import Gift, SecretSanta
from utils import clear, sleep


def allocate_santas(secret_santa):
    timeout_total = time.time() + 20
    while True:
        if time.time() > timeout_total:
            return

        gift_pool = []
        for r in secret_santa.rounds:
            for santa in secret_santa.santas:
                gift_pool.append(Gift(recipient=santa, budget=r.budget))

        for santa in secret_santa.santas:
            budget_list = [r.budget for r in secret_santa.rounds]

            timeout = time.time() + 3  # allowed seconds in the loop
            while len(santa.gifts) != secret_santa.number_rounds():
                if time.time() > timeout:
                        break
                if secret_santa.unique_recipients:
                    possible_gifts = [g for g in gift_pool if g.recipient != santa and
                                      g.budget in budget_list and not
                                      santa.is_recipient(g.recipient)]
                else:
                    possible_gifts = [g for g in gift_pool if g.recipient != santa and
                                      g.budget in budget_list]
                if possible_gifts:
                    random_gift = random.choice(possible_gifts)
                    santa.add_gift(random_gift)
                    budget_list.remove(random_gift.budget)
                    gift_pool.remove(random_gift)

        ok = True
        for santa in secret_santa.santas:
            if not len(santa.gifts) == secret_santa.number_rounds():
                ok = False
                break
        if ok:
            return secret_santa


def setup():
    secret_santa = SecretSanta()
    year = datetime.date.today().year
    counter = 0
    ok = False

    clear()
    print('\n' + '-' * 40 + " SECRET SANTA {} ".format(year) + '-' * 40 + '\n\n')
    sleep(2)
    print("first enter the participating santas ...")
    sleep(3.5)
    print("enter one name at a time ...")
    sleep(2)
    print("or 'done' when finished ...")
    sleep(2)
    print("'delete' will remove the last name ..\n")
    sleep(2)

    while not ok:
        if counter:
            clear()
            print('\n' + '-' * 40 + " SECRET SANTA {} ".format(year) + '-' * 40 + '\n\n')

            if secret_santa.santas:
                print("'done' when finished ..")
                print("'delete' will remove the last name ..\n")
                print('--------- santas ---------')
                for santa in secret_santa.santas:
                    print(santa.name)
                print('--------------------------')
            else:
                print("first enter the participating santas ...")
                print("enter one name at a time ...")
                print("or 'done' when finished ...")
                print("'delete' will remove the last name ..\n")

        santa_name = input('\nenter done to finish >>>>>>> ')
        if santa_name and type(santa_name) == str and santa_name not in secret_santa.all_names():
            if santa_name.lower() == "done":
                if len(secret_santa.santas) >= 3:
                    ok = True
                else:
                    print("\ngotta have at least 3 santas yo !!\n")
                    sleep(2)
            elif santa_name.lower() == "delete":
                if len(secret_santa.santas) > 0:
                    del secret_santa.santas[-1]
                else:
                    print('\nthere is nothing to delete!')
                    sleep(2)
            else:
                secret_santa.add_santa(santa_name)
        else:
            if santa_name in secret_santa.all_names():
                print('\nthat santa is already in the list !')
                sleep(2)
            elif santa_name:
                print('\ninvalid input... do it again')
                sleep(2)
        counter += 1

    clear()
    print('\nok ...\n')
    sleep(2)

    print('how many rounds? i.e how many gifts will each person buy?\n')
    ok = False
    while not ok:
        number_rounds = input('>>>>>>> ')
        try:
            number_rounds = int(number_rounds)
            ok = True
        except ValueError:
            print('\nmust be an integer ..\n')
            continue

    while secret_santa.number_rounds() != number_rounds:
        budget = input('\ngift budget for round {}? ($) '
                       '>>>> '.format(secret_santa.number_rounds() + 1))
        try:
            budget = int(budget)
            secret_santa.add_round(budget=budget)
        except ValueError:
            print('\nmust be an integer ..\n')
            continue

    clear()
    print('\nok ...\n')

    if secret_santa.number_rounds() > 1:
        sleep(2)
        print('do you want to enforce each santa being allocated the same person only once?\n')
        sleep(4)
        print("'y' to enforce unique recipients")
        print("'n' to leave it up to chance\n")
        ok = False
        while not ok:
            choice = input('y/n >>>>>>> ').lower()
            if type(choice) == str and choice in ('y', 'n'):
                if choice == 'n':
                    secret_santa.unique_recipients = True
                ok = True
            else:
                if choice:
                    print('\ninvalid choice... do it again\n')
                    sleep(1)

    clear()
    print('\nok ...\n')

    sleep(2)
    for santa in secret_santa.santas:
        print(santa.name)
        sleep(1)
    sleep(2)
    print("\nyou'll be giving gifts to {} other santas ...".format(secret_santa.number_rounds()))
    sleep(2)
    if secret_santa.unique_recipients:
        print("\nand you can't get the same person more than once ...")
    else:
        print("\nand you could get the same person more than once ...")

    sleep(2)
    print('\n\nready ...\n\n')
    sleep(4)

    for i in range(7):
        clear()
        print('randomly allocating santas ' + '.' * i)
        sleep(1)
    return secret_santa


def check(secret_santa):
    for santa in secret_santa.santas:
        budgets = []
        for gift in santa.gifts:
            budgets += [gift.budget]
        budgets_expected = [r.budget for r in secret_santa.rounds]
        if not Counter(budgets) == Counter(budgets_expected):
            print("\nshit.....")
            sleep(1)
            print("\nit didn't work out evenly ..")
            return False
    print("\nsweeeeeeeeeeeeeeeet ..")
    sleep(1)
    print('\ndone ... it worked out allll good!')
    time.sleep(1)
    return True


def show_individual(santa):
    ok = False
    while not ok:
        print('\n---------------------------- {} ----------------------------'.format(santa.name))
        print('\nto see who you got now >> s')
        print('for a code which can be decoded online >> c')
        print('to skip and go to the next santa >> n')
        choice = input('\nenter your choice >>>>>> ').lower()
        if type(choice) == str and choice in ('s', 'c', 'n'):
            ok = True
        else:
            clear()
            print('\ninvalid choice... do it again')
            continue

    if choice == 's':
        print('\nok, {} you will be giving to ...\n'.format(santa.name))
        santa.see_now()
        sleep(2)
        input('\nhave you remembered them? press enter to clear the screen ..')
        clear()
    elif choice == 'c':
        url = "https://www.base64decode.org/"
        sleep(1)
        print("\nok .. here's the code for {} ..\n".format(santa.name))
        sleep(1)
        print(santa.see_code())
        sleep(1)
        print("\nto reveal, copy the whole code and go to {}".format(url))
        input('\ndone? press enter to continue ..')
        clear()
    elif choice == 'n':
        clear()
        return


def show(secret_santa):
    ok = False
    while not ok:
        print('to see results individually >> i')
        print('to see results for all santas >> santas')
        print('to see codes for all santas >> codes')
        print('codes for all santas in a file >> codesf')
        choice = input('\nenter your choice >>>>>> ').lower()
        if type(choice) == str and choice in ('i', 'santas', 'codes', 'codesf'):
            ok = True
        else:
            clear()
            print('\ninvalid choice... do it again')
            continue

    if choice == 'i':
        for santa in secret_santa.santas:
            sleep(1.5)
            show_individual(santa)
    elif choice == 'santas':
        for santa in secret_santa.santas:
            print('\n{} giving to ...'.format(santa.name))
            santa.see_now()
            sleep(0.5)
        sleep(2)
        input('\npress enter to clear the screen ..')
        clear()
    elif choice == 'codes':
        print("\nok .. here are the codes..\n")
        for santa in secret_santa.santas:
            print(santa.name)
            print(santa.see_code())
        url = "https://www.base64decode.org/"
        print("\nto reveal, copy the whole code and go to {}".format(url))
        input('\ndone? press enter to continue ..')
        clear()
    elif choice == 'codesf':
        with open('santa_results.txt', 'w') as f:
            for santa in secret_santa.santas:
                f.write('\n{}\n'.format(santa.name))
                f.write('{}\n'.format(santa.see_code()))
            url = "https://www.base64decode.org/"
            f.write("\nto reveal, copy the whole code and go to {}".format(url))
        sleep(1)
        print('\n\nthe results have been saved to a file ..')
        input('\ndone? press enter to continue ..')
        clear()


def last_chance(secret_santa):
    for seconds in range(20, -1, -1):
        clear()
        print("\nlast chance! quitting and deleting in {} seconds "
              "unless you press enter ".format(seconds) + "." * (seconds * -1 + 20))
        i, o, e = select.select([sys.stdin], [], [], 1)
        if i:
            input('')
            see_again(secret_santa)
    return


def see_again(secret_santa):
    done = False
    while not done:
        print("\nif you're finished press f")
        print("if you need to see results for someone again, enter their name")
        sleep(1)
        ok = False
        while not ok:
            choice = input("\n(f/name) >>>>>>>>>>>>>>>>>>>> ").lower()
            if type(choice) == str and choice in secret_santa.all_names() or choice == 'f':
                if choice == 'f':
                    ok = True
                    done = True
                else:
                    show_individual(secret_santa.get_santa(choice))
                    ok = True
            else:
                print('\ninvalid choice... do it again')
    print('\nfinished! merry christmas !!!')
    sleep(5)
    last_chance(secret_santa)


def main():
    secret_santa_setup = setup()
    fail_count = 0
    while fail_count <= 3:
        secret_santa = allocate_santas(secret_santa_setup)
        if not check(secret_santa):
            fail_count += 1
            if fail_count == 3:
                sleep(1)
                print('faillllure ....')
                sleep(1)
                print('tried 3 times ..')
                sleep(1)
                print('giving up now ..')
                sleep(2)
                print('\nit might not be possible with that setup ...')
                sleep(2)
                if secret_santa.unique_recipients:
                    print('\ntry again without enfocing unique recipients ...\n\n')
                    sleep(5)
                return
            clear()
            print('\ntrying again ...')
            sleep(4)
        else:
            break
    sleep(1)
    print("time to see who got who .......\n")
    sleep(1)

    show(secret_santa)

    clear()
    print("\nok.. that's everyone ..")
    sleep(2)

    see_again(secret_santa)


if __name__ == '__main__':
    main()

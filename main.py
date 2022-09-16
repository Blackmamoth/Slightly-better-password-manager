from manager import PasswordManager
from getpass import getpass
from colorama import Fore
import os

instance = PasswordManager()


def add_password() -> None:
    password_for: str = input('Password for: ')
    password: str = getpass('Enter password: ')
    instance.add_password(
        password_for=password_for, password=password)


def show_all_passwords() -> None:
    print('Password-for\t\tPassword')
    for object in instance.get_all_passwords():
        password_for: str = object.get('password_for')
        password: str = object.get('password')
        print(f'{password_for}\t\t\t{password}')


def show_single_password() -> None:
    password_for: str = input('Show password for: ')
    get_pass: str = instance.get_password(password_for=password_for)
    password: str = get_pass.get('password')
    print('Password-for\t\tPassword')
    print(f'{password_for}\t\t\t{password}')


def update_password() -> None:
    password_for: str = input('Update password for: ')
    new_pass: str = input(f'Enter new password for {password_for}: ')
    proceed: str = input(
        f'Are you sure you want to update password for {password_for} (y/n): ')
    if 'y' in proceed or 'Y' in proceed:
        instance.update_password(
            password_for=password_for, new_password=new_pass)


def delete_password() -> None:
    password_for: str = input('Delete password for: ')
    proceed: str = input(
        f'Are you sure you want to delete password for {password_for} (y/n): ')
    if 'y' in proceed or 'Y' in proceed:
        instance.delete_password(password_for=password_for)


def clear_screen() -> None:
    os.system('clear' if os.name == 'posix' else 'cls')


if __name__ == '__main__':
    while True:
        if not instance.verified:
            root_pass: str = getpass(Fore.BLUE +
                                     'Enter your root password to perform the above actions: ')
            instance.verify_root_password(root_pass)
        instance.show_options()
        option: int = int(input(Fore.CYAN + 'Choose an option between 1-6: '))
        clear_screen()
        if option == 1:
            add_password()
        elif option == 2:
            show_all_passwords()
        elif option == 3:
            show_single_password()
        elif option == 4:
            update_password()
        elif option == 5:
            delete_password()
        elif option == 6:
            print(Fore.CYAN + 'Bye')
            break
        else:
            print(Fore.RED + 'Please choose an option between 1-6')

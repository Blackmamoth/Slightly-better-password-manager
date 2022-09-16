from config import DB, DB_HOST, DB_PASS, DB_USER, ROOT_PASS, KEY, USER
from cryptography.fernet import Fernet
from pymysql.cursors import DictCursor
from pymysql.err import IntegrityError
from getpass import getpass
from colorama import Fore
import pymysql
import hashlib


class PasswordManager:

    def __init__(self):
        self.connection: pymysql.Connection = pymysql.connect(
            host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=DB, cursorclass=DictCursor)
        self.cursor: DictCursor = self.connection.cursor()
        self.root_pass: str = ROOT_PASS
        self.verified: bool = False
        if not self.root_pass:
            root_pass = getpass(
                Fore.BLUE + f"Enter a root password for {USER}: ")
            hashed_pass = self.__hash_password(password=root_pass)
            with open('.env', 'a') as env_file:
                env_file.write(f'\nROOT_PASS={hashed_pass}')
        self.key = KEY
        if not self.key:
            self.key = Fernet.generate_key().decode('utf-8')
            with open('.env', 'a') as env_file:
                env_file.write(f'\nKEY={self.key}')
        self.fernet = Fernet(self.key)

    def verify_root_password(self, password: str) -> bool:
        hashed_password: str = self.__hash_password(password=password)
        if self.root_pass == hashed_password:
            self.verified = True
            return
        print(Fore.RED + "Root password does not match, you are not allowed to perform any actions")
        exit(1)

    def show_options(self) -> None:
        print(Fore.GREEN + '1. Add a new password')
        print(Fore.GREEN + '2. Show all passwords')
        print(Fore.GREEN + '3. Show a single password')
        print(Fore.GREEN + '4. Update a password')
        print(Fore.GREEN + '5. Delete a password')
        print(Fore.GREEN + '6. EXIT')

    def __hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def __encrypt_password(self, password: str) -> str:
        return self.fernet.encrypt(password.encode('utf-8')).decode('utf-8')

    def __decrypt_password(self, password: str) -> str:
        return self.fernet.decrypt(password.encode('utf')).decode('utf-8')

    def add_password(self, password_for: str, password: str) -> None:
        try:
            query: str = "INSERT INTO manager(password_for, password) VALUES (%s, %s);"
            encrypted_password: str = self.__encrypt_password(password=password)
            insert: int = self.cursor.execute(
                query=query, args=[password_for.lower(), encrypted_password])
            self.connection.commit()
            if insert == 1:
                print(Fore.GREEN +
                      f'Password for {password_for} successfully saved')
        except IntegrityError as exception:
            error_code = exception.args[0]
            if error_code == 1048:
                print(Fore.RED + 'Password-For and Password field cannot be Empty')
            if error_code == 1062:
                print(
                    Fore.RED + 'You already have a password for that application/website')

    def get_password(self, password_for: str) -> dict:
        try:
            query: str = "SELECT password_for, password FROM manager WHERE password_for = %s;"
            self.cursor.execute(query=query, args=[password_for.lower()])
            result = self.cursor.fetchone()
            password_for = str(result.get('password_for')).capitalize()
            password = self.__decrypt_password(result.get('password'))
            return {'password_for': password_for, 'password': password}
        except Exception as e:
            print(Fore.RED + e.args[1])

    def get_all_passwords(self) -> list[dict]:
        query: str = "SELECT password_for, password FROM manager;"
        self.cursor.execute(query=query)
        result = self.cursor.fetchall()
        result = [{'password_for': item['password_for'], 'password':self.__decrypt_password(
            item['password'])} for item in result]
        return result

    def update_password(self, password_for: str, new_password: str) -> None:
        try:
            new_password = self.__encrypt_password(new_password)
            query: str = "UPDATE manager SET password = %s WHERE password_for = %s;"
            update = self.cursor.execute(
                query=query, args=[new_password, password_for.lower()])
            if update == 0:
                print(
                    Fore.RED + f'There is no password set for {password_for}')
                return
            self.connection.commit()
            print(Fore.GREEN +
                  f'Password for {password_for} successfully updated')
        except Exception as e:
            print(Fore.RED + e.args[1])

    def delete_password(self, password_for: str) -> None:
        try:
            query: str = "DELETE FROM manager WHERE password_for = %s;"
            delete_record = self.cursor.execute(
                query=query, args=[password_for.lower()])
            if delete_record == 0:
                print(
                    Fore.RED + f'There is no password set for {password_for}')
                return
            self.connection.commit()
            print(Fore.GREEN +
                  f'Password-For {password_for} successfully deleted')
        except Exception as e:
            print(Fore.RED + e.args[1])

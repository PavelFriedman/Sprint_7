import random
import string
from faker import Faker


class Helper:
    @staticmethod
    def credentials(): # креды для создания курьера
        fake = Faker()
        login = fake.name()
        password = fake.password()
        first_name = fake.first_name()
        return {
            "login": login,
            "password" : password,
            "first_name" : first_name
        }

    @staticmethod
    def random_string(length=6):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(random.choices(characters, k=length))
        return random_string

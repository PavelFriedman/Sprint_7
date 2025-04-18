# helpers.py

from faker import Faker

fake = Faker()
fakeRU = Faker(locale='ru_RU')

def create_random_login():
    # Для логина можно использовать fake.user_name()
    return fake.user_name()

def create_random_password():
    return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

def create_random_firstname():
    return fakeRU.first_name()

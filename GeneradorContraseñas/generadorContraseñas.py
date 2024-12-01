import string
import random

def run():

    length = int(input('Enter lenght of password: '))
    password = string.ascii_letters + string.punctuation + string.digits

    password = "".join(random.choice(password) for i in range(length))

    print(password)


if __name__ == '__main__':
    run()
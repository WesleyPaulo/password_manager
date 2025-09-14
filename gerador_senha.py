import random

class PasswordGenerator():

    alphabet = """!"#$%&'()*+-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
    number = "0123456789"
    alphA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha = "abcdefghijklmnopqrstuvwxyz"
    sla = """!"#$%&'()*+-./:;<=>?@[\\]^_`{|}~"""

    def generate_password(self):
        lenght = random.randint(12,60)
        password = ""
        password += random.choice(self.alpha)
        password += random.choice(self.alphA)
        password += random.choice(self.number)
        password += random.choice(self.sla)
        
        for i in range(lenght):
            password = password + random.choice(self.alphabet)

        password_list = list(password)
        random.shuffle(password_list)
        
        return  "".join(password_list)

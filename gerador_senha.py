import random

alphabet = """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
number = "0123456789"
alphA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = "abcdefghijklmnopqrstuvwxyz"
sla = """!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"""

def generate_password():
    lenght = random.randint(12,60)
    password = ""
    password += random.choice(alpha)
    password += random.choice(alphA)
    password += random.choice(number)
    password += random.choice(sla)
    
    for i in range(lenght):
        password = password + random.choice(alphabet)

    password_list = list(password)
    random.shuffle(password_list)
    
    return  "".join(password_list)

senha = generate_password()
print(senha)
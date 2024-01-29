
def isPrime(n):

    if n == 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False
    
    return True


def isPalidrome(n):
    return n == n[::-1]


user = [
    [
        {
            "id" : 1,
            "password" : 1234,
            "balance" : 10000,
            "name" : "Dibbyo Roy"
        },
        {
            "id" : 2,
            "password" : 1234,
            "balance" : 10000,
            "name" : "Abdullah Ashik"

        },
        {
            "id" : 3,
            "password" : 1234,
            "balance" : 10000,
            "name" : "Abir Hasan"
        }
    ]
    ]

def getName(id, password):
    for i in range(len(user)):
        for j in range(len(user[i])):
            if user[i][j]["id"] == id and user[i][j]["password"] == password:
                return user[i][j]["name"]
    return False

def getBalance(id, password):
    for i in range(len(user)):
        for j in range(len(user[i])):
            if user[i][j]["id"] == id and user[i][j]["password"] == password:
                return user[i][j]["balance"]
    return -1


def deposit(id, password, amount):
    for i in range(len(user)):
        for j in range(len(user[i])):
            if user[i][j]["id"] == id and user[i][j]["password"] == password:
                user[i][j]["balance"] += amount
                return user[i][j]["balance"]
    return -1


def withdraw(id, password, amount):
    for i in range(len(user)):
        for j in range(len(user[i])):
            if user[i][j]["id"] == id and user[i][j]["password"] == password:
                user[i][j]["balance"] -= amount
                return user[i][j]["balance"]
    return -1


    

    
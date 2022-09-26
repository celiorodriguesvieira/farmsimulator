import random


def heater_on(min=30, max=33):
    # return temperature(min, max)
    return 10


def temperature(variavel=0):
    client.publish('v1/'+user+'/things/'+client_id +
                   '/data/0', random.randrange(80, 100))


def moisture():
    return random.randrange(0, 100)


def somar():
    return 2 + 2


def heater(state: str):
    if state == "on":
        temperature(200)
    else:
        print("ta off")

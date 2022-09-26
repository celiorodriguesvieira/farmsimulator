import paho.mqtt.client as mqtt
import time
from definitions import user, password, client_id, server, port
import random

is_heater_on = False
max_temp = 30
target_humidity = 60

global tomato_temperature
tomato_temperature = random.randrange(5, 10)

global tomato_humidity
tomato_humidity = 100

global carrot_temperature
carrot_temperature = random.randrange(10, 20)

global carrot_humidity
carrot_humidity = 100


def message(client, user_data, msg):
    vector = msg.payload.decode().split(',')
    heater("on" if vector[1] == "1" else "off")
    client.publish(f'v1/{user}/things/{client_id}/response', f'ok,{vector[0]}')
    print(vector)


# Conexão inicial
client = mqtt.Client(client_id)
client.username_pw_set(user, password)
client.connect(server, port)


# Subscribe
client.on_message = message
client.subscribe(f'v1/{user}/things/{client_id}/cmd/2')
client.loop_start()


def update_channel(channel=0, value=0):
    client.publish(f'v1/{user}/things/{client_id}/data/{channel}', value)


def heater(state: str):
    global is_heater_on
    if state == "on":
        is_heater_on = True
    else:
        is_heater_on = False


def increment_temperature(temp=0):
    next_temp = temp + random.randrange(1, 15)
    if (next_temp < max_temp):
        return next_temp
    else:
        return max_temp


def decrement_temperature(temp=0):
    next_temp = temp - random.randrange(1, 10)
    if (next_temp > 0):
        return next_temp
    else:
        return 0


def increment_humidity(hum=0):
    next_humidity = hum + random.randrange(1, 15)

    if (next_humidity < 100):
        return next_humidity
    else:
        return 100


def decrement_humidity(hum=0):
    next_humidity = hum - random.randrange(5, 10)

    if (next_humidity > target_humidity):
        return next_humidity
    else:
        return target_humidity


# Comportamento do sistema
while True:
    tomato_channel = 0
    tomato_humidity_channel = 1

    carrot_channel = 2
    carrot_humidity_channel = 3

    if (is_heater_on):
        # tomato
        tomato_temperature = increment_temperature(tomato_temperature)
        update_channel(tomato_channel, tomato_temperature)
        tomato_humidity = decrement_humidity(tomato_humidity)
        update_channel(tomato_humidity_channel, tomato_humidity)
        # carrot
        carrot_temperature = increment_temperature(carrot_temperature)
        update_channel(carrot_channel, carrot_temperature)
        carrot_humidity = decrement_humidity(carrot_humidity)
        update_channel(carrot_humidity_channel, carrot_humidity)
    else:
        # tomato
        tomato_temperature = decrement_temperature(tomato_temperature)
        update_channel(tomato_channel, tomato_temperature)
        tomato_humidity = increment_humidity(tomato_humidity)
        update_channel(tomato_humidity_channel, tomato_humidity)
        # carrot
        carrot_temperature = decrement_temperature(carrot_temperature)
        update_channel(carrot_channel, carrot_temperature)
        carrot_humidity = increment_humidity(carrot_humidity)
        update_channel(carrot_humidity_channel, carrot_humidity)

    time.sleep(5)

# client.disconnect()

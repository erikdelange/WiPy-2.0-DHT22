from machine import Pin

import dht22

dht = device(Pin.exp_board.G22)

for _ in range(5):
    if dht.trigger() == True:
        print("RH = {}%  T = {}C".format(dht.humidity, dht.temperature))
    else:
        print(dht.status)

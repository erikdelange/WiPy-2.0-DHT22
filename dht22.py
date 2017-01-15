# dht22.py
#
# Example code how to interface a WiPy 2.0 with a DHT22 temperature and humidity sensor.

from machine import Pin
import machine
import time

# The DHT22 sends 5 bytes with data, so in total 40 bits.
# Each bit is represented by the duration (high-time) of a pulse.
# This list will store the pulse-lengths (in us).
pulse = [None] * 40

# sda connects the WiPy to the data pin of the DHT22.
# I use a 4K7 external pull-up resistor.
sda = Pin(Pin.exp_board.G22, mode=Pin.OUT, pull=None)

# Ensure at least 2 seconds waiting time between measurments.
sda(1)
time.sleep(2)

# Unfortunately interrupt handling occupies the WiPy longer then pulse lengths,
# and will cause us to miss pulses, so disable interupts while receiving data.
# Caveat of this aproach: if communication fails the WiPy will freeze (which
# sometimes happens).
state = machine.disable_irq()

# Send start signal (1ms Low).
sda(0)
time.sleep_ms(1)

# Switch WiPy to receiving mode.
sda.init(mode=Pin.IN, pull=None)

time.sleep_us(20)

# Record the pulse-length for 40 pulses.
for i in range(40):
    # each high is preceded by a (50 us) low
    while sda() == 0:
        pass
    start = time.ticks_us()
    while sda() == 1:
        pass
    pulse[i] = time.ticks_us() - start

machine.enable_irq(state)

# Print measured pulse-lengths.
# The pulse for a 0 bit is 26 us long and 70us for a 1 bit.
# Here I use a length of 50 us to distinguish 0 and 1 bits.
if 1:
    for i in range(len(pulse)):
        if pulse[i] != None:
            print("measurement {:2}: {:3} us - {}".format(i, pulse[i], "0" if pulse[i] < 50 else "1"))

data = [0] * 5  # extract 5 bytes in here

# Translate 8 bits to a byte (and do that 5 times)
for n in range(5):
    b = 0
    for i in range(8):
        b <<= 1
        if pulse[n * 8 + i] > 50:
            b += 1
    data[n] = b

int_rh, dec_rh, int_t, dec_t, csum = data

print("raw data:", int_rh, dec_rh, int_t, dec_t, csum)

sum = int_rh + dec_rh + int_t + dec_t

print("checksum:", sum & 0xFF)

if (sum & 0xFF) != csum:
    print("checksum error")

humidity = ((int_rh * 256) + dec_rh) / 10

temperature = (((int_t & 0x7F) * 256) + dec_t) / 10
if (int_t & 0x80) > 0:
    temperature *= -1

print("RH = {}%  T = {}C".format(humidity, temperature))

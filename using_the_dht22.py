# using_the_dht22.py
#
# How to interface a WiPy 2.0 with a DHT22 temperature and humidity sensor.

from machine import Pin

import pycom
import time

# Hardware setup:
# - Connect expansion board pin G22 to the DHT22 sensor data bus (SDA) pin.
# - Use an 4K7 external pull-up resistor on SDA.

pin = Pin(Pin.exp_board.G22, mode=Pin.OPEN_DRAIN)

# Enforce a 2 seconds waiting time between measurements.
pin(1)
time.sleep(2)

# Send start signal = 1ms low.
pin(0)
time.sleep_ms(1)

# The DHT22 will repond with an acknowledge signal of 80 us high.
# Then 5 bytes with data are emited, so in total 40 bits.
# Each bit is represented by the duration of the high-time of a pulse, and
# every bit is preceded by a 50 us low.
# List 'pulses' will store the duration of the low- and high-pulses (in us).

pulses = pycom.pulses_get(pin, 100)

pin.init(Pin.OPEN_DRAIN)

# Display the raw measurements
if 1:
    print(len(pulses), "pulses measured")
    for i, (level, duration) in enumerate(pulses):
        print("i = {:2} level: {}  duration: {} us".format(i, level, duration))

# Extract the relevant bits to list 'bits' and skip the acknowledge high
bits = []

for level, duration in pulses[1:]:
    if level == 1:
        bits.append(0 if duration < 50 else 1)  # 50 us demarcation between 0 and 1

if 1:
    print(len(bits), "bits")
    print(bits)

# Translate the 40 bits into 5 data bytes
data = [0] * 5

for n in range(5):
    byte = 0
    for i in range(8):
        byte <<= 1
        byte += bits[n * 8 + i]
    data[n] = byte

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

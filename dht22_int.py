# dht22_int.py
#
# Use interrupts to measure time between edges of the pulses the DHT22 sends.
# Cannot get this to work; the interrupt routine does not return fast to enough
# to capture accurate timings.
# According to the DHT22 datasheet we should see lengths of 26, 50 and 70 us.

from machine import Pin
import array
import time


def interrupt(arg):
    global index
    global edge

    edge[index] = time.ticks_us()
    index += 1

# Fastest way to store the measurements is a pre-allocated array of longs.
edge = array.array("l",  (0 for i in range(0, 84)))
index = 0

sda = Pin(Pin.exp_board.G22, mode=Pin.OUT, pull=None)

# Run interrupt routing on rising and falling edge of pulse.
sda.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, interrupt)

# Ensure at least 2 seconds waiting time between measurments.
sda(1)
time.sleep(2)

# Send start signal (1ms Low).
sda(0)
time.sleep_ms(1)

# Switch WiPy to receiving mode.
sda.init(mode=Pin.IN, pull=None)

# Give data transfer enough time to complete.
time.sleep_ms(10)

# Disable interrupt handler
sda.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, None)

for i in range(1, len(edge)):
    if edge[i] != 0:
        print("measurement {:2}: {:3} uS".format(i, edge[i] - edge[i-1]))

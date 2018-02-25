# WiPy-2.0-DHT22
Measure temperature and humidity using the DHT22 and a WiPy 2.0

### Summary
The DHT22 sensor uses a type of onewire protocol to communicate with the outside world. This code example shows how to read values from this sensor using the WiPy 2.0. The DHT22 can be powered with 3V3 - the same volage as the WiPy uses - and needs an external 4K7 pull-up resistor attached to the DHT's serial data-pin (SDA).

### Protocol
After being triggered the DHT22 first acknowledges receipt of the trigger by pulling SDA low for 80 microseconds (μs) and then makes it high for 80 μs. The device then sends back 5 bytes with measurement information. The first two bytes provide the integral and decimal part of the humidity, the next two do the same for the temperature. The last byte acts as a checksum. Bytes are sent bit by bit with the MSB first. Every bit is represented by a 50 μs low followed by a variable length high time. The length of the high time indicates a 0 or a 1, typical values are 26 μs for a 0 and 70 μs for a 1. The DHT22 should be triggered not more often then once every two seconds.

### Code
Since the introduction of the *pycom.pulses_get()* function reading a DHT22 is easy. This function captures level transitions (so 0 -> 1 or 1 -> 0) on a certain pin plus the duration in μs until the next level transition. So after triggering the DHT22 by pulling SDA low for 1 ms just start this function. Use a timeout of at least 100 ms to stop the capture as no pulse will be longer then this. Then discard the first high as this is the acknowledge signal, and convert the remaining highs into 0's or 1's based on their duration. These 0's and 1's can then be converted to bytes and these into the measures temperature and humidity.

File *using_the_dht22.py* provides an extensively commented example on reading the DHT22. It also prints all intermediate results so it is easy to follow what is going on. It can be run stand-alone.

For a more comfortable use of the DHT22 file *dht22.py* contains a class *device* to access a sensor. After triggering a measurement the temperature and humidity can be read. Any error can be detected by checking the result of *trigger()* (which is False in case of errors) and the value of *status*. For testing purposes dht22.py can be run stand-alone, else use it as shown below.
```python
from machine import Pin

import dht22

dht = device(Pin.exp_board.G22)

for _ in range(5):
    if dht.trigger() == True:
        print("RH = {}%  T = {}C".format(dht.humidity, dht.temperature))
    else:
        print(dht.status)
```
Below the output you can expect.

> MicroPython v1.8.6-849-86da809 on 2018-01-17; WiPy with ESP32
> Type "help()" for more information.
>
> Running D:\Projects\WiPy\DHT22\measure.py
>
> RH = 51.0%  T = 21.7C
> RH = 51.0%  T = 21.7C
> RH = 51.0%  T = 21.7C
> RH = 51.0%  T = 21.7C
> RH = 51.0%  T = 21.7C

### Tools and versions
I used Atom version 1.23.3. to write the code and transfer it via Pymakr 1.2.7 to the WiPy. The WiPy 2.0 firmware version was 1.14.0.b1. The sensor I used was an AM2302 which is the same as the DHT22. A datasheet can be found here: https://akizukidenshi.com/download/ds/aosong/AM2302.pdf

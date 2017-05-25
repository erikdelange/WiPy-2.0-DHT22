# WiPy-2.0-DHT22
Measure temperature and humidity using the DHT22 and a WiPy 2.0

### Summary
The DHT22 sensor uses a type of onewire protocol to communicate with the outside world. This code example shows a way to read values from the sensor using the WiPy 2.0. The DHT22 was powered with 3V3, and had an external 4K7 pull-up resistor attached to the data-pin.

### Protocol
After being triggered the DHT22 sends back 5 bytes with information. Each bit is represented by the duration of a pulse. By measuring the length (= high time) of 40 pulses (= 5 bytes * 8 bits) it is possible to assemble the data bytes. The first two bytes provide the integral and decimal part of the humidity, the next two do the same for the temperature. The last byte acts as a checksum.

### Code
Initially I attempted to use the WiPy's interrupt mechanism. Triggering a time measurement on both the rising and falling edge of each pulse would allow me to determine the pulse length. However the reaction time of the interrupt mechanism is longer then the pulse duration (26, 50 and 70 us), so I missed pulses. See file dht22_int.py for the code and results_interrupt.txt for the resulting measured pulse lengths. The shortest pulse length measured is 88 us, so this was not the way to go.

The only other approach I saw was to use polling; continuously check if the DHT22 sends out a pulse (i.e. the data-pinis high), and if so measure when it starts and end. File dht22.py shows the code, result_polling.txt the outcome. Even now the interrupt mechanism did influence the measurement negatively, so during polling interrupts are disabled. The negative side-effect is that it may cause the WiPy to freeze if somehow communication fails (and this does happen). So in the end I was able to retreive temperature and humidity values, but using an approach which is actually to dangerous to use.

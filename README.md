# micro_ubx

This is ubx packet parser for MicroPython.

You can get UBX-NAV-PVT.

I tested it using Atom Lite and MicroPython v1.18 on 2022-01-17; ESP32 module with ESP32.

GPS module is UBX-M8030-KT

https://akizukidenshi.com/catalog/g/gM-12905/



UBX-NAV-PVT

|        |                                      |
| ------ | ------------------------------------ |
| year   | Year (UTC)                           |
| month  | Month, range 1..12 (UTC)             |
| day    | Day of month, range 1..31 (UTC)      |
| hour   | Hour of day, range 0..23 (UTC)       |
| min    | Minute of hour, range 0..59 (UTC)    |
| sec    | Seconds of minute, range 0..60 (UTC) |
| lon    | Longitude                            |
| lat    | Latitude                             |
| height | Height above ellipsoid               |
| hMSL   | Height above mean sea level          |



## micro_ubx.py

simple read sec(UTC)

~~~
uart = UART(1, baudrate=9600, tx=26, rx=32)

parser = UbxParser()

while True:
    while uart.any():
        rxbuf = bytearray(uart.any())
        uart.readinto(rxbuf)

        nav_pvt = parser.parse(rxbuf)
        if nav_pvt:
        	print(nav_pvt._sec)
~~~





## Reference

pyubx2

I was referring to the checksum calculation method.

https://github.com/semuconsulting/pyubx2


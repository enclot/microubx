from machine import UART
from io import BytesIO
import binascii
import struct
import time
 
class UbxParser:
    def __init__(self):
        self._carryover = bytearray()
        
    def parse(self, rxbuf) -> object: 
        message_buf = self._carryover + rxbuf    
        bytes_io = BytesIO(message_buf)

        while bytes_io.tell()!=len(message_buf):
            
            byte1 = bytes_io.read(1)
            if byte1 != b'\xb5':
                continue
            byte2 = bytes_io.read(1)
            byte_header = byte1+byte2
            if byte_header == b"\xb5\x62":
                read_byte = bytes_io.read(4)
                class_field = read_byte[0:1]
                id_field = read_byte[1:2]
                length_byte = read_byte[2:4]
                length_field = int.from_bytes(length_byte, "little")

                if bytes_io.tell()+length_field+2 > len(message_buf):
                    bytes_io.seek(0)
                    self._carryover = bytes_io.read()
                    break
            
                byten = bytes_io.read(length_field + 2)
                payload_field = byten[0:length_field]
#                 print(f"payload length {len(payload_field)}")
                checksum = byten[length_field : length_field + 2]
                if checksum==self._checksum(class_field + id_field + length_byte + payload_field):
#                     print(f"checksum ok {binascii.hexlify(class_field) } {binascii.hexlify(id_field) }")
                    if class_field==b'\x01' and id_field==b'\x07':
                        return UbxNavPvt(payload_field)
                
                self._carryover = bytes_io.read()
                break
        return None
    
    def _checksum(self, content:bytes):
        check_a = 0
        check_b = 0

        for char in content:
            check_a += char
            check_a &= 0xFF
            check_b += check_a
            check_b &= 0xFF

        return bytes((check_a, check_b))    

class UbxNavPvt:
    def __init__(self, payload):
        self._year, self._month, self._day = struct.unpack('HBB',payload[4:])
        self._hour, self._min, self._sec = struct.unpack('BBB',payload[8:])
        self._lon, self._lat, self._height, self._hMSL = struct.unpack('llll',payload[24:])
        self._fixType = struct.unpack('B',payload[20:])[0]
        self._lon = self._lon*1e-7
        self._lat = self._lat*1e-7
        self._height = self._height/1000
        self._hMSL = self._hMSL/1000
        
    @property
    def utc(self):
        #(year, month, day, weekday, hours, minutes, seconds, subseconds)
        return self._year, self._month, self._day, 0, \
                self._hour, self._min, self._sec, 0
    @property
    def jst(self):#+9hour
        #(year, month, mday, hour, minute, second, weekday, yearday) 
        t = time.mktime((self._year, self._month, self._day, \
                         self._hour+9, self._min, self._sec, 0, 0))
        
        year,month,mday,hour,minute,second,weekday,yearday = time.localtime(t)
        #(year, month, day, weekday, hours, minutes, seconds, subseconds)
        return year, month, mday, weekday, hour, minute, second, 0
    


    


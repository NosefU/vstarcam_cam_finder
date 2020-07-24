import socket
import struct
from time import sleep


class Camera:
    def __init__(self, response: bytes):
        self.raw_data = response
        # все смещения и длины полей получены с помощью вайршарка

        # ip
        offset, length = int('4', 16), 15
        self.ip = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # mac
        offset, length = int('54', 16), 5
        b_mac = self._get_bytes(offset, length)
        self.mac = ':'.join([byte.hex() for byte in struct.unpack(str(len(b_mac)) + 'c', b_mac)]).upper()

        # netmask
        offset, length = int('14', 16), 15
        self.netmask = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # gateway
        offset, length = int('24', 16), 15
        self.gateway = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # dns1
        offset, length = int('34', 16), 15
        self.dns1 = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # dns2
        offset, length = int('44', 16), 15
        self.dns2 = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # port
        offset, length = int('5A', 16), 2
        self.port = int.from_bytes(self._get_bytes(offset, length), "little")

        # cloud id
        offset, length = int('5C', 16), 15
        self.cloud_id = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # name
        offset, length = int('7C', 16), 31
        self.name = self._get_bytes(offset, length).decode("utf-8").rstrip().lstrip()

        # firmware version
        offset, length = int('CC', 16), 15
        self.firmware = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()

        # mode
        offset, length = int('DC', 16), 15
        mode = self._get_bytes(offset, length).decode("ascii").rstrip().lstrip()
        self.mode = mode[13]

    def _get_bytes(self, offset, length):
        return self.raw_data[offset: offset + length]

    @property
    def full_info(self):
        return (f'{self.name}\n'
                f'IP: {self.ip}:{self.port}\n'
                f'Cloud ID: {self.cloud_id}\n'
                f'Firmware ver.: {self.firmware}\n'
                f'Netmask: {self.netmask}\n'
                f'Gateway: {self.gateway}\n'
                f'Primary DNS: {self.dns1}\n'
                f'Secondary DNS: {self.dns2}\n'
                f'MAC: {self.mac}')

    @property
    def info(self):
        return (f'{self.name}\n'
                f'IP: {self.ip}:{self.port}\n'
                f'Cloud ID: {self.cloud_id}\n')


# создаём сокет для отправки широковещалки
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sender.bind(('', 8601))
sender.settimeout(2)
brcast_message = bytes.fromhex('44480101')      # пакет, который отправляет родная софтина

# создаём сокет для приёма ответов
receiver = socket.socket(type=socket.SOCK_DGRAM)
receiver.bind(('localhost', 8600))

cctv = []
cams_avail = False

while True:
    sender.sendto(brcast_message, ('255.255.255.255', 8600))    # отправляем широковещалку
    try:
        data, addr = sender.recvfrom(532)       # пытаемся получить от кого-нибудь ответ (размер буфера из вайршарка)
    except socket.timeout as exc:               # если ответа не дождались,
        if cams_avail:                          # то отчитываемся пользователю и засыпаем на 2 секунды
            print('-' * 25)
            print('No cams available')
            cams_avail = False
        sleep(2)
        continue

    cams_avail = True
    camera = Camera(data)       # если ответ дождались, то разбираем пакет
    # если такой камеры ещё не было, то выводим инфу о ней на консоль
    if (camera.ip, camera.port) not in [(camera.ip, camera.port) for camera in cctv]:
        cctv.append(camera)
        print('-' * 25)
        print(camera.full_info)

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from Crypto import Random
import time


def get_msg(msg):
    keyPair = RSA.generate(3072)

    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()

    privKeyPEM = keyPair.exportKey()

    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    return encrypted


def hex_dump2(s):
    cnt = 0
    ascii_text = ""
    print("len=" + str(len(s)))
    for i in range(len(s)):
        cnt += 1
        value = s[i]
        print("%02X" % value, end=" ")
        if value > 31:
            ascii_text += chr(value)
        else:
            ascii_text += '.'
        if cnt % 16 == 0:
            print("   |" + ascii_text)
            ascii_text = ""
        elif cnt % 8 == 0:
            print("  ", end=" ")
    if cnt % 16 != 0:
        for i in range(cnt % 16, 16):
            print("  ", end=" ")
            if i == 8 and cnt % 8 != 0:
                print("  ", end=" ")
        print("   |" + ascii_text)


class Algorithm:

    def __init__(self, mp3_file_name, key, rsa_msg=''):
        self.file_name = mp3_file_name
        self.msg = rsa_msg
        self.key = key
        self.len_msg = 128
        self.frames_arr = []
        self.bitrate = {"0": None, "1": 32, "2": 40, "3": 48, "4": 56, "5": 64, "6": 80, "7": 96, "8": 112, "9": 128,
                        "a": 160, "b": 192, "c": 224, "d": 256, "e": 320, "f": None}
        self.frequency = {"0": 44100, "1": 48000, "2": 32000, "3": None}

    def find_frames(self):
        self.frames_arr = []
        with open(self.file_name, "rb+") as file:
            while True:
                x = file.read(1)
                if x == b'':
                    break
                elif x == b"\xFF":
                    x = file.read(1)
                    if x == b"\xFB" or x == b"\xFA":
                        self.frames_arr.append(file.tell() - 2)
                        self.find_len(file)

    def find_len(self, file):
        data = file.read(1)
        data_str = format(data[0], "02x")
        if len(data_str) < 2:
            return 0
        bitrate = self.bitrate[data_str[0]]
        if bitrate is None:
            return 0
        frequency_bin = int(data_str[1], 16)
        if frequency_bin >= 12:
            return 0
        elif 3 >= frequency_bin >= 0:
            frequency = self.frequency["0"]
        elif 7 >= frequency_bin >= 4:
            frequency = self.frequency["1"]
        elif 11 >= frequency_bin >= 8:
            frequency = self.frequency["2"]
        else:
            return 0
        if (data[0] | 0xFD) == 0xFF:
            padding = 1
        else:
            padding = 0
        size = ((144 * bitrate * 1000) // frequency) + padding
        file.read(size - 3)
        return size

    def put_msg(self):
        with open(self.file_name, "r+b") as file:
            byte_per_frame = self.len_msg // len(self.frames_arr)
            reminder = self.len_msg % len(self.frames_arr)
            key_data = self.key.exportKey()
            offset = key_data[100 + int(str(len(self.frames_arr))[0])] + 52
            count = 0
            i = 0
            divider = len(self.frames_arr) // self.len_msg
            if byte_per_frame == 0 or (reminder == 0 and byte_per_frame == 1):
                for item in self.frames_arr:
                    if i % divider == 0:
                        if count < self.len_msg:
                            file.seek(item + offset)
                            file.write(self.msg[count:count + 1])
                            count += 1
                        else:
                            break
                    i += 1
            else:
                print('aa')
                pass

    def encrypt(self):
        self.find_frames()
        self.put_msg()

    def decrypt(self):
        self.find_frames()
        data = b''
        with open(self.file_name, "rb+") as file:
            byte_per_frame = self.len_msg // len(self.frames_arr)
            reminder = self.len_msg % len(self.frames_arr)
            key_data = self.key.exportKey()
            offset = key_data[100 + int(str(len(self.frames_arr))[0])] + 52
            count = 0
            i = 0
            divider = len(self.frames_arr) // self.len_msg
            if byte_per_frame == 0 or (reminder == 0 and byte_per_frame == 1):
                for item in self.frames_arr:
                    if i % divider == 0:
                        if count < self.len_msg:
                            file.seek(item + offset)
                            data += file.read(1)
                            count += 1
                        else:
                            break
                    i += 1
            else:
                pass
        return data


def main():
    file_name = "fake.mp3"
    msg = b'bacghjgfhn'
    key = RSA.generate(1024)
    public = key.publickey()
    encryptor = PKCS1_OAEP.new(public)
    encrypted = encryptor.encrypt(msg)
    x = Algorithm(file_name, public, encrypted)
    x.encrypt()
    y = Algorithm(file_name, public)
    msg = y.decrypt()
    hex_dump2(msg)
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(msg)
    print(decrypted)


if __name__ == '__main__':
    main()

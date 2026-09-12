import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from algorithm import Algorithm
import sys
import graphic
import pygame
import hokpygame
import time

window_width = 900
window_height = 700
white = (255, 255, 255)
background_color = (110, 150, 75)
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("mp3")
FONT = hokpygame.FONT
FONT_size = hokpygame.FONT_size


def main(ip, port):
    client_socket = socket.socket()
    client_socket.connect((ip, port))

    key = RSA.generate(1024)
    public = key.publickey()
    data = public.exportKey()

    send_with_size(client_socket, data)
    data = recv_by_size(client_socket)
    with open("fake.mp3", 'wb') as f:
        f.write(data)

    x = Algorithm("fake.mp3", public)
    msg = x.decrypt()
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(msg)
    done =False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                graphic.print_pygame("the message is: " + decrypted.decode(), 0, 0)

    client_socket.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit("enter ip")
    else:
        ip = sys.argv[1]
    main(ip, 825)

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
from algorithm import Algorithm
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import graphic
import pygame
import hokpygame

window_width = 900
window_height = 700
white = (255, 255, 255)
background_color = (110, 150, 75)
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("mp3")
FONT = hokpygame.FONT
FONT_size = hokpygame.FONT_size


def get_msg(msg, public):
    encryptor = PKCS1_OAEP.new(public)
    encrypted = encryptor.encrypt(msg)
    return encrypted


def main(ip, port):
    server = socket.socket()
    server.bind((ip, port))
    server.listen(4)


    client, address = server.accept()
    data = recv_by_size(client)
    public = RSA.importKey(data)

    is_input, msg = graphic.input_pygame(window_width / 2 - hokpygame.max_width / 2,
                                         window_height / 2 - FONT_size / 2, "enter your message:")
    pygame.quit()
    msg = str(msg).encode()
    rsa_msg = get_msg(msg, public)

    x = Algorithm("file.mp3", public, rsa_msg)
    x.encrypt()

    with open("file.mp3", 'rb') as file:
        data = file.read()
    send_with_size(client, data)

    server.close()


if __name__ == '__main__':
    main("0.0.0.0", 825)

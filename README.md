# RSA Encryption & Audio Steganography

## Overview
A client-server application built in Python that demonstrates secure communication over TCP sockets. The project combines asymmetric cryptography (RSA) with steganography by hiding encrypted messages within MP3 audio files before transmission. 

Originally developed as a final project for a specialized high school cybersecurity program, the codebase was recently migrated from Python 2.7 to Python 3.

## Core Flow
1. **Server-Side:** Prompts the user for a plaintext message, encrypts it using the RSA algorithm, and embeds the resulting ciphertext into an MP3 file (steganography payload).
2. **Transmission:** The modified MP3 file is sent over a TCP socket connection from the server to the client.
3. **Client-Side:** Receives the MP3 file, extracts the hidden ciphertext, decrypts it using the corresponding RSA keys, and displays the original message via a graphical interface.

## Repository Structure
* `/server` - Contains the server logic (`server.py`), payload generation, and encryption algorithms.
* `/client` - Contains the client logic (`client.py`), extraction protocol, and decryption algorithms.
* `Project_Documentation.pdf` - Detailed project report outlining the architecture and network protocols.

## Tech Stack & Concepts
* **Language:** Python 3 (Migrated from 2.7)
* **Networking:** TCP/IP Sockets, custom size-based transmission protocol (`tcp_by_size.py`).
* **Security:** RSA Cryptography, Steganography.
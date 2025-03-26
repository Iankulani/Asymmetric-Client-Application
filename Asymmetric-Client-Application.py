# -*- coding: utf-8 -*-
"""
Created on Tue March  26 08:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("Asymetric Client Application")
print(Fore.GREEN+font)

import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Function to load the server's public key
def load_public_key():
    with open('public_key.pem', 'rb') as public_file:
        public_key = serialization.load_pem_public_key(public_file.read(), backend=default_backend())
    return public_key

# Function to encrypt the message using the public key
def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

# Setup client socket
def start_client():
    server_ip = input("Enter server IP:")
    server_port = int(input("Enter server port:"))

    # Load server's public key
    public_key = load_public_key()

    # Get message from the user
    message = input("Enter message to send to the server:")

    # Encrypt the message using the server's public key
    encrypted_message = encrypt_message(public_key, message)

    # Create and connect the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Send the encrypted message
    client_socket.send(encrypted_message)
    print(f"Encrypted message sent to server.")

    # Receive the server's response
    response = client_socket.recv(1024)
    print(f"Response from server: {response.decode()}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()

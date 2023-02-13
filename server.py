import socket
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import seaborn as sns
import time as time
import math as math

def bs_eu_option(s, k, t, r, d, sigma, option_type): 
    d_1 = (np.log(s/k)+(r-d+((sigma**2)/2))*(t))/(sigma*np.sqrt(t))
    d_2 = d_1 - (sigma*np.sqrt(t))
    
    if option_type == "call":
        return norm.cdf(d_1) * s - norm.cdf(d_2) * k * np.exp(-r * t)
    elif option_type == "put":
        return norm.cdf(-d_2) * k * np.exp(-r * t) -norm.cdf(-d_1) * s

    else:
        raise ValueError("Invalid option type")

# Create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12347)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print(f'Listening for incoming connections on {server_address[0]}:{server_address[1]}')

while True:
    # Accept an incoming connection
    connection, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

    # Receive the input parameters from the client
    s, k, t, r, d, sigma, option_type = connection.recv(1024).decode().split(',')
    s, k, t, r, d ,sigma = map(float, [s, k, t, r, d, sigma])

    
    # Calculate the option price
    option_price = bs_eu_option(s, k, t, r, d, sigma, option_type)
    
    # Send the option price back to the client
    connection.send(str(option_price).encode())

    # Close the connection
    connection.close()

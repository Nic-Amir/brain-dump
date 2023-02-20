import socket
import numpy as np
import time
import threading

# Define the function to generate random number using the geometric Brownian motion Wiener process
def generate_random_number(S0=100, mu=0.1, sigma=0.2, dt=1/365, T=1):
    n = int(T/dt)
    t = np.linspace(0, T, n)
    W = np.random.standard_normal(size=n)
    W = np.cumsum(W)*np.sqrt(dt) 
    X = (mu-0.5*sigma**2)*t + sigma*W 
    S = S0*np.exp(X) 
    return S[-1]

# Define the function to stream the data over a socket connection
def stream_data(conn):
    while True:
        # Generate a random number using the Wiener process function
        sprayed_number = generate_random_number()

        # Round the sprayed number to 2 decimal places
        sprayed_number = round(sprayed_number, 2)

        # Send the sprayed number to the client over the socket connection
        conn.sendall(str(sprayed_number).encode())

        # Wait for 1 second before generating the next random number
        time.sleep(1)

# Define the function to start the server and listen for incoming connections
def start_server(host='', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started on {host}:{port}')

        while True:
            # Wait for a client to connect
            conn, addr = s.accept()
            print(f'Client connected from {addr}')

            # Start streaming data to the client in a separate thread
            thread = threading.Thread(target=stream_data, args=(conn,))
            thread.start()

# Start the server
if __name__ == '__main__':
    start_server()
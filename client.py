import socket

# Create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12347)
client_socket.connect(server_address)

# Get the input parameters from the user
s = input("Enter the stock price (s): ")
k = input("Enter the strike price (k): ")
t = input("Enter the time to maturity (t) in years: ")
r = input("Enter the risk-free interest rate (r): ")
d = input("Enter the dividend yield (d): ")
sigma = input("Enter the implied volatility (sigma): ")
option_type = input("Enter the option type (call/put): ")

input_params = f"{s},{k},{t},{r},{d},{sigma},{option_type}"

# Send the input parameters to the server
client_socket.send(input_params.encode())

# Receive the option price from the server
option_price = float(client_socket.recv(1024).decode())

# Close the socket
client_socket.close()

print(f'Option price: {option_price}')

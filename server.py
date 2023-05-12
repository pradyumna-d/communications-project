import os
import socket
import logging

# Define the server address and port
SERVER_ADDRESS = '127.0.0.1'  # Replace with the actual server IP address
SERVER_PORT = 5000  # Replace with the actual server port number

# Configure logging
logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
server_socket.listen()
print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")
logging.info(f"Server started listening on {SERVER_ADDRESS}:{SERVER_PORT}")


while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    logging.info(f"Accepted new connection from {client_address}")

    # Receive data from the client
    received_data = client_socket.recv(1024).decode().strip()
    print(f"Received command: {received_data}")

    # Handle the "list" command
    if received_data == "list":
        logging.info("Received 'list' request from client")
        # Get the list of files in the current directory
        file_list = os.listdir()

        # Send the file list to the client
        data_to_send = "\n".join(file_list)
        client_socket.send(data_to_send.encode())
        logging.info("Sent file list to client")

    # Handle the "get" command
    elif received_data.startswith("get "):
        # Get the file name from the command
        file_name = received_data.split()[1]
        logging.info(f"Received 'get' request for file {file_name} from client")

        # Check if the file exists in the current directory
        if os.path.exists(file_name):
            # confirsmation that file exists
            print(f"file {file_name} exists")

            # Send the file to the client
            with open(file_name, "rb") as f:
                data = f.read()
                client_socket.send(data)
                logging.info(f"Sent file {file_name} to client")
        else:
            # Send the NOT FOUND status to the client
            client_socket.send("NOT FOUND".encode())
    #if received data is terminate
    elif received_data == "terminate":
        logging.info("Received 'terminate' request from client")
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")

    # Handle other commands
    else:
        # Send an error message to the client
        error_message = "Invalid command"
        client_socket.send(error_message.encode())
        logging.error(f"Error: {error_message}")

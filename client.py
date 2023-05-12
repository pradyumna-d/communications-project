import socket
import sys
import os
import logging
import tkinter as tk

#defining a login window
def show_login_window():
    def login():
        # Perform login validation here
        username = username_entry.get()
        password = password_entry.get()
        if username == "user1" and password == "password":
            login_window.destroy()
        else:
            error_label.config(text="Invalid username or password")

    # Create the login window
    login_window = tk.Tk()
    login_window.title("Login")

    # Create a frame for the username and password fields
    frame = tk.Frame(login_window)
    frame.pack(padx=30, pady=30)

    # Create the username label and entry field
    username_label = tk.Label(frame, text="Username")
    username_label.pack(side="top")
    username_entry = tk.Entry(frame)
    username_entry.pack(side="top")

    # Create the password label and entry field
    password_label = tk.Label(frame, text="Password")
    password_label.pack(side="top")
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(side="bottom")

    # Create the login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    # Create an error label
    error_label = tk.Label(login_window, fg="red")
    error_label.pack()

    # Start the login window event loop
    login_window.mainloop()

#calling the login window
show_login_window()


# Define the server address and port
SERVER_ADDRESS = '127.0.0.1'  # Replace with the actual server IP address
SERVER_PORT = 5000  # Replace with the actual server port number

# Configure logging
logging.basicConfig(filename='client.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Check if the second command line argument is "list"
if len(sys.argv) > 1 and sys.argv[1] == "list":
    # Send a request to the server for a list of all files in the current server file directory
    request = "list"
    client_socket.send(request.encode())
    logging.info(f"Sent request to server: {request}")

    # Receive the list of filenames from the server
    filenames = client_socket.recv(1024).decode()

    # Print out the list of filenames
    print("Files in server directory:")
    print(filenames)
    logging.info(f"Received response from server: {filenames}")

# Check if the second command line argument is "get"
elif len(sys.argv) > 1 and sys.argv[1] == "get":
    # Check that the third command line argument is a valid filename
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        print("Error: Please provide a filename")
        sys.exit()

    # Send a request to the server for the file with the given filename
    request = str("get ")+filename
    client_socket.send(request.encode())
    logging.info(f"Sent request to server: {request}")

    # Receive the file data from the server
    file_data = client_socket.recv(2*1024*1024)

    # Check if the file was found on the server
    if file_data.decode() == f"File '{filename}' not found":
        print(f"Error: {file_data.decode()}")
        logging.error(f"Received error from server: {file_data.decode()}")
        sys.exit()

    # Write the file data to a file with the same name in the current client file directory
    with open(filename, "wb") as f:
        f.write(file_data)
        f.close()

    print(f"File '{filename}' downloaded successfully")
    logging.info(f"File '{filename}' downloaded successfully")

#checking if second command line argument is terminate
elif len(sys.argv) > 1 and sys.argv[1] == "terminate":
    request = "terminate"
    client_socket.send(request.encode())
    logging.info(f"Sent request to server: {request}")
    client_socket.close()
    logging.info("Client socket closed")

# If no command line argument is provided, send a invalid request to the server
else:
    # Send data to the server
    data_to_send = "invalid command"  # Replace with the actual data to be sent
    client_socket.send(data_to_send.encode())
    logging.info(f"Sent request to server: {data_to_send}")

    # Receive response from the server
    received_response = client_socket.recv(1024).decode()
    print(f"Received response: {received_response}")
    logging.info(f"Received response from server: {received_response}")

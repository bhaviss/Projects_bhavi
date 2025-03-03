import socket
import os
from threading import Thread
from cryptography.fernet import Fernet
import logging

# Logging setup
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load encryption key
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)

# Decrypt data
def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)

# Authenticate user
def authenticate_user(username, password):
    # Replace with your authentication logic
    users = {
        "user1": "password1",
        "user2": "password2"
    }
    return users.get(username) == password

# Handle client requests
def handle_client(client_socket, client_address, key):
    logging.info(f"Client connected: {client_address}")
    while True:
        try:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            logging.info(f"Received command: {command} from {client_address}")

            if command.startswith("AUTH"):
                _, username, password = command.split()
                if authenticate_user(username, password):
                    client_socket.send("OK".encode())
                else:
                    client_socket.send("FAIL".encode())

            elif command.startswith("UPLOAD"):
                _, file_name = command.split()
                client_socket.send("READY".encode())
                encrypted_data = b""
                while True:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        break
                    encrypted_data += chunk
                with open(file_name, "wb") as file:
                    file.write(decrypt_data(encrypted_data, key))
                logging.info(f"File uploaded: {file_name}")

            elif command.startswith("DOWNLOAD"):
                _, file_name = command.split()
                if os.path.exists(file_name):
                    with open(file_name, "rb") as file:
                        file_data = file.read()
                    encrypted_data = encrypt_data(file_data, key)
                    client_socket.sendall(encrypted_data)
                    logging.info(f"File sent: {file_name}")
                else:
                    client_socket.send(b"")

            elif command == "LIST":
                files = os.listdir()
                client_socket.send("\n".join(files).encode())

            elif command.startswith("DELETE"):
                _, file_name = command.split()
                if os.path.exists(file_name):
                    os.remove(file_name)
                    client_socket.send(f"File {file_name} deleted successfully.".encode())
                    logging.info(f"File deleted: {file_name}")
                else:
                    client_socket.send(f"File {file_name} not found.".encode())

            else:
                client_socket.send("Invalid command.".encode())

        except Exception as e:
            logging.error(f"Error handling client {client_address}: {e}")
            break

    client_socket.close()
    logging.info(f"Client disconnected: {client_address}")

# Start the server
def start_server():
    server_ip = "0.0.0.0"
    server_port = 12347  # Ensure this matches the client code
    key = load_key()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    logging.info(f"Server started on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket, client_address, key))
        client_thread.start()

if __name__ == "__main__":
    start_server()

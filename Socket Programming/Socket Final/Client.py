import socket
import os
import logging
from cryptography.fernet import Fernet
import sys

# Set up logging
logging.basicConfig(filename='client.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load encryption key (Assuming key is pre-generated and saved as key.key)
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

# Cross-platform password masking with `*`
def get_password(prompt="Enter password: "):
    """Read a password with '*' masking."""
    print(prompt, end="", flush=True)
    password = ""
    try:
        if os.name == 'nt':  # Windows system
            import msvcrt
            while True:
                char = msvcrt.getch()
                if char in {b'\r', b'\n'}:  # Enter key
                    print("")  # Move to the next line
                    break
                elif char == b'\x08':  # Backspace key
                    if len(password) > 0:
                        print("\b \b", end="", flush=True)
                        password = password[:-1]
                else:
                    print("*", end="", flush=True)
                    password += char.decode()
        else:  # Unix-like system
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    char = sys.stdin.read(1)
                    if char == '\n' or char == '\r':  # Enter key
                        print("")  # Move to the next line
                        break
                    elif char == '\x7f':  # Backspace key
                        if len(password) > 0:
                            sys.stdout.write("\b \b")
                            sys.stdout.flush()
                            password = password[:-1]
                    else:
                        sys.stdout.write("*")
                        sys.stdout.flush()
                        password += char
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception as e:
        print("\nError reading password input.")
        logging.error(f"Password input error: {e}")
    return password

# Authenticate user
def authenticate(server_ip, server_port, username, password):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(f"AUTH {username} {password}".encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()
        if response == "OK":
            logging.info(f"Authentication successful for user: {username}")
            return True
        else:
            logging.warning(f"Authentication failed for user: {username}")
            return False
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        return False

# Upload file
def upload_file(server_ip, server_port, key):
    file_name = input("Enter file name to upload: ").strip()
    if not os.path.exists(file_name):
        print("File not found.")
        logging.error(f"Upload failed: {file_name} not found.")
        return

    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
        encrypted_data = encrypt_data(file_data, key)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(f"UPLOAD {file_name}".encode())
        
        # Wait for acknowledgment before sending file
        ack = client_socket.recv(1024).decode()
        if ack == "READY":
            client_socket.sendall(encrypted_data)
            print(f"File {file_name} uploaded successfully.")
            logging.info(f"File uploaded: {file_name}")
        else:
            print(f"Failed to upload file: {ack}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        logging.error(f"Upload error: {e}")
    finally:
        client_socket.close()

# Download file
def download_file(server_ip, server_port, key):
    file_name = input("Enter file name to download: ").strip()
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(f"DOWNLOAD {file_name}".encode())

        encrypted_data = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            encrypted_data += data
        
        decrypted_data = decrypt_data(encrypted_data, key)
        with open(f"downloaded_{file_name}", 'wb') as file:
            file.write(decrypted_data)
        print(f"File {file_name} downloaded successfully.")
        logging.info(f"File downloaded: {file_name}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        logging.error(f"Download error: {e}")
    finally:
        client_socket.close()

# List files
def list_files(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send("LIST".encode())
        file_list = client_socket.recv(1024).decode()
        print("Files on server:")
        print(file_list)
        logging.info("Listed files from server.")
    except Exception as e:
        print(f"Error listing files: {e}")
        logging.error(f"List error: {e}")
    finally:
        client_socket.close()

# Delete file
def delete_file(server_ip, server_port):
    file_name = input("Enter file name to delete: ").strip()
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(f"DELETE {file_name}".encode())
        response = client_socket.recv(1024).decode()
        print(response)
        logging.info(f"Delete response: {response}")
    except Exception as e:
        print(f"Error deleting file: {e}")
        logging.error(f"Delete error: {e}")
    finally:
        client_socket.close()

# Command-line interface with menu
def command_line_client():
    server_ip = input("Enter server IP address: ").strip()
    server_port = 12347  # Make sure this matches your server code's port
    key = load_key()

    username = input("Enter username: ")
    password = get_password("Enter password: ")

    if not authenticate(server_ip, server_port, username, password):
        print("Authentication failed!")
        return

    while True:
        print("\nMenu:")
        print("1. Upload File")
        print("2. Download File")
        print("3. List Files")
        print("4. Delete File")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            upload_file(server_ip, server_port, key)
        elif choice == "2":
            download_file(server_ip, server_port, key)
        elif choice == "3":
            list_files(server_ip, server_port)
        elif choice == "4":
            delete_file(server_ip, server_port)
        elif choice == "5":
            print("Exiting...")
            logging.info("Client exited.")
            break
        else:
            print("Invalid option. Please try again.")
            logging.warning("Invalid menu option selected.")

if __name__ == "__main__":
    command_line_client()

